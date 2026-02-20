# 🚀 Edge AI Based Road Anomaly Detection using Raspberry Pi

## 📌 Project Overview

This project implements a **Real-Time Edge AI Road Anomaly Detection System** using Raspberry Pi.

It detects:
- 🕳️ Potholes
- 🚧 Obstacles

The system:
- Runs YOLO-based ONNX model on Raspberry Pi (CPU only)
- Shows live detection with timestamp
- Classifies pothole intensity (LOW / MEDIUM / HIGH)
- Automatically records detection videos
- Saves pothole and obstacle recordings in separate folders

---

# 🛠 Hardware Requirements

- Raspberry Pi 4 / Raspberry Pi 5
- Raspberry Pi OS (64-bit recommended)
- USB Camera or Pi Camera Module
- High-speed microSD card

---

# 💻 Software Requirements

- Python 3.9+
- OpenCV
- NumPy
- ONNX Runtime

---

# 🔧 Installation & Setup Guide

## Step 1️⃣ Update Raspberry Pi

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 2️⃣ Install Required Packages

```bash
sudo apt install python3-pip -y
pip3 install --upgrade pip
pip3 install opencv-python numpy onnxruntime
```

---

## Step 3️⃣ Create Project Folder

```bash
mkdir project
cd project
```

---

## Step 4️⃣ Clone Repository

```bash
git clone https://github.com/vizarrd/Edge_AI_Based_Road_Anomaly_Detection_using_raspberrypi.git
```

Then enter the folder:

```bash
cd Edge_AI_Based_Road_Anomaly_Detection_using_raspberrypi
```

This downloads:
- detect_ai.py
- best_dynamic_int8.onnx
- best.pt

---

# ▶️ Run the Project

```bash
python3 detect_ai.py
```

Press **q** to exit the application.

---

# 📁 Output Folders

After detection:

- pothole/ → contains pothole detection recordings
- obstacle/ → contains obstacle detection recordings

Each video is timestamped automatically.

---

# 🧠 How It Works

1. Camera captures live video.
2. Frame is resized and preprocessed.
3. ONNX model performs CPU inference.
4. If detected:
   - Class 0 → Obstacle
   - Class 1 → Pothole
5. Pothole intensity is classified:
   - LOW
   - MEDIUM
   - HIGH
6. Video is recorded using real-time FPS (natural playback, no fast video).

---

# ⚙️ When You Need to Modify detect_ai.py

Normally, no modification is required.

Modify only in the following cases:

---

## 🔹 Case 1: Model File Name is Different

If your model file is not named:

```
best_dynamic_int8.onnx
```

Then edit:

```bash
nano detect_ai.py
```

Find:

```python
MODEL_PATH = os.path.join(BASE_DIR, "best_dynamic_int8.onnx")
```

Replace with your model filename.

Save and exit:

```
CTRL + X
Y
ENTER
```

---

## 🔹 Case 2: Camera Not Detected

If camera does not open, edit:

```bash
nano detect_ai.py
```

Find:

```python
cap = cv2.VideoCapture(0)
```

Change `0` to:
- 1
- 2
- etc.

Save and exit.

---

## 🔹 Case 3: Adjust Detection Confidence

Find:

```python
CONF_THRESHOLD = 0.4
```

Increase value (e.g., 0.5) to reduce false positives.

---

# 📊 Performance

- CPU-based inference
- Optimized INT8 ONNX model
- Real-time detection
- Natural speed recording
- Separate logging for pothole & obstacle

---

# 📂 Repository Files

| File | Description |
|------|------------|
| detect_ai.py | Main detection script |
| best_dynamic_int8.onnx | Quantized YOLO model |
| best.pt | Trained model |

---

# 🏆 Key Features

- Edge AI based
- No cloud dependency
- Low power deployment
- Timestamp overlay
- Intensity classification
- Automatic video logging
- Folder-wise event storage

---

# ⛔ Exit Application

Press:

```
q
```

To close the detection window.

---

# 👨‍💻 Developed For

Bharat AI-SoC Student Challenge  
Edge AI Deployment on ARM Platforms  

---

If you are cloning this project for the first time, make sure your repository visibility is set to:

Public

Copy your repository link and submit it in the Project Submission Form.
