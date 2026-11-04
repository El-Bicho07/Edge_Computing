from gpiozero import AngularServo
from time import sleep

SERVO_GPIO = 18  # BCM GPIO18, physical pin 12

servo = None

try:
    servo = AngularServo(
        SERVO_GPIO,
        min_angle=0,
        max_angle=180,
        min_pulse_width=0.001,
        max_pulse_width=0.002,
        frame_width=0.020
    )




    print("Servo test started.")

    for angle in (0, 30, 60, 90, 60, 30, 0):
        print(f"Moving to {angle} degrees")
        servo.angle = angle
        sleep(1)

    print("Test complete.")

except KeyboardInterrupt:
    print("Test stopped by user.")

finally:
    if servo is not None:
        servo.close()
    print("GPIO released.")