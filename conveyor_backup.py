"""
Conveyor belt control: continuous-rotation servo motor + IR object sensor.

Rule
    IR sensor sees an object  -> the motor stops
    otherwise                 -> the motor runs

Wiring (Raspberry Pi 5, BCM numbers)
    Servo signal (orange/yellow)  -> GPIO18   (physical pin 12)
    Servo power  (red)            -> separate 5 V supply, NOT the Pi
    Servo ground (brown/black)    -> supply ground AND a Pi GND pin (common ground)
    IR sensor OUT                 -> GPIO5    (physical pin 29)
    IR sensor VCC                 -> 3.3 V    (physical pin 1)   <- 3.3 V, not 5 V
    IR sensor GND                 -> Pi GND   (physical pin 9)

What the servo can report
    A hobby servo has no feedback wire. The values stored are what the program
    commanded: running or stopped, speed, run time, and how many times it stopped.
"""

import threading
import time

# =========================================================
# SETTINGS
# =========================================================

SERVO_PIN = 18
IR_PIN = 5

# Most IR obstacle modules (FC-51 and similar) pull OUT to LOW when they see an object.
# If the dashboard shows "Object" when nothing is there, change this to False.
IR_ACTIVE_LOW = True

# Continuous-rotation servo.
SERVO_SPEED = 0.4            # 0.1 (slowest) to 1.0 (fastest). Slow is easier to inspect.
SERVO_DIRECTION = 1          # 1 or -1. Change to -1 if the belt moves the wrong way.
SERVO_MIN_PULSE = 1.0 / 1000
SERVO_MAX_PULSE = 2.0 / 1000

# What happens after an object is seen.
#   3.0 = the belt stays stopped for 3 seconds (time for the camera to inspect),
#         then runs again. It also runs again at once if the object is taken away.
#   0   = the belt stays stopped for as long as the sensor sees an object.
STOP_HOLD_SECONDS = 3.0

# After the belt restarts, the sensor is ignored until it has seen "clear" once,
# so the same pack is not counted twice. If it is still blocked after this many
# seconds, the sensor is re-armed anyway.
RESUME_MAX_BLOCKED_S = 8.0

# Sensor noise filter.
IR_DEBOUNCE_ON_S = 0.05      # object must be seen this long to count
IR_DEBOUNCE_OFF_S = 0.15     # and gone this long to count as clear

SAMPLE_INTERVAL_S = 1.0      # one row per second goes to the database
FLUSH_INTERVAL_S = 3.0       # how often queued rows are written to disk
LOOP_INTERVAL_S = 0.02       # control loop: 50 times per second


