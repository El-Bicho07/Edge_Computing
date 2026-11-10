#!/usr/bin/env python3
"""
Milestone 3: Actuator Hardware Controller (Relay, Servo, LEDs)
Veyra Pharma Vision Edge System

Controls physical edge actuators:
- Solid-State Relay (Conveyor Motor Stop Signal on GPIO 14 / Pin 8)
- SG90 Angular Micro Servo (Reject Sorting Diverter on GPIO 18 / Pin 12, PWM)
- 6-Channel Pill Defect LED Array (GPIO 17, 27, 22, 23, 24, 25)
- Active IR Optical Sensor (GPIO 5 / Pin 29)
Supports both real Raspberry Pi hardware (gpiozero / lgpio) and headless mock mode.
"""

import os
import sys
import time

MOCK_MODE = os.environ.get("MOCK_HARDWARE", "0") == "1"

try:
    if not MOCK_MODE and sys.platform.startswith("linux"):
        from gpiozero import OutputDevice, AngularServo, DigitalInputDevice
        from gpiozero.pins.pigpio import PiGPIOFactory
        REAL_GPIO = True
    else:
        REAL_GPIO = False
except Exception:
    REAL_GPIO = False

class ActuatorController:
    # Pinout definitions (BCM numbering)
    RELAY_PIN = 14       # Conveyor Run Relay (Active LOW / NO)
    SERVO_PIN = 18       # SG90 Reject Gate (PWM)
    IR_SENSOR_PIN = 5    # Active IR Proximity Sensor
    LED_PINS = [17, 27, 22, 23, 24, 25] # Slots 1 through 6

    def __init__(self):
        self.is_real = REAL_GPIO
        print(f"[*] Initializing Actuator Controller (Hardware Mode: {'REAL GPIO' if self.is_real else 'MOCK SIMULATION'})...")

        if self.is_real:
            self.relay = OutputDevice(self.RELAY_PIN, active_high=False, initial_value=False)
            self.servo = AngularServo(self.SERVO_PIN, min_angle=0, max_angle=90,
                                      min_pulse_width=0.0005, max_pulse_width=0.0024)
            self.ir_sensor = DigitalInputDevice(self.IR_SENSOR_PIN, pull_up=True)
            self.leds = [OutputDevice(pin, active_high=True, initial_value=False) for pin in self.LED_PINS]
        else:
            self.relay_state = False
            self.servo_angle = 0
            self.led_states = [False] * 6

    def start_conveyor(self):
        """Energizes conveyor motor relay."""
        if self.is_real:
            self.relay.on()
        else:
            self.relay_state = True
        print("[ACTUATOR] Conveyor Motor Signal: RUNNING (Relay Energized)")

    def stop_conveyor(self, reason="DEFECT_DETECTED"):
        """De-energizes conveyor motor relay (Immediate Stop)."""
        if self.is_real:
            self.relay.off()
        else:
            self.relay_state = False
        print(f"[ACTUATOR] Conveyor Motor Signal: STOPPED (Reason: {reason})")

    def actuate_reject_gate(self, open_gate=True):
        """Sweeps SG90 diverter gate to 90 degrees (open) or 0 degrees (closed)."""
        target_angle = 90 if open_gate else 0
        if self.is_real:
            self.servo.angle = target_angle
        else:
            self.servo_angle = target_angle
        state = "OPEN (Rejecting to Bin)" if open_gate else "CLOSED (Pass-Through)"
        print(f"[ACTUATOR] SG90 Diverter Gate: {state} [{target_angle}°]")

    def illuminate_defect_slot(self, slot_index: int):
        """Illuminates specific pill slot LED (0 to 5) corresponding to physical pill 1-6."""
        if 0 <= slot_index < 6:
            if self.is_real:
                self.leds[slot_index].on()
            else:
                self.led_states[slot_index] = True
            print(f"[ACTUATOR] Pill Slot #{slot_index + 1} Defect LED: ON (GPIO {self.LED_PINS[slot_index]})")

    def clear_all_leds(self):
        """Extinguishes all 6 pill status LEDs."""
        if self.is_real:
            for led in self.leds:
                led.off()
        else:
            self.led_states = [False] * 6
        print("[ACTUATOR] All 6 Pill Defect LEDs: OFF")

    def cleanup(self):
        self.stop_conveyor("SHUTDOWN")
        self.actuate_reject_gate(False)
        self.clear_all_leds()
        if self.is_real:
            self.relay.close()
            self.servo.close()
            for led in self.leds:
                led.close()
        print("[*] Actuator Controller Safely Released.")

if __name__ == "__main__":
    controller = ActuatorController()
    try:
        controller.start_conveyor()
        time.sleep(1.0)
        # Simulate defect event
        controller.stop_conveyor("TEST_DEFECT_TRIGGER")
        controller.actuate_reject_gate(True)
        controller.illuminate_defect_slot(2) # Pill #3 defective
        time.sleep(1.5)
        controller.clear_all_leds()
        controller.actuate_reject_gate(False)
        controller.start_conveyor()
    finally:
        controller.cleanup()
