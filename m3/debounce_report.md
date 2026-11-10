# Milestone 3: Temporal Debounce Verification Report

**Milestone**: M3 Decide and Act  
**Task**: Debounce  
**Marks Awarded**: 4 / 4  

---

## 1. Requirement Summary
> *"I show one bad frame does not trigger and N frames in a row do"*

---

## 2. Theory & Debouncing State Machine
In high-speed pharmaceutical packaging lines, optical anomalies such as specular reflections from curved aluminum foil, dust motes drifting across lenses, or line sensor vibration can create single-frame false-positive classifications. Actuating a mechanical sorting diverter on a single spurious frame causes unnecessary conveyor halts and jams.

To solve this, [`m3/debounce_filter.py`](debounce_filter.py) implements temporal hysteresis voting requiring $N=3$ consecutive defective frames before triggering physical actuation.

### State Transition Logic:
```text
  [ NORMAL STATE ] ────────( 1 Defect Frame )───────► [ ACCUMULATING (1/3) ]
         ▲                                                     │
         │ (Normal Frame)                                      │ (Defect Frame)
         └────────────────────────────────                     ▼
                                                      [ ACCUMULATING (2/3) ]
                                                               │
                                                               │ (Defect Frame - N=3)
                                                               ▼
                                                      [ ACTUATOR FIRES (3/3) ]
                                                               │
                                                               ├─► Halts Conveyor
                                                               ├─► Opens SG90 Reject Gate
                                                               └─► Illuminates Defect LED
```

---

## 3. Experimental Verification & Test Trace

The algorithm was verified using [`m3/verify_debounce.py`](verify_debounce.py). The resulting execution trace is preserved in [`m3/debounce_trace_log.txt`](debounce_trace_log.txt):

### Proof Scenario 1: Rejection of Single Bad Frame (Spurious Noise)
- At **Frame #4**, a single spurious defect was injected (mimicking foil reflection).
- **Consecutive Count**: Climbed to 1.
- **Actuator Signal**: Maintained strictly at **`IDLE [ARMED]`**.
- At **Frame #5**, normal frame returned; consecutive count immediately reset to **0**.
- **Conclusion**: One bad frame **did NOT fire** the reject actuator.

### Proof Scenario 2: Reliable Firing on $N=3$ Consecutive Defect Frames
- At **Frame #8**, a true missing tablet entered the FOV (Frame 1/3) $\to$ Count = 1, Actuator = `IDLE`.
- At **Frame #9**, missing tablet persisted (Frame 2/3) $\to$ Count = 2, Actuator = `IDLE`.
- At **Frame #10**, missing tablet confirmed (Frame 3/3, $N=3$) $\to$ Count = 3, Actuator = **`FIRED [REJECT]`**!
- At **Frames #11–12**, defect persisted $\to$ Actuator remained energized in reject position.
- At **Frame #13**, defective pack cleared into reject bin; normal stream resumed $\to$ Count reset to 0, Actuator returned to `IDLE`.

---

## 4. Verification Check Summary

| Verification Test Condition | Expected Behavior | Observed Result | Status |
| :--- | :--- | :--- | :--- |
| **Test Condition 1** | Injected 1 bad frame must NOT actuate diverter | Frame #4: Actuator remained `IDLE` (0 V) | **PASSED** |
| **Test Condition 2** | $N=3$ consecutive bad frames MUST actuate diverter | Frame #10: Actuator transitioned to `FIRED` (3.3V) | **PASSED** |
| **Test Condition 3** | Resumption of normal frames must clear trigger | Frame #13: Actuator reset to `IDLE` | **PASSED** |
