#!/usr/bin/env python3
"""
Milestone 4: Industrial PLC Bridge & Register Tag Controller
Veyra Pharma Vision Edge System

Interfaces with programmable logic controllers (PLCs) via Modbus TCP (Port 502)
and OPC-UA to coordinate conveyor actuation:
- Holding Register 40001: PACK_PRESENT (0 = Idle, 1 = Object Arrived)
- Holding Register 40002: INSPECTION_RESULT (0 = Pending, 1 = PASS, 2 = FAIL)
- Holding Register 40003: DEFECT_SLOT_MASK (Bitmask: Bit0=Pill1 ... Bit5=Pill6)
- Discrete Coil 00001   : CONVEYOR_HALT_CMD (0 = Belt Run, 1 = Belt Stop)
"""

import time

class PLCBridge:
    def __init__(self, host="127.0.0.1", port=502):
        self.host = host
        self.port = port
        # Simulated PLC Internal Register Bank
        self.holding_registers = {
            40001: 0, # PACK_PRESENT
            40002: 0, # INSPECTION_RESULT
            40003: 0  # DEFECT_SLOT_MASK
        }
        self.coils = {
            1: 0      # CONVEYOR_HALT_CMD
        }
        print(f"[*] PLC Modbus Bridge Initialized (Target: {self.host}:{self.port})")

    def read_tag(self, tag_name):
        mapping = {
            "PACK_PRESENT": self.holding_registers[40001],
            "INSPECTION_RESULT": self.holding_registers[40002],
            "DEFECT_SLOT_MASK": self.holding_registers[40003],
            "CONVEYOR_HALT_CMD": self.coils[1]
        }
        return mapping.get(tag_name, None)

    def write_tag(self, tag_name, value):
        if tag_name == "PACK_PRESENT":
            self.holding_registers[40001] = int(value)
        elif tag_name == "INSPECTION_RESULT":
            self.holding_registers[40002] = int(value)
        elif tag_name == "DEFECT_SLOT_MASK":
            self.holding_registers[40003] = int(value)
        elif tag_name == "CONVEYOR_HALT_CMD":
            self.coils[1] = 1 if value else 0

        print(f"[PLC WRITE] Tag: '{tag_name}' -> New Value: {value}")

    def on_object_detected(self):
        """Called when optical IR beam is broken."""
        print("\n--- [EVENT] Optical Proximity Sensor Tripped: Blister Pack Arrived ---")
        self.write_tag("PACK_PRESENT", 1)
        self.write_tag("INSPECTION_RESULT", 0) # Pending
        self.write_tag("DEFECT_SLOT_MASK", 0)

    def on_inspection_complete(self, is_defect: bool, defect_slots=None):
        """Called when YOLO inspection verdict is rendered."""
        if defect_slots is None:
            defect_slots = []

        print(f"\n--- [EVENT] Vision Inspection Complete (Verdict: {'FAIL' if is_defect else 'PASS'}) ---")
        if not is_defect:
            self.write_tag("INSPECTION_RESULT", 1) # 1 = PASS
            self.write_tag("DEFECT_SLOT_MASK", 0)
            self.write_tag("CONVEYOR_HALT_CMD", 0) # Belt continues
        else:
            # Build bitmask (e.g. slots 2 and 5 -> (1<<2) | (1<<5) = 4 + 32 = 36)
            bitmask = 0
            for s in defect_slots:
                bitmask |= (1 << s)
            self.write_tag("INSPECTION_RESULT", 2) # 2 = FAIL
            self.write_tag("DEFECT_SLOT_MASK", bitmask)
            self.write_tag("CONVEYOR_HALT_CMD", 1) # Halt motor drive!

    def on_object_departed(self):
        """Called when blister pack clears the station."""
        print("\n--- [EVENT] Blister Pack Cleared Station ---")
        self.write_tag("PACK_PRESENT", 0)
        self.write_tag("CONVEYOR_HALT_CMD", 0)

if __name__ == "__main__":
    plc = PLCBridge()
    # Simulate full arrival, detection, and reject sequence
    plc.on_object_detected()
    time.sleep(0.5)
    plc.on_inspection_complete(is_defect=True, defect_slots=[1, 4])
    time.sleep(0.5)
    plc.on_object_departed()
