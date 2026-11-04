"""
Test the IR sensor and the servo on their own, before running the dashboard.

    python hardware_test.py

Stop app.py first. Only one program can use the pins at a time.
"""

import time

from gpiozero import Servo, DigitalInputDevice

import conveyor as cfg


def test_ir():
    ir = DigitalInputDevice(cfg.IR_PIN, pull_up=None, active_state=(not cfg.IR_ACTIVE_LOW))
    print(f"\nIR sensor on GPIO{cfg.IR_PIN}. Move your hand in front of it. Ctrl+C to finish.\n")
    last = None
    try:
        while True:
            state = "OBJECT DETECTED" if ir.is_active else "clear"
            if state != last:
                print(f"  {time.strftime('%H:%M:%S')}  {state}")
                last = state
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("\nDone.")
    finally:
        ir.close()


def test_servo():
    servo = Servo(
        cfg.SERVO_PIN,
        initial_value=None,
        min_pulse_width=cfg.SERVO_MIN_PULSE,
        max_pulse_width=cfg.SERVO_MAX_PULSE,
    )
    speed = cfg.SERVO_SPEED
    print(f"\nServo on GPIO{cfg.SERVO_PIN}, speed {speed}. Make sure it has its own 5 V supply.")
    try:
        for label, value in (("forward", speed), ("reverse", -speed)):
            print(f"  {label} for 3 seconds")
            servo.value = value
            time.sleep(3)
            print("  stop for 1 second")
            servo.detach()
            time.sleep(1)
        print("\nDone. The belt direction used by the dashboard is SERVO_DIRECTION =",
              cfg.SERVO_DIRECTION, "(set -1 in conveyor.py to flip it).")
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        servo.detach()
        servo.close()


if __name__ == "__main__":
    print("1 = IR sensor monitor")
    print("2 = Servo test (forward, stop, reverse, stop)")
    choice = input("Choose 1 or 2: ").strip()
    if choice == "1":
        test_ir()
    elif choice == "2":
        test_servo()
    else:
        print("Nothing to do.")