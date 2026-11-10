#!/usr/bin/env python3
"""
Milestone 3: Temporal Debounce Filter Module
Veyra Pharma Vision Edge System

Implements temporal hysteresis debouncing:
- Single noisy/glint defect frame does NOT trigger reject mechanism
- Exactly N consecutive defective frames triggers reject actuator
- Automatically resets when normal frames resume
"""

class DebounceFilter:
    def __init__(self, required_consecutive=3, window_size=5):
        self.N = required_consecutive
        self.window_size = window_size
        self.history = []
        self.consecutive_defect_count = 0
        self.actuator_triggered = False

    def update(self, is_defective_frame: bool):
        """
        Updates the filter with the latest frame verdict.
        Returns:
            triggered (bool): True if N consecutive defects achieved.
            state_str (str): Human-readable filter status.
        """
        self.history.append(is_defective_frame)
        if len(self.history) > self.window_size:
            self.history.pop(0)

        if is_defective_frame:
            self.consecutive_defect_count += 1
        else:
            self.consecutive_defect_count = 0
            self.actuator_triggered = False

        if self.consecutive_defect_count >= self.N:
            self.actuator_triggered = True
            status = f"DEFECT_CONFIRMED (Triggered: {self.consecutive_defect_count}/{self.N})"
        elif self.consecutive_defect_count > 0:
            status = f"DEBOUNCING_ACCUMULATION ({self.consecutive_defect_count}/{self.N} - Actuator Suppressed)"
        else:
            status = "NORMAL (Pass)"

        return self.actuator_triggered, status

    def reset(self):
        self.history.clear()
        self.consecutive_defect_count = 0
        self.actuator_triggered = False
