import os
import cv2
import numpy as np
import onnxruntime as ort
import time
import math
from datetime import datetime
from gps_module import start_gps, get_location

# ---------------- CONFIG ----------------
BASE_DIR = os.getcwd()
MODEL_PATH = os.path.join(BASE_DIR, "best_dynamic_int8.onnx")

CONF_THRESHOLD = 0.4
NMS_THRESHOLD = 0.45
TOTAL_FRAMES_TO_SAVE = 120

OBSTACLE_DIR = os.path.join(BASE_DIR, "obstacle")
POTHOLE_DIR = os.path.join(BASE_DIR, "pothole")
LOG_FILE = os.path.join(BASE_DIR, "pothole_detection.txt")

# -------- UPLOAD ZONE CONFIG --------
TARGET_LAT = 12.971598      # 🔁 Change to your target location
TARGET_LON = 77.594566      # 🔁 Change to your target location
UPLOAD_RADIUS = 100         # meters

upload_triggered = False

os.makedirs(OBSTACLE_DIR, exist_ok=True)
os.makedirs(POTHOLE_DIR, exist_ok=True)

CLASS_NAMES = {0: "obstacle", 1: "pothole"}

print("Model path:", MODEL_PATH)
print("Saving videos inside:", BASE_DIR)

# ---------------- MODEL ----------------
if not os.path.exists(MODEL_PATH):
    print("❌ ERROR: Model file not found!")
    exit()

session = ort.InferenceSession(MODEL_PATH, providers=['CPUExecutionProvider'])
input_name = session.get_inputs()[0].name

# ---------------- START GPS ----------------
start_gps()

# ---------------- DISTANCE FUNCTION ----------------
def is_within_radius(lat1, lon1, lat2, lon2, radius_meters=100):
    try:
        R = 6371000
        phi1 = math.radians(float(lat1))
        phi2 = math.radians(float(lat2))
        delta_phi = math.radians(float(lat2) - float(lat1))
        delta_lambda = math.radians(float(lon2) - float(lon1))

        a = math.sin(delta_phi/2)**2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c

        return distance <= radius_meters
    except:
        return False

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

print("🚀 System Monitoring... Press 'q' to quit.")

# ---------------- RECORD STATE ----------------
writers = {0: None, 1: None}
frame_counts = {0: 0, 1: 0}

prev_time = time.time()
pothole_logged = False

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    real_fps = 1 / (current_time - prev_time)
    prev_time = current_time
    save_fps = max(8, min(real_fps, 25))

    h0, w0 = frame.shape[:2]
    frame_area = h0 * w0

    # -------- PREPROCESS --------
    img = cv2.resize(frame, (640, 640))
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)

    outputs = session.run(None, {input_name: img})[0]
    outputs = np.squeeze(outputs).T

    boxes, scores, class_ids = [], [], []

    for det in outputs:
        cls_scores = det[4:]
        cls_id = np.argmax(cls_scores)
        conf = cls_scores[cls_id]

        if conf > CONF_THRESHOLD:
            cx, cy, w, h = det[:4]

            x1 = int((cx - w / 2) * w0 / 640)
            y1 = int((cy - h / 2) * h0 / 640)
            w_box = int(w * w0 / 640)
            h_box = int(h * h0 / 640)

            boxes.append([x1, y1, w_box, h_box])
            scores.append(float(conf))
            class_ids.append(cls_id)

    indices = cv2.dnn.NMSBoxes(boxes, scores, CONF_THRESHOLD, NMS_THRESHOLD)
    detected_classes = set()

    if len(indices) > 0:
        for i in indices.flatten():
            cls = class_ids[i]
            conf = scores[i]
            x, y, w_box, h_box = boxes[i]

            detected_classes.add(cls)

            if cls == 1:  # POTHOLE
                box_area = w_box * h_box
                intensity_pct = (box_area / frame_area) * 100

                if intensity_pct < 1.5:
                    level = "LOW"
                elif intensity_pct < 4:
                    level = "MEDIUM"
                else:
                    level = "HIGH"

                label = f"POTHOLE | INT:{level}"

                # -------- EVENT-BASED LOGGING --------
                if not pothole_logged:
                    lat, lon = get_location()

                    with open(LOG_FILE, "a") as f:
                        f.write(f"Timestamp: {datetime.now()}\n")
                        f.write(f"Latitude: {lat}\n")
                        f.write(f"Longitude: {lon}\n")
                        f.write(f"Severity: {level}\n")
                        f.write(f"Confidence: {conf:.2f}\n")

                        if lat != "No Fix":
                            f.write(f"Google Maps: https://www.google.com/maps?q={lat},{lon}\n")

                        f.write("---------------------------------\n")

                    print(f"📍 Pothole logged → {lat}, {lon}")

                    # -------- ZONE CHECK FOR UPLOAD --------
                    if lat != "No Fix" and not upload_triggered:
                        if is_within_radius(lat, lon, TARGET_LAT, TARGET_LON, UPLOAD_RADIUS):
                            print("📡 Upload zone reached. Running upload script...")
                            os.system("python upload_script.py")
                            upload_triggered = True

                    pothole_logged = True

            else:
                label = "OBSTACLE"

            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 0, 255), 2)
            cv2.putText(frame, label, (x, y - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

    # -------- RESET FLAGS --------
    if 1 not in detected_classes:
        pothole_logged = False

    lat, lon = get_location()
    if lat != "No Fix":
        if not is_within_radius(lat, lon, TARGET_LAT, TARGET_LON, UPLOAD_RADIUS):
            upload_triggered = False

    # -------- TIMESTAMP --------
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.rectangle(frame, (0, 0), (w0, 35), (0, 0, 0), -1)
    cv2.putText(frame, timestamp, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Road Anomaly Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
