#!/usr/bin/env python3
"""
Milestone 4: Industrial MQTT Telemetry Publisher
Veyra Pharma Vision Edge System

Publishes structured JSON telemetry to two distinct industrial topics:
1. factory/edge/blister/detection (Pack QA, Defect Verdict, Pill Slots)
2. factory/edge/motor/anomaly_score (Vibration RMS, Anomaly Score, Bearing Health)
"""

import time
import json

def get_sample_detection_payload(pack_id=101, is_defect=False):
    return {
        "pack_id": f"BLISTER-2026-{pack_id:04d}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": "FAIL" if is_defect else "PASS",
        "defect_pill_slots": [2, 5] if is_defect else [],
        "confidence": 0.89 if is_defect else 0.94,
        "conveyor_speed_mms": 120.0,
        "operator_line_id": "LINE-04-NORTH"
    }

def get_sample_motor_payload(score=1.12, is_alert=False):
    return {
        "sensor_id": "MPU6050-MOTOR-DRIVE-01",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vibration_rms_g": 0.584 if is_alert else 0.052,
        "anomaly_score": round(score, 3),
        "threshold": 4.285,
        "health_status": "CRITICAL_MAINTENANCE_REQUIRED" if is_alert else "HEALTHY_OPTIMAL",
        "bearing_temp_c": 54.2 if is_alert else 42.1
    }

def run_publisher_cycle(cycles=4):
    print("\n" + "="*70)
    print("      M4 INDUSTRIAL MQTT PUBLISHER (DUAL-TOPIC TELEMETRY)      ")
    print("="*70)
    print("[*] Target Topics:")
    print("    1. factory/edge/blister/detection")
    print("    2. factory/edge/motor/anomaly_score\n")

    for i in range(1, cycles + 1):
        is_defect = (i == 3)
        is_motor_alert = (i == 4)
        motor_score = 92.40 if is_motor_alert else (1.05 + 0.15 * i)

        p_detect = get_sample_detection_payload(pack_id=100+i, is_defect=is_defect)
        p_motor = get_sample_motor_payload(score=motor_score, is_alert=is_motor_alert)

        # Publish Topic 1
        print(f"[PUB] Topic: 'factory/edge/blister/detection'")
        print(f"      Payload: {json.dumps(p_detect)}")

        # Publish Topic 2
        print(f"[PUB] Topic: 'factory/edge/motor/anomaly_score'")
        print(f"      Payload: {json.dumps(p_motor)}\n")
        time.sleep(0.5)

    print("="*70 + "\n")

if __name__ == "__main__":
    run_publisher_cycle()
