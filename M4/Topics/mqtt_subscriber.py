#!/usr/bin/env python3
"""
Milestone 4: Industrial MQTT Telemetry Subscriber
Veyra Pharma Vision Edge System

Subscribes to wild-card topic 'factory/edge/#' and processes:
1. factory/edge/blister/detection
2. factory/edge/motor/anomaly_score
"""

import time
import json

def simulate_subscriber():
    print("\n" + "="*70)
    print("      M4 INDUSTRIAL MQTT SUBSCRIBER DISPATCH CONSOLE      ")
    print("="*70)
    print("[*] Subscribing to Topic Pattern: factory/edge/#")
    print("[*] Listening for incoming telemetry packets...\n")

    incoming_messages = [
        ("factory/edge/blister/detection", {
            "pack_id": "BLISTER-2026-0101",
            "timestamp": "2026-10-09T18:12:01Z",
            "verdict": "PASS",
            "defect_pill_slots": [],
            "confidence": 0.94
        }),
        ("factory/edge/motor/anomaly_score", {
            "sensor_id": "MPU6050-MOTOR-DRIVE-01",
            "timestamp": "2026-10-09T18:12:01Z",
            "vibration_rms_g": 0.052,
            "anomaly_score": 1.12,
            "health_status": "HEALTHY_OPTIMAL"
        }),
        ("factory/edge/blister/detection", {
            "pack_id": "BLISTER-2026-0102",
            "timestamp": "2026-10-09T18:12:03Z",
            "verdict": "FAIL",
            "defect_pill_slots": [2, 5],
            "confidence": 0.89
        }),
        ("factory/edge/motor/anomaly_score", {
            "sensor_id": "MPU6050-MOTOR-DRIVE-01",
            "timestamp": "2026-10-09T18:12:03Z",
            "vibration_rms_g": 0.584,
            "anomaly_score": 92.4,
            "health_status": "CRITICAL_MAINTENANCE_REQUIRED"
        })
    ]

    for topic, payload in incoming_messages:
        print(f"[SUB RECEIVED] Topic: {topic}")
        if "blister" in topic:
            status = "✅ PASS" if payload["verdict"] == "PASS" else "❌ FAIL"
            print(f"               --> Pack: {payload['pack_id']} | Verdict: {status} | Slots: {payload['defect_pill_slots']}")
        elif "motor" in topic:
            alert = "⚠️ ALERT" if payload["anomaly_score"] > 4.28 else "🟢 OK"
            print(f"               --> Motor: {payload['sensor_id']} | RMS: {payload['vibration_rms_g']}g | Score: {payload['anomaly_score']} [{alert}]")
        print()
        time.sleep(0.4)

    print("="*70 + "\n")

if __name__ == "__main__":
    simulate_subscriber()
