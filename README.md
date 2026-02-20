# 🚀 Edge AI Based Road Anomaly Detection using Raspberry Pi

---

## 📌 Project Overview

This project implements a **Real-Time Edge AI Road Anomaly Detection System** deployed on a Raspberry Pi.

The system detects:

- 🕳️ Potholes  
- 🚧 Obstacles  

This solution is optimized for **edge deployment on ARM-based systems** and runs entirely on CPU using an INT8 quantized ONNX model.

---

## ✨ Core Features

- ONNX optimized YOLO model (INT8)
- CPU-only inference (No GPU required)
- Real-time camera processing
- Timestamp overlay
- Pothole intensity classification (LOW / MEDIUM / HIGH)
- Automatic video logging
- Separate folders for pothole and obstacle events
- Natural playback speed recording
- 📍 GPS-based pothole tagging
- 🗺 Google Maps link generation
- 📡 Geo-fenced smart upload trigger
- 🧠 Event-based intelligent logging

---

# 🛠 Hardware Requirements

- Raspberry Pi 4 / Raspberry Pi 5  
- Raspberry Pi OS (64-bit recommended)  
- USB Camera or Pi Camera Module  
- High-speed microSD card (Class 10+)  
- GPS Module (USB/UART based, e.g., Neo-6M)

---

# 💻 Software Requirements

- Raspberry Pi OS  
- Python 3.11 (via pyenv)  
- OpenCV  
- NumPy  
- ONNX Runtime  

---

# 🔧 Complete Setup Guide (Clean Environment Using pyenv)

Follow these steps exactly.

---

## 🔹 Step 1 — Update Raspberry Pi

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 🔹 Step 2 — Install Build Dependencies

```bash
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev \
libffi-dev liblzma-dev git
```

---

## 🔹 Step 3 — Install pyenv

```bash
curl https://pyenv.run | bash
```

Add pyenv to your shell:

```bash
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
exec "$SHELL"
```

Verify installation:

```bash
pyenv --version
```

---

## 🔹 Step 4 — Install Python 3.11.9

```bash
pyenv install 3.11.9
pyenv global 3.11.9
```

Verify:

```bash
python --version
```

Expected output:

```
Python 3.11.9
```

---

## 🔹 Step 5 — Create Virtual Environment

```bash
pyenv virtualenv 3.11.9 yolo311
pyenv activate yolo311
```

Verify:

```bash
python --version
```

---

## 🔹 Step 6 — Upgrade pip

```bash
pip install --upgrade pip
pip install pydrive2
```

---

## 🔹 Step 7 — Install Required Packages

Make sure you are inside `(yolo311)` environment.

```bash
pip install numpy opencv-python onnxruntime
```

Notes:

- ❌ No torch
- ❌ No ultralytics
- ✅ Using ONNX Runtime directly

---

# 📂 Project Setup

---

## 🔹 Step 8 — Create Project Folder

```bash
cd ~
mkdir project
cd project
```

---

## 🔹 Step 9 — Clone Repository

```bash
git clone https://github.com/vizarrd/Edge_AI_Based_Road_Anomaly_Detection_using_raspberrypi.git
cd Edge_AI_Based_Road_Anomaly_Detection_using_raspberrypi
```

Files included:

- detect_ai.py  
- best_dynamic_int8.onnx  
- best.pt  
- gps_module.py  

---

# ▶️ Running the Project

Ensure virtual environment is active:

```bash
pyenv activate yolo311
```

Run:

```bash
python detect_ai.py
```

Press:

```
q
```

To exit the detection window.

---

# 📁 Output Structure

After detection:

```
project/
│
├── pothole/
│   ├── pothole_YYYYMMDDHHMMSS.avi
│
├── obstacle/
│   ├── obstacle_YYYYMMDDHHMMSS.avi
│
├── pothole_detection.txt
```

---

# 📍 GPS-Based Intelligent Logging (Novel Feature)

Whenever a pothole is detected:

- GPS coordinates are fetched
- A new log entry is created
- Data is stored in text format
- Google Maps link is generated
- Geo-fence check is performed

---

## Example Log Entry

```
Timestamp: 2025-02-10 14:22:31
Latitude: 12.9716
Longitude: 77.5945
Severity: HIGH
Confidence: 0.87
Google Maps: https://www.google.com/maps?q=12.9716,77.5945
---------------------------------
```

---

# 🗺 Geo-Fencing & Smart Upload System

The system defines:

- TARGET_LAT  
- TARGET_LON  
- UPLOAD_RADIUS (meters)  

When:

1. Pothole is detected  
2. Vehicle enters defined geographic radius  

Then the system automatically triggers:

```bash
python upload_script.py
```

This enables:

- Smart zone-based upload
- Reduced bandwidth usage
- Edge-to-cloud selective transmission

Upload is triggered only once per zone entry.

---

# 🧠 How The Complete System Works

1. Captures live camera feed  
2. Resizes frame to 640x640  
3. Runs ONNX inference on CPU  
4. Applies Non-Max Suppression  
5. Detects:
   - Class 0 → Obstacle
   - Class 1 → Pothole  
6. For potholes:
   - Calculates bounding box area
   - Classifies severity (LOW / MEDIUM / HIGH)
   - Fetches GPS coordinates
   - Logs event in text file
   - Generates Google Maps link
   - Checks geo-fence radius
   - Triggers upload if inside zone  
7. Saves detection video in respective folder  

All processing happens locally on Raspberry Pi.

---

# ⚙️ When You Need to Modify detect_ai.py

Normally no changes required.

Modify only in these cases:

---

## 🔹 If Model File Name Is Different

```bash
nano detect_ai.py
```

Find:

```python
MODEL_PATH = os.path.join(BASE_DIR, "best_dynamic_int8.onnx")
```

Replace with your model filename.

Save:

CTRL + X  
Y  
ENTER  

---

## 🔹 If Camera Not Detected

Find:

```python
cap = cv2.VideoCapture(0)
```

Change `0` to 1 or 2.

---

## 🔹 If GPS Target Location Needs Change

Find:

```python
TARGET_LAT = 12.971598
TARGET_LON = 77.594566
UPLOAD_RADIUS = 100
```

Replace with your required coordinates.

---

# 📊 Performance

- CPU-based inference
- INT8 optimized model
- Real-time edge deployment
- GPS-integrated anomaly tracking
- Geo-fenced smart upload
- No continuous cloud dependency
- Event-based intelligent logging

---

# 📦 Repository Files

| File | Description |
|------|------------|
| detect_ai.py | Main detection + GPS logic |
| gps_module.py | GPS integration module |
| best_dynamic_int8.onnx | Quantized YOLO model |
| best.pt | Trained PyTorch model |

---

# 🏆 Key Highlights

- Edge AI deployment on ARM platform
- Fully offline detection capability
- GPS-tagged pothole mapping
- Geo-fenced smart upload
- INT8 optimized inference
- Organized anomaly logging
- Competition-ready architecture

---

# ⛔ Exit Application

Press:

```
q
```

---

# 👨‍💻 Developed For

Bharat AI-SoC Student Challenge  
Edge AI Deployment on ARM Platforms  

---
