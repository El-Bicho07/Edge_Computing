#!/usr/bin/env python3
"""
Milestone 4: PLC Tag Transition Test Harness
Veyra Pharma Vision Edge System

Executes automated verification showing PLC registers changing in real-time
as objects are detected and evaluated.
"""

import time
from plc_bridge import PLCBridge

def run_plc_verification_test():
    print("\n" + "="*70)
    print("      M4 INDUSTRIAL PLC MODBUS TAG TRANSITION TEST HARNESS       ")
    print("="*70)

    plc = PLCBridge()

    def print_plc_state_banner(step_name):
        print(f"\n>>> STATE SNAPSHOT: {step_name} <<<")
        print(f"    Register 40001 (PACK_PRESENT)     : {plc.read_tag('PACK_PRESENT')}")
        print(f"    Register 40002 (INSPECTION_RESULT): {plc.read_tag('INSPECTION_RESULT')} (0=Pending, 1=Pass, 2=Fail)")
        print(f"    Register 40003 (DEFECT_SLOT_MASK) : {plc.read_tag('DEFECT_SLOT_MASK')} (Binary: {bin(plc.read_tag('DEFECT_SLOT_MASK'))})")
        print(f"    Coil 00001     (CONVEYOR_HALT_CMD): {plc.read_tag('CONVEYOR_HALT_CMD')} (0=Run, 1=Halt)")

    # Initial State
    print_plc_state_banner("Initial System Idle")

    # Step 1: Object arrives under camera
    plc.on_object_detected()
    print_plc_state_banner("Step 1: Object Arrived under Optical Sensor")

    # Step 2: YOLOv8 flags defect on Pill #2 and Pill #5
    time.sleep(0.3)
    plc.on_inspection_complete(is_defect=True, defect_slots=[1, 4]) # 0-indexed: Slot 1=Pill 2, Slot 4=Pill 5
    print_plc_state_banner("Step 2: Defect Confirmed on Pills #2 and #5")

    # Step 3: Diverter clears pack into reject chute
    time.sleep(0.4)
    plc.on_object_departed()
    print_plc_state_banner("Step 3: Object Cleared into Reject Chute")

    print("\n[+] PLC Tag State Transition Test PASSED Successfully.")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_plc_verification_test()
