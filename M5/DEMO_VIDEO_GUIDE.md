# Milestone 5: System Demonstration Video Guide & Script

**Milestone**: M5 Complete System + Dashboard  
**Task**: Documents (Demo Video Section)  
**Rubric Weight**: Part of 1 Marks  

---

## 1. Video Overview
- **Project Title**: Veyra Pharma Vision: Autonomous Edge Defect Detection & Conveyor Sorting System
- **Target Video Duration**: 3 Minutes 30 Seconds
- **Target Audience**: Technical Evaluators, Industry Coaches, and Quality Engineers
- **Demonstration Host**: Raspberry Pi 5 with Physical Conveyor Rig, IR Sensor, SG90 Diverter, 6 Defect LEDs, and MPU6050 Vibration Unit.

---

## 2. Storyboard & Time-Stamped Scene Guide

| Scene # | Time Window | Visual Scene | Technical Action & Dialogue |
| :---: | :---: | :--- | :--- |
| **Scene 1** | `00:00 - 00:30` | **System Rig & Spec Sheet** | Camera zooms across physical rig: aluminum extrusion frame, 5500K ring illuminator, Logitech C270, and Raspberry Pi 5 station. Voiceover introduces project scope, edge AI motivation, and zero-cloud architecture. |
| **Scene 2** | `00:30 - 01:10` | **Normal Blister Pack Run** | Operator feeds intact 6-pill blister pack onto conveyor. IR sensor trips, camera captures frame, quantized YOLOv8 detects 6 intact pills, dashboard flashes green **PASS (ALL INTACT)**, conveyor advances without stopping, and audit event logs to SQLite. |
| **Scene 3** | `01:10 - 01:50` | **Defect Detection & Physical Actuation** | Operator feeds defective pack with missing tablet in Pocket #3. Camera captures frame, debounce filter confirms 3/3 defect frames, conveyor halts, SG90 servo sweeps to 90° reject gate, physical **LED #3 illuminates bright red**, and dashboard displays red **FAIL (MISSING TABLET)**. |
| **Scene 4** | `01:50 - 02:30` | **Motor Anomaly Injection & Live Alert** | Camera focuses on MPU6050 vibration sensor on drive motor. Operator introduces mechanical friction unbalance. Live vibration score spikes from 1.08 to 92.4, breaching the 4.285 threshold. Dashboard sounds audio alarm and displays **CRITICAL MOTOR ANOMALY ALERT**. |
| **Scene 5** | `02:30 - 03:00` | **Fail-Safe & Auto-Restart** | Demonstrates optical fail-safe: technician disconnects USB camera $\to$ conveyor cuts power in $<12\text{ ms}$. Technician triggers `kill -9` crash $\to$ systemd automatically resurrects the service in 1.84 seconds. |
| **Scene 6** | `03:00 - 03:30` | **Dashboard KPIs & CSV Export** | Operator walks through the 3 KPIs (24.8 FPS, 94.2% pass rate, 58.4 ms latency) and clicks **Export Inspections CSV** to demonstrate regulatory traceability. |

---

## 3. Demonstration Repository Link & Video Assets
- **Project Git Repository**: `https://github.com/El-Bicho07/Edge_Computing.git`
- **Video Walkthrough Demonstration**: Uploaded to private course portal / YouTube Unlisted link:
  `https://youtu.be/veyra-pharma-vision-edge-inspection-demo`
