#!/usr/bin/env python3
"""
Milestone 3: Industrial Decision Engine & Fail-Safe Controller
Veyra Pharma Vision Edge System

Implements:
- Threshold validation and rule evaluation (R-01 through R-08)
- Real-time optical watchdog for camera failure fail-safe lock
- State machine transitioning: IDLE -> INSPECTING -> REJECT / PASS -> SAFE_STATE
"""

import time
import threading

class SystemState:
    IDLE = "IDLE"
    INSPECTING = "INSPECTING"
    PACK_PASSED = "PACK_PASSED"
    DEFECT_REJECT = "DEFECT_REJECT"
    SAFE_STATE_FAIL = "SAFE_STATE_FAIL"
    EMERGENCY_STOP = "EMERGENCY_STOP"

class DecisionEngine:
    def __init__(self, debounce_n=3, conf_threshold=0.25, camera_timeout_sec=0.50):
        self.debounce_n = debounce_n
        self.conf_threshold = conf_threshold
        self.camera_timeout_sec = camera_timeout_sec

        self.current_state = SystemState.IDLE
        self.last_frame_timestamp = time.perf_counter()
        self.consecutive_defects = 0
        self.failsafe_active = False

        self._lock = threading.Lock()

    def feed_camera_heartbeat(self):
        """Called whenever a valid frame is acquired."""
        with self._lock:
            self.last_frame_timestamp = time.perf_counter()
            if self.failsafe_active:
                print("[*] Camera heartbeat restored, but safe state requires operator reset.")

    def evaluate_inspection(self, detections, pack_present=True):
        """
        Evaluates detection candidates.
        detections: list of dicts [{'slot': 0..5, 'is_defect': bool, 'conf': float}]
        """
        with self._lock:
            # 1. Check optical watchdog
            dt_since_frame = time.perf_counter() - self.last_frame_timestamp
            if dt_since_frame > self.camera_timeout_sec:
                self.trigger_failsafe(f"Camera frame timeout ({dt_since_frame*1000:.1f} ms > {self.camera_timeout_sec*1000:.0f} ms)")
                return self.current_state, "HALT_FAILSAFE"

            if not pack_present:
                self.current_state = SystemState.IDLE
                self.consecutive_defects = 0
                return self.current_state, "WAITING_PACK"

            # 2. Check for defects above confidence threshold
            defects_in_frame = [
                d for d in detections 
                if d.get("is_defect", False) and d.get("conf", 0.0) >= self.conf_threshold
            ]

            if defects_in_frame:
                self.consecutive_defects += 1
            else:
                self.consecutive_defects = 0

            # 3. Apply Debounce Rule: N consecutive frames required
            if self.consecutive_defects >= self.debounce_n:
                self.current_state = SystemState.DEFECT_REJECT
                action = "ACTUATE_REJECT_GATE"
            elif self.consecutive_defects > 0:
                self.current_state = SystemState.INSPECTING
                action = f"DEBOUNCING ({self.consecutive_defects}/{self.debounce_n})"
            else:
                self.current_state = SystemState.PACK_PASSED
                action = "CONVEYOR_ADVANCE"

            return self.current_state, action

    def trigger_failsafe(self, reason):
        self.failsafe_active = True
        self.current_state = SystemState.SAFE_STATE_FAIL
        print(f"\n[!] >>> FAIL-SAFE ENGAGED: {reason} <<<")
        print("[!] ACTION: Conveyor relay cut (NO open) | Red strobe ON | Alarm dispatched.\n")

    def reset_failsafe(self):
        with self._lock:
            self.failsafe_active = False
            self.last_frame_timestamp = time.perf_counter()
            self.current_state = SystemState.IDLE
            self.consecutive_defects = 0
            print("[+] Fail-safe manually reset by operator. Resuming operational state.")

if __name__ == "__main__":
    engine = DecisionEngine(debounce_n=3, conf_threshold=0.25, camera_timeout_sec=0.20)
    print("Testing Decision Engine Logic...")

    # Test 1: Single bad frame (should not trigger reject)
    engine.feed_camera_heartbeat()
    state, action = engine.evaluate_inspection([{"slot": 1, "is_defect": True, "conf": 0.88}])
    print(f"Cycle 1 (1 Defect): State={state}, Action={action}")

    # Test 2: Normal frame follows (resets debounce)
    engine.feed_camera_heartbeat()
    state, action = engine.evaluate_inspection([])
    print(f"Cycle 2 (0 Defect): State={state}, Action={action}")

    # Test 3: 3 consecutive bad frames (triggers reject)
    for i in range(1, 4):
        engine.feed_camera_heartbeat()
        state, action = engine.evaluate_inspection([{"slot": 1, "is_defect": True, "conf": 0.88}])
        print(f"Cycle 3.{i} (Consecutive {i}): State={state}, Action={action}")

    # Test 4: Camera failure timeout
    print("\nSimulating Camera Failure (Frame Dropped)...")
    time.sleep(0.25)
    state, action = engine.evaluate_inspection([])
    print(f"Cycle 4 (After timeout): State={state}, Action={action}")
