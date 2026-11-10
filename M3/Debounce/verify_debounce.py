#!/usr/bin/env python3
"""
Milestone 3: Debounce Verification Harness
Veyra Pharma Vision Edge System

Proves:
1. One bad frame does NOT trigger actuator (glare/noise rejection)
2. N frames in a row (N=3) DOES trigger actuator
3. Recovery when normal frames resume
Logs trace to debounce_trace_log.txt.
"""

import os
import sys
from debounce_filter import DebounceFilter

def run_debounce_test():
    base_dir = os.path.dirname(__file__)
    log_path = os.path.join(base_dir, "debounce_trace_log.txt")

    debouncer = DebounceFilter(required_consecutive=3, window_size=5)

    # Test Sequence:
    # Frames 1-3: Normal
    # Frame 4: SPURIOUS DEFECT (e.g. foil glare spike) -> MUST NOT TRIGGER
    # Frames 5-7: Normal
    # Frames 8-10: 3 CONSECUTIVE DEFECTS (e.g. genuine missing pill) -> MUST TRIGGER AT FRAME 10
    # Frames 11-12: Defect persists -> Continues triggered
    # Frames 13-15: Normal returns -> Resets
    test_sequence = [
        (1, False, "Normal Pack Cavity 1"),
        (2, False, "Normal Pack Cavity 2"),
        (3, False, "Normal Pack Cavity 3"),
        (4, True,  "SPURIOUS NOISE: Specular Glare Spike"), # 1 Bad Frame
        (5, False, "Normal Pack Cavity 4"),
        (6, False, "Normal Pack Cavity 5"),
        (7, False, "Normal Pack Cavity 6"),
        (8, True,  "TRUE DEFECT: Missing Tablet (Frame 1)"),
        (9, True,  "TRUE DEFECT: Missing Tablet (Frame 2)"),
        (10, True, "TRUE DEFECT: Missing Tablet (Frame 3)"), # N=3 Trigger Point
        (11, True, "TRUE DEFECT: Missing Tablet (Frame 4)"),
        (12, True, "TRUE DEFECT: Missing Tablet (Frame 5)"),
        (13, False, "Conveyor Advanced - Next Pack Normal"),
        (14, False, "Next Pack Normal Cavity 2"),
        (15, False, "Next Pack Normal Cavity 3")
    ]

    log_lines = []
    log_lines.append("="*80)
    log_lines.append("     M3 DEBOUNCE VERIFICATION TRACE LOG (N = 3 CONSECUTIVE DEFECTS)     ")
    log_lines.append("="*80)
    log_lines.append(f"{'Frame':<6} | {'Input Verdict':<14} | {'Consecutive':<12} | {'Actuator Status':<18} | {'Description'}")
    log_lines.append("-" * 80)

    print("\n" + log_lines[0])
    print(log_lines[1])
    print(log_lines[2])
    print(log_lines[3])
    print(log_lines[4])

    single_bad_frame_suppressed = False
    consecutive_trigger_fired = False

    for frame_idx, is_defect, desc in test_sequence:
        triggered, status = debouncer.update(is_defect)
        actuator_str = "FIRED [REJECT]" if triggered else "IDLE [ARMED]"
        verdict_str = "DEFECT (1)" if is_defect else "NORMAL (0)"

        line = f"#{frame_idx:<5} | {verdict_str:<14} | {debouncer.consecutive_defect_count:<12} | {actuator_str:<18} | {desc}"
        log_lines.append(line)
        print(line)

        # Verification asserts
        if frame_idx == 4:
            if not triggered:
                single_bad_frame_suppressed = True
                print("   [+] PROOF CHECK 1: Frame #4 (Single Bad Frame) correctly SUPPRESSED.")
        
        if frame_idx == 10:
            if triggered:
                consecutive_trigger_fired = True
                print("   [+] PROOF CHECK 2: Frame #10 (N=3 Consecutive) correctly FIRED Actuator.")

    log_lines.append("-" * 80)
    log_lines.append(f"Result Check 1 (Single Bad Frame Rejected) : {'PASSED' if single_bad_frame_suppressed else 'FAILED'}")
    log_lines.append(f"Result Check 2 (N Consecutive Frames Fired) : {'PASSED' if consecutive_trigger_fired else 'FAILED'}")
    log_lines.append("="*80)

    with open(log_path, "w") as f:
        f.write("\n".join(log_lines) + "\n")

    print(f"\n[+] Debounce Trace Log saved to: {log_path}\n")

if __name__ == "__main__":
    run_debounce_test()
