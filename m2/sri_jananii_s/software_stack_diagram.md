# Milestone 2: Edge Vision System Software Stack

**Milestone**: M2 Optimize  
**Task**: CPU vs accelerator + stack (Stack Diagram Section)  
**Marks Awarded**: Part of 2 / 2  

---

## 1. Edge Software Architecture Diagram

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       LAYER 6: APPLICATION & UI                             │
│  Flask Web Dashboard (dashboard.html) │ MQTT Publisher │ Modbus PLC Bridge  │
│  SQLite Audit Logger (inspection.db)   │ 6-LED Matrix   │ Servo Actuator     │
├─────────────────────────────────────────────────────────────────────────────┤
│                     LAYER 5: DECISION & CONTROL LOGIC                       │
│  Spatial Slot Partitioner (2x3 Grid)  │ Temporal Debounce Filter (N=3)      │
│  Fail-Safe State Machine Watchdog      │ Instantaneous & Smoothed FPS Engine │
├─────────────────────────────────────────────────────────────────────────────┤
│                   LAYER 4: MODEL INFERENCE & RUNTIMES                       │
│  Tencent NCNN (best2_ncnn_model)       │ TFLite Runtime (model_int8.tflite) │
│  ONNX Runtime (model.onnx)             │ PyTorch Backend (best2.pt)         │
├─────────────────────────────────────────────────────────────────────────────┤
│                  LAYER 3: COMPUTER VISION & ACCELERATION                    │
│  OpenCV 4.10.0 (V4L2 Ingestion, MOG2)  │ ARM NEON SIMD Vectorization        │
│  NumPy 2.2.4 (Tensor Transformation)   │ Linux lgpio / gpiozero Libs        │
├─────────────────────────────────────────────────────────────────────────────┤
│                     LAYER 2: OPERATING SYSTEM & DRIVERS                     │
│  Debian 12 Bookworm (64-bit aarch64, Linux Kernel 6.6.20+rpt-rpi-2712)     │
│  V4L2 Video Subsystem (/dev/video0)   │ I2C Driver (/dev/i2c-1)             │
│  PWM & GPIO Subsystem (/dev/gpiomem)   │ Systemd Process Supervisor         │
├─────────────────────────────────────────────────────────────────────────────┤
│                       LAYER 1: PHYSICAL HARDWARE                            │
│  Broadcom BCM2712 Quad Cortex-A76 @ 2.4 GHz │ VideoCore VII GPU @ 800 MHz   │
│  Logitech C270 HD Optical Camera       │ SG90 Micro Servo Conveyor Diverter │
│  Active IR Optical Proximity Sensor    │ MPU6050 6-DoF Vibration Sensor     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Layer-by-Layer Functional Flow

1. **Physical Hardware**:
   - Logitech C270 acquires raw optical photons; MPU6050 samples conveyor vibration; SG90 servo mechanically actuates product sorting.
2. **Operating System & Kernel Drivers**:
   - Linux V4L2 device nodes stream frames; I2C kernel modules communicate with vibration sensors; systemd manages supervisor watchdogs.
3. **Computer Vision & Hardware Acceleration**:
   - OpenCV decodes YUYV to BGR; ARM NEON 128-bit vector registers accelerate 2D convolution matrix products directly on Cortex-A76 cores.
4. **Model Runtimes**:
   - Quantized TFLite and NCNN models execute forward tensor graphs at batch size 1 with minimal memory allocation overhead.
5. **Decision & Control Logic**:
   - Evaluates bounding box coordinates into physical $2\times 3$ pill slots, applies 3-frame temporal voting to suppress false positives, and signals reject mechanisms.
6. **Application & UI**:
   - Multi-threaded Flask WSGI server distributes low-latency MJPEG video feeds, drives GPIO relays and LEDs, logs transactions to SQLite WAL, and connects to factory SCADA via MQTT and Modbus TCP.
