# Milestone 5: End-to-End System Architecture Diagram

**Milestone**: M5 Complete System + Dashboard  
**Task**: Documents  
**Rubric Weight**: Part of 1 Marks  

---

## 1. Complete Cyber-Physical System Architecture

```text
                                  PHYSICAL CONVEYOR RIG
                      ┌───────────────────────────────────────────┐
                      │  [ 5500K Polarized LED Ring Illuminator ] │
                      │                     │                     │
                      │                     ▼                     │
                      │         [ Logitech C270 Webcam ]          │
                      │                     │                     │
                      │                     │ USB 2.0 (/dev/video0)
                      │                     ▼                     │
                      │          ═══════════════════════          │
                      │          [ Blister Pack Stream ]          │
                      │          ═══════════════════════          │
                      │               │               ▲           │
                      │   [IR Beam]   │               │ [Diverter]│
                      │       ▼       │               │           │
                      │   [IR Sensor] │        [ SG90 Servo Gate ]│
                      │   (GPIO 5)    │           (GPIO 18 PWM)   │
                      │               │                           │
                      │     [ Conveyor Drive Motor ]              │
                      │               │                           │
                      │     [ MPU6050 I2C Sensor ]                │
                      │     (SDA GPIO2, SCL GPIO3)                │
                      └───────────────┼───────────────────────────┘
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            │                                                   │
            ▼                                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│              RASPBERRY PI 5 EDGE COMPUTE ENGINE (Debian 12 aarch64)              │
│                                                                                  │
│   ┌───────────────────────────┐           ┌──────────────────────────────────┐   │
│   │ CAMERA INGESTION WORKER   │           │ MPU6050 VIBRATION WORKER         │   │
│   │ V4L2 Thread @ 30 FPS      │           │ I2C Thread @ 50 Hz               │   │
│   │ Bounded 1-Frame Buffer    │           │ Continuous Feature Extraction    │   │
│   └─────────────┬─────────────┘           └─────────────────┬────────────────┘   │
│                 │                                           │                    │
│                 ▼                                           ▼                    │
│   ┌───────────────────────────┐           ┌──────────────────────────────────┐   │
│   │ YOLOv8 INFERENCE ENGINE   │           │ ANOMALY DETECTION ENGINE         │   │
│   │ INT8 Quantized (TFLite)   │           │ 3.5-Sigma Mahalanobis Envelope   │   │
│   │ Latency: 40.1 ms          │           │ Alert Cutoff: Score >= 4.285     │   │
│   └─────────────┬─────────────┘           └─────────────────┬────────────────┘   │
│                 │                                           │                    │
│                 ▼                                           │                    │
│   ┌───────────────────────────┐                             │                    │
│   │ DECISION & ACTUATOR LOGIC │                             │                    │
│   │ Spatial 2x3 Slot Grid     │                             │                    │
│   │ Temporal Debounce (N=3)   │                             │                    │
│   │ Fail-Safe Heartbeat Watch │                             │                    │
│   └─────────────┬─────────────┘                             │                    │
│                 │                                           │                    │
│                 ├─────────────────────┐                     │                    │
│                 ▼                     ▼                     ▼                    │
│   ┌────────────────────────┐  ┌──────────────────────────────────────────────┐   │
│   │ HARDWARE ACTUATION     │  │ FACTORY INTEGRATION & LOGGING                │   │
│   │ • Relay Stop (GPIO 14) │  │ • SQLite WAL Database (data/inspection.db)   │   │
│   │ • Reject Servo (GPIO18)│  │ • Modbus TCP Server (PLC Registers: 40001..) │   │
│   │ • 6 Defect LEDs        │  │ • Secure MQTT TLS Publisher (Port 8883)      │   │
│   └────────────────────────┘  └─────────────────────┬────────────────────────┘   │
└─────────────────────────────────────────────────────┼────────────────────────────┘
                                                      │
                                                      ▼
                                ┌────────────────────────────────────────┐
                                │      OPERATOR MANAGEMENT DASHBOARD     │
                                │ • Live MJPEG Video Stream (/video_feed)│
                                │ • High-Contrast PASS/FAIL View         │
                                │ • 3 Real-Time KPIs (FPS, Count, Latency│
                                │ • Motor Vibration Anomaly Badge        │
                                │ • 21 CFR Part 11 CSV Export Engine     │
                                └────────────────────────────────────────┘
```
