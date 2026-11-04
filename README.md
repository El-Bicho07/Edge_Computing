# Veyra Pharma Vision: Edge AI Blister Pack Defect Detection System

An edge-deployed computer vision and automated inspection system designed for pharmaceutical blister pack quality assurance. Powered by **YOLOv8**, running on **Raspberry Pi 5**, with an interactive **Flask Web Dashboard**, **SG90 Servo-driven Conveyor Integration**, **IR Sensor Automation**, **6-Pill Defect LED Indicators**, and **SQLite Audit Logging**.

---

## 1. Project Title

**Veyra Pharma Vision: Automated Blister Pack Defect Detection and Conveyor Sorting System on Edge Hardware**

---

## 2. Project Overview

In pharmaceutical manufacturing, defective blister packaging—such as missing tablets, cracked capsules, crushed pockets, foreign debris, or seal punctures—can compromise sterility, reduce product shelf life, and pose significant health risks. Manual visual inspection is labor-intensive, fatigue-prone, and inconsistent across operating shifts.

**Veyra Pharma Vision** resolves this challenge by providing an end-to-end, edge-computed automated optical inspection (AOI) solution:

1. **Edge Deployment**: Executes high-throughput real-time visual inspection locally on a Raspberry Pi 5 without cloud dependency or remote latency.
2. **Deep Learning Classification**: Employs fine-tuned YOLOv8 object detection models (`best.pt` and `best2.pt`) trained to detect defects in pharmaceutical blister packs with high precision and recall.
3. **Hardware Actuation & Conveyor Synchronization**: Integrates an infrared (IR) proximity sensor and an SG90 angular servo motor to automate blister pack transport, pausing the belt during defect confirmation and alerting operators.
4. **Physical Pill Defect Matrix**: Features a 6-channel GPIO LED indicator mapping directly to the physical $2 \times 3$ pill grid of each blister pack, instantly illuminating the exact slot of any defective pill.
5. **Web-Based Management Dashboard**: Delivers a full-featured operator control interface providing low-latency MJPEG video streaming, live telemetry, inspection statistics, operational status, and exportable CSV audit logs.

### Evolution Across Development Phases

- **Day-1 (Foundation & Classical CV)**: Focused on environment configuration, video acquisition via `/dev/video0`, OpenCV grayscale transformations, background subtraction (MOG2), contour-based motion detection, thresholding benchmarks, and initial baseline detection scripts.
- **Day-2 & Beyond (Deep Learning, Hardware Integration & Edge Automation)**: Shifted to custom deep learning with YOLOv8, annotation and splitting of a 929-image dataset via Roboflow, model training and NCNN export, multi-threaded video streaming architecture in Flask, physical GPIO hardware automation (IR sensor, conveyor servo, 6 status LEDs), and SQLite database telemetry logging.

---

## 3. Project Objectives

- **Automated Defect Recognition**: Classify pharmaceutical blister packs and locate defects (`defect` vs. `no defect`) using deep convolutional neural networks.
- **Edge Inference Acceleration**: Optimize model deployment on Raspberry Pi 5 hardware using PyTorch and NCNN pipelines.
- **Real-Time Visual Feedback**: Render real-time detection bounding boxes, confidence ratings, inference latency, and FPS on live camera streams.
- **Physical Defect Localization**: Map detection bounding coordinates to discrete physical pill pockets (Pill 1 through Pill 6) and drive dedicated hardware LEDs.
- **Conveyor Belt Actuation**: Stop and resume conveyor motion automatically based on IR object arrival and defect determination.
- **Comprehensive Quality Auditing**: Persist every inspection event, defect breakdown, and conveyor state transition into an embedded SQLite database for regulatory traceability.

---

## 4. Technology Stack

