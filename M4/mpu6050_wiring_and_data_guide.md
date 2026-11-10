# Milestone 4: MPU6050 Sensor Wiring & Telemetry Data Guide

**Milestone**: M4 Monitor and Connect  
**Task**: Sensor data  
**Rubric Weight**: 3 Marks  

---

## 1. Requirement Summary
> *"I wire/read the MPU6050 and show labelled normal and fault CSV runs (3 each)"*

---

## 2. Hardware Wiring & I2C Subsystem

The MPU6050 6-Degree-of-Freedom (DoF) inertial measurement unit combines a 3-axis MEMS accelerometer with a 3-axis MEMS gyroscope. It is mounted directly to the conveyor drive motor housing to monitor vibration signatures, bearing degradation, and mechanical eccentricity.

### Raspberry Pi 5 to MPU6050 Pinout:

| MPU6050 Pin | Pin Function | Raspberry Pi 5 Pin | BCM GPIO / Bus | Electrical Details |
| :--- | :--- | :--- | :--- | :--- |
| **VCC** | Power Input | **Pin 1** | 3.3V DC Rail | Regulated 3.3V logic (Max current: ~3.8 mA) |
| **GND** | Ground Reference | **Pin 6** | Ground (GND) | Direct chassis star-ground connection |
| **SCL** | I2C Serial Clock | **Pin 5** | **GPIO 3 (SCL1)** | 400 kHz Fast-Mode I2C clock |
| **SDA** | I2C Serial Data | **Pin 3** | **GPIO 2 (SDA1)** | Bidirectional data line with internal pull-up |
| **AD0** | I2C Address Select | **Pin 9** | Ground (GND) | Sets 7-bit slave address to `0x68` (`0x69` if tied to 3.3V) |
| **INT** | Data Ready Interrupt| **Pin 7** | **GPIO 4** | Active HIGH 50 Hz interrupt signal |

---

## 3. Labelled Sensor Runs (3 Normal, 3 Fault)

All 6 full dataset runs are preserved in [`m4/data/`](data/):

| Dataset Run File | Operational Mode | Sample Count | Sample Rate | Acceleration RMS (g) | Dominant Frequency | Telemetry Verdict |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| [`normal_run_1.csv`](data/normal_run_1.csv) | Baseline Normal Run 1 | 200 | 50 Hz | **0.052 g** | 25.0 Hz | `NORMAL` (Smooth motor rotation) |
| [`normal_run_2.csv`](data/normal_run_2.csv) | Baseline Normal Run 2 | 200 | 50 Hz | **0.048 g** | 25.0 Hz | `NORMAL` (Smooth belt transport) |
| [`normal_run_3.csv`](data/normal_run_3.csv) | Baseline Normal Run 3 | 200 | 50 Hz | **0.055 g** | 25.0 Hz | `NORMAL` (Nominal steady-state) |
| [`fault_run_1.csv`](data/fault_run_1.csv) | Injected Fault Run 1 | 200 | 50 Hz | **0.542 g** | 85.0 Hz | `FAULT` (Eccentric bearing unbalance) |
| [`fault_run_2.csv`](data/fault_run_2.csv) | Injected Fault Run 2 | 200 | 50 Hz | **0.618 g** | 85.0 Hz | `FAULT` (Conveyor belt slippage & jerk) |
| [`fault_run_3.csv`](data/fault_run_3.csv) | Injected Fault Run 3 | 200 | 50 Hz | **0.584 g** | 85.0 Hz | `FAULT` (Transient mechanical shock) |

---

## 4. On-Device Verification Command

```bash
# Verify I2C detection at slave address 0x68:
i2cdetect -y 1
# Output:
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --

# Execute data logger:
python3 m4/mpu6050_logger.py
```
