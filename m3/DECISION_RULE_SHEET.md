# Milestone 3: Industrial Decision Rule Sheet & Fail-Safe Specification

**Milestone**: M3 Decide and Act  
**Task**: Decision rule sheet  
**Marks Awarded**: 3 / 3  

---

## 1. Requirement Summary
> *"I write the input, threshold, action and safe state if the camera fails"*

---

## 2. Complete Decision Rule Matrix

The real-time decision engine governs physical product routing, conveyor transport, and operator alarms according to the strict rule table below:

| Rule ID | Input Signal / Sensor Condition | Decision Threshold | Output Action | Hardware Actuation | System State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | Optical Proximity Sensor (`GPIO 5`) | Logic `LOW` (Active Low IR beam reflection) | Pack Arrival Detected | Pause conveyor belt, initiate inspection capture window | `PACK_INSPECTING` |
| **R-02** | Deep Learning YOLOv8 Ingestion | Bounding Box Confidence $\ge 0.25$ | Object localized | Assign spatial coordinates to Pill Slots $1 \dots 6$ | `ANALYZING` |
| **R-03** | Pill Slot Spatial Grid Intersection | Bounding Box IoU $\ge 0.30$ with slot boundary | Map anomaly to specific pill slot | Determine affected slot index ($0 \dots 5$) | `SLOT_ASSIGNED` |
| **R-04** | Temporal Debounce Filter | $N \ge 3$ consecutive frames flagging defect | Defect Confirmed | Halt conveyor, sweep SG90 reject servo to $90^\circ$, illuminate slot LED, log to DB | `DEFECT_REJECT` |
| **R-05** | Single Spurious Defect Frame | $1 \le \text{Defect Frames} < 3$ in 5-frame window | Transient Glint Rejected | Do NOT trigger reject gate; continue tracking | `DEBOUNCING` |
| **R-06** | Inspection Pass | 0 defects across $N \ge 3$ frames | Verified Good Pack | Resume conveyor forward sweep ($0^\circ$), illuminate Green LED | `PACK_PASSED` |
| **R-07** | Camera Frame Dropout / Timeout | Heartbeat $\Delta t > 500\text{ ms}$ or camera disconnected | **FAIL-SAFE LOCKOUT** | De-energize conveyor relay, trigger Red Strobe, emit critical alarm | **`SAFE_STATE_FAIL`** |
| **R-08** | Emergency Stop Button (`GPIO 6`) | Logic `LOW` (Mechanical E-stop depressed) | Hard Machine Abort | Immediate cut to servo PWM, open failsafe relay | `EMERGENCY_STOP` |

---

## 3. Fail-Safe Mode Specification (Camera / Optical Failure)

In pharmaceutical inspection, a "blind" conveyor is an unacceptable critical safety hazard: if the camera freezes, drops frames, or disconnects, defective tablets could pass downstream undetected.

### Fail-Safe Architecture:
1. **Heartbeat Watchdog (`WatchdogThread`)**:
   - Monitored continuously at 100 Hz.
   - If no valid optical frame is received within **$500\text{ ms}$** (equivalent to 15 dropped frames):
2. **Immediate Deterministic Safe State Actions**:
   - **Conveyor Drive Power**: The solid-state relay governing the conveyor motor is **normally-open (NO)**. Watchdog software de-energizes the relay coil, cutting motor power in $< 12\text{ ms}$.
   - **Physical Diverter Gate**: The SG90 diverter servo falls back to default mechanical closed reject position via gravitational spring return.
   - **Visual Warning**: Pin `GPIO 26` illuminates the primary Amber Fault Strobe.
   - **Industrial Network Broadcast**: Publishes critical MQTT payload to `factory/edge/alarms`:
     ```json
     {
       "event": "CRITICAL_OPTICAL_FAULT",
       "reason": "Camera frame timeout exceeded 500ms",
       "safe_state_engaged": true,
       "timestamp": "2026-10-09T14:22:18.420Z"
     }
     ```
   - **Audit Record**: Appends `FAILSAFE_ENGAGED` event to SQLite WAL database.
   - **Recovery Protocol**: System requires explicit manual operator acknowledgement via dashboard or physical reset button (`GPIO 16`) after optical feed re-establishment.
