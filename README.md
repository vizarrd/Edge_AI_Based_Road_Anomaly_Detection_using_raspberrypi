# 🚀 Edge AI Based Road Anomaly Detection using Raspberry Pi

---

## 📌 Project Overview

This project implements a **Real-Time Edge AI Road Anomaly Detection System** deployed on a Raspberry Pi.

The system detects:

- 🕳️ Potholes
- 🚧 Obstacles

Features:

- ONNX optimized YOLO model (INT8)
- CPU-only inference (no GPU required)
- Real-time camera processing
- Timestamp overlay
- Pothole intensity classification (LOW / MEDIUM / HIGH)
- Automatic video logging
- Separate folders for pothole and obstacle events
- Natural playback speed recording

This solution is designed for **edge deployment on ARM-based systems**.

---

# 🛠 Hardware Requirements

- Raspberry Pi 4 / Raspberry Pi 5
- Raspberry Pi OS (64-bit recommended)
- USB Camera or Pi Camera Module
- High-speed microSD card (recommended: Class 10+)

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

## 🔹 Step 2 — Install Build Dependencies (Required for pyenv)

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

Expected:

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

Make sure you are inside `(yolo311)`.

```bash
pip install numpy opencv-python onnxruntime
```

Note:

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
```

Each detection is automatically logged.

---

# 🧠 How The System Works

1. Captures live camera feed.
2. Resizes frame to 640x640.
3. Runs ONNX inference on CPU.
4. Applies Non-Max Suppression.
5. Detects:
   - Class 0 → Obstacle
   - Class 1 → Pothole
6. For potholes:
   - Calculates bounding box area
   - Classifies intensity:
     - LOW
     - MEDIUM
     - HIGH
7. Saves detection video with real-time FPS.

---

# ⚙️ When You Need to Modify detect_ai.py

Normally, no changes required.

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

```
CTRL + X
Y
ENTER
```

---

## 🔹 If Camera Not Detected

Edit:

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

## 🔹 If You Want Higher Detection Strictness

Find:

```python
CONF_THRESHOLD = 0.4
```

Increase to 0.5 or 0.6.

---

# 📊 Performance

- CPU-based inference
- INT8 optimized model
- Real-time edge deployment
- No cloud dependency
- Automatic logging
- Separate anomaly classification

---

# 📦 Repository Files

| File | Description |
|------|------------|
| detect_ai.py | Main detection script |
| best_dynamic_int8.onnx | Quantized YOLO model |
| best.pt | Trained PyTorch model |

---

# 🏆 Key Highlights

- Edge AI deployment on ARM platform
- Optimized for Raspberry Pi
- Quantized model for performance
- Clean Python virtual environment
- Natural-speed recording
- Organized anomaly logging

---

# ⛔ Exit Application

Press:

```
q
```

To stop the system.

---

# 👨‍💻 Developed For

Bharat AI-SoC Student Challenge  
Edge AI Deployment on ARM Platforms  

---


**Public**

Copy your repository link and paste it into the Project Submission Form.