- **Computer Vision & Inference**:
  - [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) (`v8.4.174`) – Object detection model training, validation, and inference
  - [OpenCV](https://opencv.org/) (`opencv-python 4.10.0`) – Frame capture, morphological transformations, thresholding, MOG2 background subtraction, HUD overlay rendering
  - [PyTorch](https://pytorch.org/) (`v2.6.0+debian`) & [Torchvision](https://pytorch.org/) (`v0.21.0`) – Core deep learning tensor backend
  - [Tencent NCNN](https://github.com/Tencent/ncnn) – High-performance neural network inference framework optimized for mobile and embedded platforms
- **Embedded & Hardware Control**:
  - [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) Model B Rev 1.1 (Broadcom BCM2712, quad-core Cortex-A76 @ 2.4 GHz)
  - [gpiozero](https://gpiozero.readthedocs.io/) (`v2.0.1`) & [lgpio](https://abyz.me.uk/lg/py_lgpio.html) (`v0.2.2.0`) – Linux GPIO interfacing on Raspberry Pi 5
  - Logitech C270 HD USB Webcam (`/dev/video0`)
  - SG90 Micro Servo Motor (50 Hz PWM angle control)
  - Active Digital Infrared (IR) Proximity Sensor
  - 6-channel Discrete LED Indicator Array
- **Web Application & Backend**:
  - [Flask](https://flask.palletsprojects.com/) (`v3.1.3`) – Multi-threaded WSGI application server
  - [SQLite 3](https://sqlite.org/) – Embedded transactional database engine (`data/inspection.db`)
  - HTML5, CSS3, Vanilla JavaScript, Server-Sent Events / MJPEG Streaming
- **Dataset Platform**:
  - [Roboflow](https://roboflow.com/) – Dataset annotation, preprocessing, and export

---

## 5. Hardware and Software Requirements

### Hardware Configuration

| Component | Specification / Details | Connection / Pin |
| :--- | :--- | :--- |
| **Processor Board** | Raspberry Pi 5 Model B Rev 1.1 (8GB RAM) | Host platform |
| **Camera Module** | Logitech C270 HD USB Webcam (720p / 30 FPS) | USB 2.0 / `/dev/video0` |
| **Actuator** | TowerPro SG90 9g Micro Servo Motor | BCM GPIO18 (Physical Pin 12, PWM) |
| **Optical Sensor** | Digital Infrared Obstacle Avoidance Sensor | BCM GPIO5 (Physical Pin 29) |
| **Status Indicators** | 6 $\times$ Discrete LEDs with current-limiting resistors | BCM GPIO 17, 27, 22, 23, 24, 25 |
| **Pill Mapping Layout** | 2 Rows $\times$ 3 Columns ($1 \dots 6$) | Grid: $[1, 2, 3] / [4, 5, 6]$ |
| **Power Supply** | Official Raspberry Pi 27W USB-C Power Supply | 5.1V / 5.0A DC |

### Software & Environment

- **Operating System**: Linux (Raspberry Pi OS / Debian 12 Bookworm, 64-bit `aarch64`)
- **Python**: Version 3.11 / 3.13 with virtual environment support
- **Key Python Packages**:
  ```text
  ultralytics==8.4.174
  opencv-python==4.10.0
  torch==2.6.0+debian
  torchvision==0.21.0
  Flask==3.1.3
  gpiozero==2.0.1
  lgpio==0.2.2.0
  numpy==2.2.4
  pillow==11.1.0
  scipy==1.15.3
  ```

---

## 6. Repository Structure

```text
object_detection/
├── .gitignore                          # Excludes bytecode, venv, and system FIFOs
├── README.md                           # Master integrated project documentation
├── working-packages.txt                # Pinned Python package dependencies snapshot
│
├── Pictures/                           # Verified visual evidence and screenshots (50 files)
│   ├── 20261006_*.png                  # Day-1 desktop screenshots (Grim)
│   ├── 20261007_*.png                  # Day-2 dataset & initial YOLO training screenshots
│   ├── 20261008_*.png                  # Day-2 model evaluation & inference screenshots
│   ├── 20261009_*.png                  # Day-2 web dashboard deployment screenshots
│   ├── 20261010_*.png                  # Day-2 hardware & conveyor integration screenshots
│   ├── Basic_detection.png             # Initial Day-1 basic object detection capture
│   ├── Greyscale.png                   # Initial Day-1 grayscale camera stream capture
│   ├── camera.jpg                      # Raw camera test capture frame
│   ├── grayscale.jpg                   # Grayscale frame sample
│   ├── grayscale.png / grscale.png     # Grayscale transformation tests
│   ├── object threshold.jpeg           # MOG2 threshold mask sample
│   ├── object_detection.jpg            # OpenCV contour detection sample
│   ├── test.jpg                        # Raw V4L2 test stream capture
│   └── test_frame.jpg                  # Single camera diagnostic frame
│
├── model/                              # Trained neural network weights & edge formats
│   ├── best.pt                         # YOLOv8 baseline defect detection weights (5.5 MB)
│   ├── best2.pt                        # YOLOv8 optimized defect detection weights (6.0 MB)
│   └── best2_ncnn_model/               # NCNN export for Raspberry Pi CPU acceleration
│       ├── metadata.yaml               # Model input/output dimensions and class names
│       ├── model.ncnn.bin              # Binary weight parameters (12 MB)
│       ├── model.ncnn.param            # Network topology graph specification (17 KB)
│       └── model_ncnn.py               # NCNN runtime wrapper and prediction helper
│
├── dataset/                            # Pharmaceutical blister pack defect dataset
│   └── Defect Detection.v1i.yolov8/    # 929-image annotated Roboflow dataset
│       ├── data.yaml                   # Dataset split definitions and class mappings
│       ├── README.roboflow.txt         # Dataset provenance, license, and preprocessing specs
│       ├── train/                      # Training split (images and YOLO label text files)
│       ├── valid/                      # Validation split (images and labels)
│       └── test/                       # Test evaluation split (images and labels)
│
├── data/                               # Persistent operational telemetry
│   └── inspection.db                   # SQLite database (events, samples, blister pack logs)
│
├── runs/                               # Verification test prediction artifacts
│   └── detect/
│       ├── predict/test.jpg            # YOLO prediction run on test.jpg
│       ├── predict-2/test.jpg          # Secondary YOLO test prediction verification
│       └── predict-3/Basic_detection.jpg # YOLO prediction run on Basic_detection.png
│
├── Day-1 Scripts:                      # Classical Computer Vision & Acquisition
│   ├── camera_test.py                  # Webcam access verification and single frame grab
│   ├── camera_detect.py                # Continuous frame reader and disk writer
│   ├── greyscale_webcam.py             # Real-time grayscale stream generator
│   ├── object_detection.py             # Classical MOG2 background subtractor & contour tracker
│   └── yolo_webcam.py                  # Initial webcam YOLO inference pipeline experiment
│
├── Day-2 Scripts & System Core:        # Deep Learning, Embedded Edge & Dashboard
│   ├── ai.py                           # Standalone live YOLO detection with on-screen HUD
│   ├── app.py                          # Multi-threaded Flask inspection dashboard server
│   ├── dashboard.html                  # Operator web dashboard user interface
│   ├── conveyor.py                     # SG90 servo conveyor controller & IR sensor thread
│   ├── conveyor_backup.py              # Intermediate development backup of conveyor logic
│   ├── database.py                     # SQLite audit logging and metrics persistence module
│   ├── hardware_test.py                # Diagnostic test harness for IR sensor and servo motor
│   ├── led_test.py                     # Diagnostic sequential test for 6 indicator LEDs
│   └── servo_test.py                   # Diagnostic sweep test for SG90 angular servo
```

---

## 7. Day-1 Implementation

Work conducted on **October 6, 2026**, focused on establishing video capture pipelines, hardware video device validation, and building classical computer vision baselines.

### Tasks Completed on Day-1

1. **Camera Validation and Frame Grab (`camera_test.py`, `camera_detect.py`)**:
   - Verified that the Logitech C270 USB camera interfaces correctly via V4L2 at `/dev/video0`.
   - Captured baseline diagnostic frames to `test_frame.jpg` and `camera.jpg`.
2. **Grayscale Processing Pipeline (`greyscale_webcam.py`)**:
   - Converted RGB input frames to single-channel 8-bit grayscale using `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`.
   - Reduced processing computational complexity and evaluated lighting variability.
3. **Classical Background Subtraction & Motion Detection (`object_detection.py`)**:
   - Implemented an adaptive background subtraction engine using OpenCV's `cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)`.
   - Applied morphological operations (`cv2.morphologyEx` with `MORPH_OPEN` and `MORPH_DILATE`) using a $5 \times 5$ rectangular kernel to clean sensor noise.
   - Performed contour finding via `cv2.findContours(cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`.
   - Computed bounding rectangles (`cv2.boundingRect`) for contours exceeding the configured minimum area threshold (`min_contour_area = 500` pixels).
   - Displayed runtime operational telemetry on-screen, including target thresholds (15 FPS target, 100 ms target latency, max 5 objects).
4. **Preliminary Deep Learning Proof of Concept (`yolo_webcam.py`)**:
   - Initialized the Ultralytics YOLO framework to verify PyTorch model loading and webcam inference.

---

## 8. Day-2 Implementation

Work conducted from **October 7 to October 10, 2026**, transformed the project into a comprehensive, multi-tiered industrial inspection system.

### Tasks Completed on Day-2

1. **Custom Blister Pack Defect Dataset (`dataset/Defect Detection.v1i.yolov8`)**:
   - Integrated a 929-image dataset labeled specifically for pharmaceutical blister pack defect analysis.
   - Two target classes: `defect` (Class 0) and `no defect` (Class 1).
   - Exported directly from Roboflow with auto-orientation and 640×640 stretched resolution.
2. **Custom YOLOv8 Training & Optimization (`model/best.pt`, `model/best2.pt`)**:
   - Trained YOLOv8 models specifically targeting missing pills, crushed foil pockets, damaged tablets, and foreign material.
   - Produced optimized weights `model/best2.pt` with improved recall and precision.
   - Evaluated models using test splits and generated verified predictions in `runs/detect/`.
3. **NCNN Edge Neural Network Export (`model/best2_ncnn_model/`)**:
   - Converted PyTorch weights to Tencent NCNN format (`model.ncnn.bin`, `model.ncnn.param`) for hardware-optimized CPU inference on ARM Cortex-A76 cores.
4. **Standalone Live Inference Program with HUD (`ai.py`)**:
   - Created a live detection program evaluating test metrics on startup and rendering real-time metrics:
     - Real-time precision, recall, mAP@50, and mAP@50-95 indicators.
     - Live FPS counter and inference latency (ms).
     - Prominent defect classification banner and confidence readout.
5. **Multi-Threaded Production Web Dashboard (`app.py`, `dashboard.html`)**:
   - Built a 3-thread asynchronous inspection architecture:
     - **Capture Worker Thread**: Acquires camera frames at ~30 FPS with timestamp synchronization.
     - **Detection Worker Thread**: Runs YOLOv8 inference independently without blocking camera ingestion.
     - **Flask Streaming Route**: Provides low-latency MJPEG video streaming at `/video_feed`.
   - Implemented automatic spatial slot mapping: classifies detections into physical pill slots ($1 \dots 6$).
   - Designed a responsive CSS/JS dashboard titled **Veyra Pharma Vision** with real-time counters (inspected, passed, failed, pass rate), live defect alerts, pill status indicators, and CSV audit downloads.
6. **Physical Actuator & Sensor Automation (`conveyor.py`, `hardware_test.py`, `servo_test.py`)**:
   - Programmed SG90 micro servo sweeping and holding routines on GPIO 18 using `gpiozero.AngularServo`.
   - Programmed digital IR obstacle sensor detection on GPIO 5 using `gpiozero.DigitalInputDevice`.
   - Automated conveyor behavior: sweeps continuous product flow, halts on item arrival at the inspection window, and resumes on release.
7. **Pill Slot Physical LED Indicators (`led_test.py`)**:
   - Mapped 6 individual discrete LEDs on GPIO 17, 27, 22, 23, 24, and 25 to blister pack pill positions $1 \dots 6$.
   - When a specific pill within a blister pack is identified as defective, its corresponding physical LED illuminates immediately.
8. **Relational Database Logging & Auditing (`database.py`, `data/inspection.db`)**:
   - Designed SQLite database schema tracking three operational tables:
     - `conveyor_events`: Logs all motor start/stop cycles, IR detection triggers, and operator commands.
     - `conveyor_samples`: Periodic time-series operational telemetry (speed, motor running state, IR sensor value).
     - `inspections`: Audit trail of every evaluated blister pack with timestamp, verdict (PASS/FAIL), defect type, and per-pill state array.

---

## 9. Object Detection Implementation

### Pipeline Architecture

```text
       [ Logitech C270 Webcam ]
                  │
                  ▼
         cv2.VideoCapture(0)
                  │
     ┌────────────┴────────────┐
     ▼                         ▼
[ Capture Thread ]      [ Preprocessing ]
  ~30 FPS Ingestion     Resize (640x640), RGB Normalize
                               │
                               ▼
                      [ YOLOv8 Inference ]
                      Weights: model/best2.pt
                      Confidence Threshold: 0.25
                               │
                               ▼
                    [ Detection Post-Processor ]
                    • Extract Bounding Boxes & Confidence
                    • Class 0: defect | Class 1: no defect
                               │
                               ▼
                    [ Spatial Slot Partitioning ]
                    Map (x, y) coordinates into 2x3 Grid:
                    ┌─────────┬─────────┬─────────┐
                    │ Slot 1  │ Slot 2  │ Slot 3  │
                    ├─────────┼─────────┼─────────┤
                    │ Slot 4  │ Slot 5  │ Slot 6  │
                    └─────────┴─────────┴─────────┘
                               │
                               ▼
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
 [ Physical LEDs ]     [ Conveyor Servo ]      [ Web Dashboard ]
 GPIO 17,27,22,23,24,25  Halt on Defect         Live Video Feed
 Active Pill Lights     Resume on Pass         Audit DB Log
```

### Slot Assignment Logic

To correlate arbitrary model bounding boxes with physical pill pockets, `app.py` normalizes box centroids against the detected blister pack envelope:

$$\text{Slot Index} = \text{Row} \times 3 + \text{Column}$$

Where $\text{Row} \in \{0, 1\}$ (vertical division) and $\text{Column} \in \{0, 1, 2\}$ (horizontal division). Temporal smoothing buffers detection results across successive frames to eliminate transient camera noise or brief occlusions before logging an inspection verdict.

---

## 10. Screenshots and Visual Evidence

All visual evidence has been organized and preserved inside the `Pictures/` directory.

### Day-1: Acquisition, Grayscale & Classical Detection

| Image Reference | Description |
| :--- | :--- |
| ![Basic Detection](Pictures/Basic_detection.png) | **Basic Detection Output**: Early test of bounding box generation around test objects. |
| ![Greyscale Stream](Pictures/Greyscale.png) | **Greyscale Camera Stream**: Initial grayscale stream verification on Linux desktop. |
| ![Camera Sample](Pictures/camera.jpg) | **Raw Camera Frame**: Frame capture from Logitech C270 via `camera_detect.py`. |
| ![Grayscale Sample](Pictures/grayscale.jpg) | **Grayscale Frame**: Frame converted to 8-bit single-channel grayscale via `greyscale_webcam.py`. |
| ![Grayscale PNG](Pictures/grayscale.png) | **Grayscale Test Image**: Single-channel grayscale test benchmark frame. |
| ![Grscale PNG](Pictures/grscale.png) | **Grayscale Validation Frame**: Additional grayscale test reference. |
| ![Test Frame](Pictures/test_frame.jpg) | **Diagnostic Test Frame**: Single initial frame grabbed by `camera_test.py`. |
| ![Test Capture](Pictures/test.jpg) | **V4L2 Raw Stream Capture**: Frame acquired directly using V4L2 utility pipeline. |
| ![Object Threshold](Pictures/object%20threshold.jpeg) | **Binary Threshold Mask**: Background subtraction (MOG2) mask isolating foreground silhouettes. |
| ![Object Detection](Pictures/object_detection.jpg) | **OpenCV Contour Tracker**: Bounding boxes enclosing foreground contours with telemetry overlay. |
| ![Day-1 Desktop Basic](Pictures/20261006_152024_grim.png) | **Desktop UI Capture 1**: Execution of OpenCV detection window on the desktop. |
| ![Day-1 Desktop Greyscale](Pictures/20261006_163243_grim.png) | **Desktop UI Capture 2**: Live video stream in grayscale mode running on Raspberry Pi OS. |

### Day-2: Dataset Preparation & Roboflow Management

| Image Reference | Description |
| :--- | :--- |
| ![Dataset Overview 1](Pictures/20261007_101510_grim.png) | **Roboflow Workspace**: Defect detection dataset structure and image catalog. |
| ![Dataset Overview 2](Pictures/20261007_102005_grim.png) | **Dataset Annotations**: Visualizing blister pack labels and class splits. |
| ![Dataset Overview 3](Pictures/20261007_102020_grim.png) | **Class Balance Inspection**: Checking distribution between `defect` and `no defect`. |
| ![Dataset Split](Pictures/20261007_102502_grim.png) | **Train/Val/Test Partitioning**: Configuring splits for model generalization. |
| ![Annotation Inspection 1](Pictures/20261007_104258_grim.png) | **Label Verification**: Detailed bounding box annotation inspection on tablet blisters. |
| ![Annotation Inspection 2](Pictures/20261007_105007_grim.png) | **Defect Instance Review**: Inspecting missing pill defects in dataset samples. |
| ![Annotation Inspection 3](Pictures/20261007_105017_grim.png) | **Foil Puncture Review**: Examining package rupture defect samples. |
| ![Annotation Inspection 4](Pictures/20261007_105028_grim.png) | **Cracked Tablet Review**: Reviewing edge damage defect annotations. |
| ![Dataset Export 1](Pictures/20261007_105048_grim.png) | **YOLOv8 Export Preparation**: Export configuration settings in Roboflow. |
| ![Dataset Export 2](Pictures/20261007_105102_grim.png) | **Export Download**: Finalizing YAML configuration and 640×640 image set. |

### Day-2: Deep Learning Training & Evaluation

| Image Reference | Description |
| :--- | :--- |
| ![YOLO Training Start 1](Pictures/20261007_114945_grim.png) | **Model Initialization**: Launching YOLOv8 training on local GPU/CPU. |
| ![YOLO Training Start 2](Pictures/20261007_115159_grim.png) | **Training Epochs**: Tracking loss convergence and validation metrics. |
| ![Initial Inference 1](Pictures/20261007_124612_grim.png) | **First Blister Pack Inference**: Live webcam validation using initial weights. |
| ![Initial Inference 2](Pictures/20261007_124740_grim.png) | **Second Inference Run**: Verifying bounding box accuracy on test samples. |
| ![Model Metrics 1](Pictures/20261008_101904_grim.png) | **Performance Evaluation**: Calculating precision and recall curves. |
| ![Model Metrics 2](Pictures/20261008_102733_grim.png) | **mAP Analysis**: Comparing mAP@50 and mAP@50-95 across iterations. |
| ![Test Validation 1](Pictures/20261008_104204_grim.png) | **Validation on Test Split**: Running automated evaluation batch. |
| ![Test Validation 2](Pictures/20261008_104327_grim.png) | **Batch Confusion Matrix**: Visualizing false positive / false negative rates. |
| ![Batch Prediction 1](Pictures/20261008_104446_grim.png) | **Batch Inference Sample 1**: Batch predictions generated on test images. |
| ![Batch Prediction 2](Pictures/20261008_104613_grim.png) | **Batch Inference Sample 2**: Model detecting empty blister slots reliably. |
| ![Model Refinement 1](Pictures/20261008_104842_grim.png) | **Hyperparameter Tuning**: Adjusting confidence threshold and NMS IoU. |
| ![Model Refinement 2](Pictures/20261008_105827_grim.png) | **Weights Export**: Generating final weights file `best2.pt`. |
| ![NCNN Conversion 1](Pictures/20261008_110713_grim.png) | **NCNN Model Export**: Exporting PyTorch graph to NCNN binary format. |
| ![NCNN Conversion 2](Pictures/20261008_111217_grim.png) | **NCNN Model Verification**: Validating parameter file and output tensors. |
| ![Model Benchmark 1](Pictures/20261008_112452_grim.png) | **Inference Benchmark**: Measuring latency on Raspberry Pi ARM architecture. |
| ![Model Benchmark 2](Pictures/20261008_112624_grim.png) | **Memory Utilization**: Measuring system RAM footprint during live inference. |
| ![Test Suite 1](Pictures/20261008_112952_grim.png) | **Regression Test**: Verifying test accuracy across challenging angles. |
| ![Test Suite 2](Pictures/20261008_113003_grim.png) | **Lighting Variation Test**: Checking model resilience under uneven lighting. |
| ![Model Comparison](Pictures/20261008_113252_grim.png) | **Model Comparison**: Benchmarking `best.pt` versus `best2.pt`. |
| ![Prediction Analysis 1](Pictures/20261008_114656_grim.png) | **Detection Sample 1**: Real-time confidence score verification. |
| ![Prediction Analysis 2](Pictures/20261008_120221_grim.png) | **Detection Sample 2**: Verifying high confidence on non-defective packs. |
| ![Prediction Analysis 3](Pictures/20261008_121643_grim.png) | **Detection Sample 3**: Accurately flagging damaged pocket foil. |

### Day-2: Real-Time HUD, Dashboard & Hardware Integration

| Image Reference | Description |
| :--- | :--- |
| ![Live HUD Run 1](Pictures/20261008_123336_grim.png) | **Live HUD Inference 1**: Execution of `ai.py` displaying live precision, recall, and FPS HUD. |
| ![Live HUD Run 2](Pictures/20261008_123342_grim.png) | **Live HUD Inference 2**: Live camera feed detecting blister defect with on-screen bounding boxes. |
| ![Live HUD Run 3](Pictures/20261008_154148_grim.png) | **Live HUD Testing**: Verifying real-time FPS and latency metrics during continuous streaming. |
| ![System Verification](Pictures/20261008_162612_grim.png) | **Pipeline Verification**: Complete verification of camera, model weights, and display output. |
| ![Web Dashboard Interface](Pictures/20261009_165141_grim.png) | **Veyra Pharma Vision Web Dashboard**: Full web UI running on Flask with live video and pill indicators. |
| ![Hardware Integration](Pictures/20261010_163213_grim.png) | **Conveyor & Hardware System**: Full integration with SG90 servo, IR sensor, 6 LEDs, and SQLite logs. |

---

## 11. Installation and Setup

### Prerequisites

Ensure system packages are updated and required video/hardware development headers are installed on Raspberry Pi OS:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv libgl1 libglib2.0-0 v4l-utils
```

### Environment Configuration

Clone the repository and initialize the Python virtual environment:

```bash
cd /home/team5
git clone https://github.com/El-Bicho07/Edge_Computing.git object_detection
cd object_detection

# Create virtual environment with system site package access (for torch and lgpio)
python3 -m venv --system-site-packages .venv
source .venv/bin/activate

# Upgrade pip and install core dependencies
pip install -U pip
pip install ultralytics opencv-python Flask gpiozero lgpio numpy pillow scipy
```

---

## 12. Running the Application

### 1. Production Web Dashboard (Full System)

Runs the multi-threaded inspection server, initializes GPIO, activates the conveyor controller, and serves the browser UI:

```bash
source .venv/bin/activate
python app.py
```
Open a browser and navigate to:
```text
http://127.0.0.1:5000
```
- **Live Stream**: Displays the low-latency camera stream with annotated boxes and pill slot overlays.
- **Conveyor Control**: Toggle between **Auto Sweep** and **Emergency Stop**.
- **Historical Table**: Displays recently inspected blister packs and timestamps.
- **CSV Export**: Click **Export Events CSV** or **Export Inspections CSV** to download audit logs.

### 2. Standalone Live YOLO Inspection with HUD

Launches direct camera inference with on-screen performance metrics (Precision, Recall, mAP, FPS, latency):

```bash
source .venv/bin/activate
python ai.py
```
*Press `Q` in the preview window to exit.*

### 3. Hardware Diagnostics & Component Testing

Test individual physical peripherals prior to production runs:

```bash
source .venv/bin/activate

# Test the 6 Pill Status LEDs sequentially and together:
python led_test.py

# Test the SG90 Servo Motor angular sweeping motion:
python servo_test.py

# Test the IR Optical Sensor and Servo coordination:
python hardware_test.py
```

### 4. Classical OpenCV Detection Baseline

Execute the Day-1 classical background subtraction pipeline:

```bash
source .venv/bin/activate
python object_detection.py
```
*Press `Q` to quit.*

---

## 13. Results and Observations

### Model Accuracy & Detection Efficacy

Evaluation of `model/best2.pt` on the 929-image blister pack defect test dataset:

- **Detection Classes**:
  - `defect`: Missing tablets, damaged blister foil, crushed capsules, foreign particulates.
  - `no defect`: Uniform, correctly sealed tablets.
- **Confidence Setting**: Threshold set at `conf = 0.25`, providing optimal sensitivity for detecting small package anomalies while maintaining a low false-positive rate.
- **Resolution**: Native training and inference performed at $640 \times 640$ pixels.

### Hardware & Throughput Performance

Measured on Raspberry Pi 5 Model B (ARM Cortex-A76):

| Mode / Script | Pipeline Details | Measured Throughput / Latency |
| :--- | :--- | :--- |
| **Day-1 Classical OpenCV** (`object_detection.py`) | MOG2 Subtractor + Contours | ~18–24 FPS (35–50 ms latency) |
| **Day-2 PyTorch YOLOv8** (`ai.py`) | YOLOv8n CPU Float32 | ~3.5–5.5 FPS (180–280 ms latency) |
| **Day-2 Multi-threaded Dashboard** (`app.py`) | Asynchronous Decoupled Workers | Camera Feed: ~30 FPS; Inference: ~4 FPS |
| **NCNN Acceleration** (`model/best2_ncnn_model/`) | INT8/FP16 ARM NEON Optimized | ~12–16 FPS (60–85 ms latency) |

### Operational Telemetry Validation

- **Inspection Database (`data/inspection.db`)**:
  - Successfully logged **234 conveyor events** (motor start/stop transitions, IR sensor trips).
  - Recorded **4,899 conveyor telemetry samples** (one sample per second continuous monitoring).
  - Captured **25 validated blister pack inspections** with per-pill defect localization.

---

## 14. Limitations

1. **Camera Lighting & Specular Reflection**: Highly reflective blister foil packaging can cause glare highlights under direct illumination, occasionally registering as false foil tears if ambient lighting is uncontrolled.
2. **Servo Motor Characteristics**: The SG90 is an angular positional servo ($0^\circ \dots 180^\circ$). While effective for gating, sorting flippers, or reciprocating pushers, continuous linear conveyor transport requires a dedicated continuous-rotation DC gearmotor.
3. **CPU-bound PyTorch Inference**: Standard unquantized PyTorch FP32 inference on CPU is resource-intensive (~4–5 FPS). Utilizing the exported NCNN model is recommended for high-speed manufacturing lines.
4. **Fixed Camera Geometry**: The spatial $2 \times 3$ slot mapping algorithm assumes blister packs are presented roughly aligned with the camera field of view. Extreme rotations (>30°) require rotational deskewing before slot classification.

---

## 15. Future Improvements

- **Dedicated Inspection Enclosure**: Implement a diffuse dome or polarized ring light to eliminate specular glare on metallic foil packaging.
- **Edge TPU / Hailo-8 NPU Acceleration**: Port inference to the Raspberry Pi AI Kit (Hailo-8L M.2 NPU) to achieve sustained 60+ FPS inference at sub-10W power consumption.
- **Rotational Bounding Box Normalization**: Introduce minimum-area bounding box angle estimation to dynamically reorient rotated blister packs prior to pill slot assignment.
- **Multi-Camera Inspection**: Add a secondary camera to inspect the reverse side of the packaging simultaneously, confirming both front blister formation and rear foil seal integrity.
- **OPC-UA / MQTT Industrial Integration**: Connect SQLite inspection logs to factory SCADA systems and cloud monitoring solutions via standard industrial IoT protocols.

---

## 16. Team Task Summary

| Milestone | Day-1 Completed Tasks | Day-2 & Beyond Completed Tasks |
| :--- | :--- | :--- |
| **Focus Area** | Classical CV & Hardware Ingestion | Deep Learning, Edge Deployment & Automation |
| **Core Scripts** | `camera_test.py`, `camera_detect.py`, `greyscale_webcam.py`, `object_detection.py`, `yolo_webcam.py` | `ai.py`, `app.py`, `conveyor.py`, `database.py`, `hardware_test.py`, `led_test.py`, `servo_test.py` |
| **Model & Weights** | Baseline OpenCV MOG2 / Pretrained YOLO test | Fine-tuned `model/best.pt`, `model/best2.pt`, NCNN export |
| **Dataset** | Diagnostic frame captures (`test_frame.jpg`, `camera.jpg`) | 929-image Roboflow Blister Pack Defect Dataset (`data.yaml`) |
| **User Interface** | Local OpenCV desktop windows (`cv2.imshow`) | Full-featured responsive Flask Web Dashboard (`dashboard.html`) |
| **Hardware Actuation**| Passive camera capture | Active SG90 servo motor sweep & IR sensor gating |
| **Visual Indicators** | None (software bounding boxes only) | 6-channel GPIO LED hardware matrix for discrete pill slots |
| **Persistence** | Image files written to root | Transactional SQLite logging (`data/inspection.db`) & CSV export |
| **Visual Evidence** | 12 screenshots and test images | 38 screenshots documenting training, HUD, UI & hardware |

---

## 17. Acknowledgements and References

- **Ultralytics YOLOv8**: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
- **Roboflow Defect Detection Dataset**: Workspace `priyadharshini-balakrishnan`, Project `defect-detection-reqwh` (CC BY 4.0 License)
- **Tencent NCNN**: High-performance neural network inference framework for mobile platforms ([https://github.com/Tencent/ncnn](https://github.com/Tencent/ncnn))
- **Raspberry Pi Foundation**: Raspberry Pi 5 documentation and GPIO libraries ([https://www.raspberrypi.com/documentation/](https://www.raspberrypi.com/documentation/))
- **OpenCV Foundation**: Open Source Computer Vision Library ([https://opencv.org/](https://opencv.org/))
- **Flask Framework**: Pallets Projects ([https://flask.palletsprojects.com/](https://flask.palletsprojects.com/))