class Conveyor:

    def __init__(self, db):
        self.db = db
        self.lock = threading.RLock()

        self.servo = None
        self.ir = None
        self.hardware = False
        self.hardware_error = None
        self._init_hardware()

        self.mode = "stop"                 # "auto" or "stop". Starts stopped for safety.
        self.state = "manual"              # "manual", "run" or "hold"
        self.reason = "Waiting for the operator"
        self.motor_on = False
        self.motor_since = time.monotonic()
        self.run_total = 0.0

        self.object_present = False
        self._raw = False
        self._raw_since = time.monotonic()
        self._sim_ir = None                # lets tests fake the sensor

        self.armed = True
        self.run_started = 0.0
        self.hold_start = 0.0

        self.stops = 0
        self.objects_today = db.count_events_today("motor_stop", "Object detected")
        self.events_seq = 0

        self._stop_evt = threading.Event()
        self._thread = None

    # -----------------------------------------------------
    # hardware
    # -----------------------------------------------------

    def _init_hardware(self):
        try:
            from gpiozero import Servo, DigitalInputDevice

            self.servo = Servo(
                SERVO_PIN,
                initial_value=None,                 # no pulses = servo stays still
                min_pulse_width=SERVO_MIN_PULSE,
                max_pulse_width=SERVO_MAX_PULSE,
            )
            self.ir = DigitalInputDevice(
                IR_PIN, pull_up=None, active_state=(not IR_ACTIVE_LOW)
            )
            self.hardware = True
            print(f"Conveyor hardware ready: servo GPIO{SERVO_PIN}, IR sensor GPIO{IR_PIN}")
        except Exception as e:
            self.hardware = False
            self.hardware_error = str(e)
            print("WARNING: conveyor hardware unavailable:", e)
            print("         The conveyor runs in simulation (the motor does not move).")
            for dev in (self.servo, self.ir):
                try:
                    if dev is not None:
                        dev.close()
                except Exception:
                    pass
            self.servo = None
            self.ir = None

    def _read_ir(self):
        if self._sim_ir is not None:
            return bool(self._sim_ir)
        if self.ir is not None:
            try:
                return bool(self.ir.is_active)
            except Exception:
                return False
        return False

    def _drive(self, on):
        if self.servo is None:
            return
        try:
            if on:
                self.servo.value = max(-1.0, min(1.0, SERVO_DIRECTION * SERVO_SPEED))
            else:
                self.servo.detach()      # stop sending pulses: the servo stops, no hum
        except Exception as e:
            self.hardware_error = f"servo error: {e}"
            print("Servo error:", e)

    # -----------------------------------------------------
    # logging helpers
    # -----------------------------------------------------

    def _log(self, event, detail=""):
        self.db.add_event(event, detail)
        self.events_seq += 1

    def _motor(self, on, reason):
        with self.lock:
            self.reason = reason
            if on == self.motor_on:
                return
            now = time.monotonic()
            if self.motor_on:
                self.run_total += now - self.motor_since
            self.motor_on = on
            self.motor_since = now
            self._drive(on)
            self._log("motor_start" if on else "motor_stop", reason)

    # -----------------------------------------------------
    # operator commands
    # -----------------------------------------------------

    def set_mode(self, mode):
        with self.lock:
            now = time.monotonic()
            if mode == "auto":
                if self.mode == "auto":
                    return
                self.mode = "auto"
                self.state = "run"
                self.armed = True
                self.run_started = now
                self._log("mode_auto", "Operator started the conveyor")
            elif mode == "stop":
                if self.mode == "stop" and not self.motor_on:
                    return
                self.mode = "stop"
                self.state = "manual"
                self._log("mode_stop", "Operator stopped the conveyor")
                self._motor(False, "Operator stopped the conveyor")

    # -----------------------------------------------------
    # control logic
    # -----------------------------------------------------

    def _debounce(self, raw, now):
        if raw != self._raw:
            self._raw = raw
            self._raw_since = now
        stable = now - self._raw_since

        if raw and not self.object_present and stable >= IR_DEBOUNCE_ON_S:
            self.object_present = True
            self._log("ir_object", "IR sensor sees an object")
        elif (not raw) and self.object_present and stable >= IR_DEBOUNCE_OFF_S:
            self.object_present = False
            self._log("ir_clear", "IR sensor is clear")

    def _step(self, now):
        with self.lock:
            if self.mode != "auto":
                if self.motor_on:
                    self._motor(False, "Operator stopped the conveyor")
                return

            if self.state == "hold":
                removed = not self.object_present
                timed_out = (STOP_HOLD_SECONDS > 0
                             and now - self.hold_start >= STOP_HOLD_SECONDS)
                if removed or timed_out:
                    self.state = "run"
                    self.armed = False
                    self.run_started = now
                    self._motor(True, "Object removed" if removed else "Inspection time finished")
                return

            # state == "run"
            if (not self.armed and
                    (not self.object_present
                     or now - self.run_started >= RESUME_MAX_BLOCKED_S)):
                self.armed = True

            if self.armed and self.object_present:
                self.state = "hold"
                self.hold_start = now
                self.stops += 1
                self.objects_today += 1
                self._motor(False, "Object detected by the IR sensor")
                return

            if not self.motor_on:
                self._motor(True, "Path is clear")

    def _loop(self):
        next_sample = 0.0
        next_flush = time.monotonic() + FLUSH_INTERVAL_S
        last_error = 0.0

        while not self._stop_evt.is_set():
            now = time.monotonic()
            try:
                with self.lock:
                    self._debounce(self._read_ir(), now)
                    self._step(now)

                    if now >= next_sample:
                        next_sample = now + SAMPLE_INTERVAL_S
                        self.db.queue_sample(self.motor_on, SERVO_SPEED, self.object_present)

                if now >= next_flush:
                    next_flush = now + FLUSH_INTERVAL_S
                    self.db.flush()
            except Exception as e:
                if now - last_error > 5:
                    print("Conveyor loop error:", e)
                    last_error = now

            time.sleep(LOOP_INTERVAL_S)

    # -----------------------------------------------------
    # start, stop, status
    # -----------------------------------------------------

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._log("system_start", "Conveyor controller started")
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def shutdown(self):
        self._stop_evt.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        with self.lock:
            self.mode = "stop"
            self.state = "manual"
            if self.motor_on:
                self._motor(False, "Program closed")
            self._log("system_stop", "Conveyor controller stopped")
        self.db.flush()
        for dev in (self.servo, self.ir):
            try:
                if dev is not None:
                    dev.close()
            except Exception:
                pass

    def status(self):
        with self.lock:
            now = time.monotonic()
            run_seconds = self.run_total + ((now - self.motor_since) if self.motor_on else 0.0)

            hold_left = None
            if self.state == "hold" and STOP_HOLD_SECONDS > 0:
                hold_left = max(0.0, STOP_HOLD_SECONDS - (now - self.hold_start))

            return {
                "hardware": self.hardware,
                "hardware_error": self.hardware_error,
                "mode": self.mode,
                "state": self.state,
                "motor": "running" if self.motor_on else "stopped",
                "reason": self.reason,
                "speed": SERVO_SPEED,
                "direction": SERVO_DIRECTION,
                "object_present": self.object_present,
                "objects_today": self.objects_today,
                "stops": self.stops,
                "run_seconds": round(run_seconds, 1),
                "hold_seconds": STOP_HOLD_SECONDS,
                "hold_remaining_s": None if hold_left is None else round(hold_left, 1),
                "events_seq": self.events_seq,
                "pins": {"servo": SERVO_PIN, "ir": IR_PIN},
            }