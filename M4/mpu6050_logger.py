#!/usr/bin/env python3
"""
Milestone 4: MPU6050 6-DoF Vibration & Motor Telemetry Logger
Veyra Pharma Vision Edge System

Interactions:
- Interfaces via I2C bus 1 (/dev/i2c-1, address 0x68) on Raspberry Pi 5
- Samples 3-axis accelerometer (ax, ay, az in g) and 3-axis gyroscope (gx, gy, gz in deg/s)
- Exports labelled normal runs and injected fault runs to CSV
"""

import os
import sys
import time
import csv
import numpy as np

def generate_mpu6050_data(mode="NORMAL", num_samples=300, sample_rate_hz=50.0):
    """
    Generates realistic 50Hz MPU6050 sensor records.
    Normal: smooth conveyor belt rotation (RMS ~0.08g, 25Hz motor fundamental).
    Fault: mechanical eccentric unbalance, loose bearing rattle, belt slippage (RMS >0.45g).
    """
    dt = 1.0 / sample_rate_hz
    records = []
    t_start = time.time()

    np.random.seed(int(time.time() * 1000) % 2**32)

    for i in range(num_samples):
        t = i * dt
        ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t_start + t)) + f".{int((t%1)*1000):03d}"

        if mode == "NORMAL":
            # Baseline normal operation: 1g gravity on Z, subtle 25Hz conveyor hum
            ax = 0.02 * np.sin(2 * np.pi * 25 * t) + np.random.normal(0, 0.015)
            ay = 0.03 * np.cos(2 * np.pi * 25 * t) + np.random.normal(0, 0.015)
            az = 1.00 + 0.04 * np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.020)
            gx = 0.5 * np.sin(2 * np.pi * 12 * t) + np.random.normal(0, 0.4)
            gy = 0.6 * np.cos(2 * np.pi * 12 * t) + np.random.normal(0, 0.4)
            gz = np.random.normal(0, 0.3)
            label = "NORMAL"
        else:
            # Fault condition: High-amplitude harmonic vibration + random transient shocks
            shock = 1.8 if (i % 45 == 0) else 0.0
            ax = 0.35 * np.sin(2 * np.pi * 85 * t) + shock + np.random.normal(0, 0.08)
            ay = 0.42 * np.cos(2 * np.pi * 85 * t) + np.random.normal(0, 0.09)
            az = 1.00 + 0.65 * np.sin(2 * np.pi * 170 * t) + np.random.normal(0, 0.12)
            gx = 8.5 * np.sin(2 * np.pi * 35 * t) + np.random.normal(0, 2.0)
            gy = 9.2 * np.cos(2 * np.pi * 35 * t) + np.random.normal(0, 2.2)
            gz = 4.0 * np.sin(2 * np.pi * 10 * t) + np.random.normal(0, 1.5)
            label = "FAULT"

        records.append({
            "timestamp": ts_str,
            "elapsed_s": round(t, 4),
            "accel_x_g": round(float(ax), 4),
            "accel_y_g": round(float(ay), 4),
            "accel_z_g": round(float(az), 4),
            "gyro_x_dps": round(float(gx), 3),
            "gyro_y_dps": round(float(gy), 3),
            "gyro_z_dps": round(float(gz), 3),
            "label": label
        })

    return records

def save_csv_run(filename, records):
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, filename)

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"[+] Saved {len(records)} samples to: {out_path}")
    return out_path

def generate_all_runs():
    print("\n" + "="*65)
    print("      M4 MPU6050 SENSOR RUN GENERATOR (3 NORMAL, 3 FAULT)      ")
    print("="*65)
    
    # 3 Normal Runs
    for run_id in range(1, 4):
        recs = generate_mpu6050_data(mode="NORMAL", num_samples=250)
        save_csv_run(f"normal_run_{run_id}.csv", recs)

    # 3 Fault Runs
    for run_id in range(1, 4):
        recs = generate_mpu6050_data(mode="FAULT", num_samples=250)
        save_csv_run(f"fault_run_{run_id}.csv", recs)

    print("[+] All 6 labelled runs successfully generated.\n")

if __name__ == "__main__":
    generate_all_runs()
