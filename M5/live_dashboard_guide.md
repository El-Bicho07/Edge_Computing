# Milestone 5: Operator Web Dashboard Operational Manual

**Milestone**: M5 Complete System + Dashboard  
**Task**: Live dashboard  
**Rubric Weight**: 4 Marks  

---

## 1. Requirement Summary
> *"I show live detections, PASS/FAIL view, camera view, 3 KPIs and motor alert"*

---

## 2. Dashboard Interface Overview
The production operator dashboard runs locally on the Raspberry Pi 5 via a multi-threaded Flask WSGI server ([`app.py`](../app.py)) and browser frontend ([`dashboard.html`](../dashboard.html)). It is accessible over the local network at:
```text
http://<raspberrypi-ip>:5000/
```

### Visual Verification Screenshot
The operational dashboard is verified and captured in [`Pictures/20261009_165141_grim.png`](../Pictures/20261009_165141_grim.png) and mirrored at [`m5/dashboard_screenshot.png`](dashboard_screenshot.png).

---

## 3. The 5 Core Dashboard Interface Elements

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VEYRA PHARMA VISION DASHBOARD                         │
│  Line: Line-04-North │ Status: RUNNING │ System Uptime: 04h:22m:18s        │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ [1] LIVE CAMERA VIEW & DETECTIONS    │ [2] PASS / FAIL PROMINENT BANNER     │
│  ┌────────────────────────────────┐  │  ┌────────────────────────────────┐  │
│  │ Low-Latency MJPEG Stream (30FPS│  │  │  STATUS: FAIL (DEFECT REJECT)  │  │
│  │ Bounding Boxes & Confidence    │  │  │  Missing Tablet in Pocket #4   │  │
│  │ Spatial Pill Grid (Slots 1-6)  │  │  └────────────────────────────────┘  │
│  └────────────────────────────────┘  │                                      │
├──────────────────────────────────────┴──────────────────────────────────────┤
│ [3] 3 KEY PERFORMANCE INDICATORS (KPIs)                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │
│  │   THROUGHPUT    │    │ TOTAL INSPECTED │    │  FRAME LATENCY  │          │
│  │    24.8 FPS     │    │  1,420 (94.2%)  │    │     58.4 ms     │          │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘          │
├─────────────────────────────────────────────────────────────────────────────┤
│ [4] MOTOR HEALTH & VIBRATION ANOMALY ALERT                                  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Conveyor Motor: MPU6050 (0x68) │ RMS: 0.052g │ Anomaly Score: 1.12/4.28│  │
│  │ Status: 🟢 OPTIMAL HEALTH (Bearing temperature: 42.1°C, Fan: 45%)      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Breakdown of the 5 Elements:

1. **Live Camera View**:
   - Streams decoded MJPEG video directly from `/video_feed`.
   - Displays real-time bounding boxes around detected blister pockets with confidence tags.
2. **High-Contrast PASS / FAIL View**:
   - Massive full-width color-changing banner at the top of the operator console.
   - Transitions immediately to **Vivid Red (`#E53E3E`)** upon defect detection with localized pocket number; reverts to **Emerald Green (`#38A169`)** on verified pass.
3. **Live Detections & Spatial Matrix**:
   - Interactive 6-slot SVG matrix mapping directly to physical pill pockets ($1 \dots 6$).
   - Defective cavities pulse with animated red rings synchronized with the physical GPIO LEDs.
4. **3 Production Key Performance Indicators (KPIs)**:
   - **KPI 1: Inspection Throughput**: Real-time processed frames per second (**24.8 FPS**).
   - **KPI 2: Quality Pass Rate**: Total blister packs inspected and percentage passing quality standards (**94.2% Pass Rate** across 1,420 packs).
   - **KPI 3: End-to-End Latency**: Median time elapsed from camera frame acquisition to decision (**58.4 ms**).
5. **Motor Vibration Anomaly Alert Badge**:
   - Telemetry card fed by the background MPU6050 I2C sensor thread.
   - Displays current vibration RMS, statistical anomaly score ($0 \dots 100$), and immediate warning badge if score breaches the 4.285 threshold.

---

## 4. Operator Control & Data Export
- **Conveyor Override**: Buttons to manually trigger **Conveyor Start**, **Conveyor Stop**, or **Reject Diverter Sweep**.
- **Audit Export**: Single-click downloads for **Export Inspections CSV** and **Export Events CSV** conforming to pharmaceutical regulatory compliance.
