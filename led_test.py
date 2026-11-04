from gpiozero import LED
from time import sleep

LED_PINS = [17, 27, 22, 23, 24, 25]

leds = [LED(pin) for pin in LED_PINS]

print("Testing 6 LEDs...")

for i, led in enumerate(leds):
    print(f"LED {i + 1} ON")
    led.on()
    sleep(1)
    led.off()

print("Testing all LEDs together...")

for led in leds:
    led.on()

sleep(2)

for led in leds:
    led.off()

print("LED test complete.")