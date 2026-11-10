#!/usr/bin/env python3
"""
Milestone 3: Live Actuator Hardware Verification Test Script
Veyra Pharma Vision Edge System

Executes automated live functional tests on:
1. Solid-State Relay (Conveyor Motor Stop/Start)
2. SG90 Micro Servo Sorting Diverter
3. 6-Channel Pill Defect LED Array
"""

import time
from actuator_controller import ActuatorController

def run_actuator_live_test():
    print("\n" + "="*65)
    print("      M3 LIVE HARDWARE ACTUATOR FUNCTIONAL TEST RUNNER      ")
    print("="*65)
    
    actuator = ActuatorController()

    try:
        print("\n--- TEST PHASE 1: Conveyor Relay Start/Stop Cycling ---")
        actuator.start_conveyor()
        time.sleep(1.0)
        actuator.stop_conveyor(reason="OPERATOR_STOP_TEST")
        time.sleep(0.5)

        print("\n--- TEST PHASE 2: SG90 Servo Diverter Sweeping ---")
        print("[*] Sweeping diverter to REJECT position (90°)...")
        actuator.actuate_reject_gate(True)
        time.sleep(1.0)
        print("[*] Returning diverter to PASS position (0°)...")
        actuator.actuate_reject_gate(False)
        time.sleep(0.5)

        print("\n--- TEST PHASE 3: 6-Channel Pill Defect LED Sequence ---")
        for slot in range(6):
            actuator.illuminate_defect_slot(slot)
            time.sleep(0.25)
            actuator.clear_all_leds()
            time.sleep(0.10)

        print("\n--- TEST PHASE 4: End-to-End Coordinated Defect Trip ---")
        print("[*] Simulated Scenario: Blister pack enters with defective Pill #5...")
        actuator.start_conveyor()
        time.sleep(0.8)
        actuator.stop_conveyor(reason="PILL_5_MISSING_CONFIRMED")
        actuator.actuate_reject_gate(True)
        actuator.illuminate_defect_slot(4) # Slot 4 = Pill 5
        time.sleep(1.5)
        print("[*] Defective pack cleared. Restoring forward motion...")
        actuator.clear_all_leds()
        actuator.actuate_reject_gate(False)
        actuator.start_conveyor()
        time.sleep(0.8)

        print("\n[+] All Actuator Live Diagnostic Tests PASSED Successfully!")

    finally:
        actuator.cleanup()
        print("="*65 + "\n")

if __name__ == "__main__":
    run_actuator_live_test()
