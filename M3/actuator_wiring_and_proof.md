# Milestone 3: Actuator Hardware Interface, Wiring & Live Proof

**Milestone**: M3 Decide and Act  
**Task**: Actuator fires  
**Rubric Weight**: 3 Marks  

---

## 1. Requirement Summary
> *"I make the relay, LED or conveyor-stop signal work live"*

---

## 2. Hardware Wiring & Electrical Schematics

The Raspberry Pi 5 40-pin GPIO header interfaces with three physical actuation sub-circuits designed for industrial reliability:

| Peripheral / Signal | BCM GPIO Pin | Physical Board Pin | Electrical Specification | Protective Isolation / Interface |
| :--- | :---: | :---: | :--- | :--- |
| **Conveyor Stop Relay** | **GPIO 14** | Pin 8 (TXD) | 5V Coil / Active LOW (NO logic) | Optocoupled relay board with PC817 optoisolator & flyback diode |
| **SG90 Servo Diverter** | **GPIO 18** | Pin 12 (PWM0) | 50 Hz PWM ($0.5\text{ ms} \dots 2.4\text{ ms}$) | Independent 5V/2A rail sharing common ground with Pi |
| **IR Proximity Sensor** | **GPIO 5** | Pin 29 | 3.3V Digital Input (Active LOW) | Internal pull-up resistor enabled; optical beam interrupt |
| **Pill 1 Defect LED** | **GPIO 17** | Pin 11 | 3.3V High / 10 mA | $330\,\Omega$ current-limiting series resistor |
| **Pill 2 Defect LED** | **GPIO 27** | Pin 13 | 3.3V High / 10 mA | $330\,\Omega$ current-limiting series resistor |
| **Pill 3 Defect LED** | **GPIO 22** | Pin 15 | 3.3V High / 10 mA | $330\,\Omega$ current-limiting series resistor |
| **Pill 4 Defect LED** | **GPIO 23** | Pin 16 | 3.3V High / 10 mA | $330\,\Omega$ current-limiting series resistor |
| **Pill 5 Defect LED** | **GPIO 24** | Pin 18 | 3.3V High / 10 mA | $330\,\Omega$ current-limiting series resistor |
| **Pill 6 Defect LED** | **GPIO 25** | Pin 22 | 3.3V High / 10 mA | $330\,\Omega$ current-limiting series resistor |
| **Ground Reference** | **GND** | Pins 6, 9, 14, 20, 39| Common DC Ground | Star-ground topology preventing ground loop noise |

---

## 3. On-Device Execution Proof

Executed live using [`m3/test_actuator_live.py`](test_actuator_live.py):

```text
pi@raspberrypi:~/object_detection $ python3 m3/test_actuator_live.py
=================================================================
      M3 LIVE HARDWARE ACTUATOR FUNCTIONAL TEST RUNNER      
=================================================================
[*] Initializing Actuator Controller (Hardware Mode: REAL GPIO)...

--- TEST PHASE 1: Conveyor Relay Start/Stop Cycling ---
[ACTUATOR] Conveyor Motor Signal: RUNNING (Relay Energized)
[ACTUATOR] Conveyor Motor Signal: STOPPED (Reason: OPERATOR_STOP_TEST)

--- TEST PHASE 2: SG90 Servo Diverter Sweeping ---
[*] Sweeping diverter to REJECT position (90°)...
[ACTUATOR] SG90 Diverter Gate: OPEN (Rejecting to Bin) [90°]
[*] Returning diverter to PASS position (0°)...
[ACTUATOR] SG90 Diverter Gate: CLOSED (Pass-Through) [0°]

--- TEST PHASE 3: 6-Channel Pill Defect LED Sequence ---
[ACTUATOR] Pill Slot #1 Defect LED: ON (GPIO 17)
[ACTUATOR] All 6 Pill Defect LEDs: OFF
[ACTUATOR] Pill Slot #2 Defect LED: ON (GPIO 27)
[ACTUATOR] All 6 Pill Defect LEDs: OFF
[ACTUATOR] Pill Slot #3 Defect LED: ON (GPIO 22)
[ACTUATOR] All 6 Pill Defect LEDs: OFF
[ACTUATOR] Pill Slot #4 Defect LED: ON (GPIO 23)
[ACTUATOR] All 6 Pill Defect LEDs: OFF
[ACTUATOR] Pill Slot #5 Defect LED: ON (GPIO 24)
[ACTUATOR] All 6 Pill Defect LEDs: OFF
[ACTUATOR] Pill Slot #6 Defect LED: ON (GPIO 25)
[ACTUATOR] All 6 Pill Defect LEDs: OFF

--- TEST PHASE 4: End-to-End Coordinated Defect Trip ---
[*] Simulated Scenario: Blister pack enters with defective Pill #5...
[ACTUATOR] Conveyor Motor Signal: RUNNING (Relay Energized)
[ACTUATOR] Conveyor Motor Signal: STOPPED (Reason: PILL_5_MISSING_CONFIRMED)
[ACTUATOR] SG90 Diverter Gate: OPEN (Rejecting to Bin) [90°]
[ACTUATOR] Pill Slot #5 Defect LED: ON (GPIO 24)
[*] Defective pack cleared. Restoring forward motion...
[ACTUATOR] All 6 Pill Defect LEDs: OFF
[ACTUATOR] SG90 Diverter Gate: CLOSED (Pass-Through) [0°]
[ACTUATOR] Conveyor Motor Signal: RUNNING (Relay Energized)

[+] All Actuator Live Diagnostic Tests PASSED Successfully!
[*] Actuator Controller Safely Released.
=================================================================
```

Visual evidence of the operational hardware with lit LEDs and actuated servo diverter is preserved in [`Pictures/20261010_163213_grim.png`](../Pictures/20261010_163213_grim.png).
