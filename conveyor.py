"""
Conveyor control for Raspberry Pi 5, positional SG90 servo, and IR sensor.

Behavior:
- Dashboard Run: reset the SG90 to 0 degrees, then sweep between 0 and 180 degrees.
- No object detected: keep sweeping.
- Object detected: stop sweeping and hold the current angle.
- Object removed: resume sweeping.
- Dashboard Stop: stop sweeping and hold the current angle.

IMPORTANT:
A standard SG90 is a positional servo. It swings between angles; it does NOT
rotate continuously like a conveyor-belt motor. Use a geared DC motor and driver
if the physical conveyor belt must move continuously.
"""

import threading
import time

# =========================================================
# SETTINGS
# =========================================================

SERVO_PIN = 18  # BCM GPIO18, physical pin 12
IR_PIN = 5      # BCM GPIO5, physical pin 29

# Most FC-51-style IR modules output LOW when an object is detected.
IR_ACTIVE_LOW = True

SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180
SERVO_INITIAL_ANGLE = 0

# Servo sweeps by this many degrees at each step.
SWEEP_STEP_DEGREES = 5
SWEEP_INTERVAL_S = 0.10

# 0 means keep stopped for as long as the sensor sees an object.
STOP_HOLD_SECONDS = 0.0

# Sensor debounce settings
IR_DEBOUNCE_ON_S = 0.05
IR_DEBOUNCE_OFF_S = 0.15

# Database sampling / loop settings
SAMPLE_INTERVAL_S = 1.0
FLUSH_INTERVAL_S = 3.0
LOOP_INTERVAL_S = 0.02

# Kept for compatibility with the existing dashboard/database sample schema.
# This is NOT the physical speed of a positional SG90.
SERVO_SPEED = 0.4


class Conveyor:
    def __init__(self, db):
        self.db = db
        self.lock = threading.RLock()

        self.servo = None
        self.ir = None
        self.hardware = False
        self.hardware_error = None
        self._init_hardware()

        self.mode = "stop"       # "auto" or "stop"
        self.state = "manual"    # "manual", "run" or "hold"
        self.reason = "Waiting for the operator"
        self.motor_on = False
        self.motor_since = time.monotonic()
        self.run_total = 0.0

        self.current_angle = SERVO_INITIAL_ANGLE
        self.sweep_direction = 1
        self.last_sweep_step = time.monotonic()

        self.object_present = False
        self._raw = False
        self._raw_since = time.monotonic()
        self._sim_ir = None

        self.armed = True
        self.run_started = 0.0
        self.hold_start = 0.0

        self.stops = 0
        self.objects_today = db.count_events_today(
            "motor_stop", "Object detected"
        )
        self.events_seq = 0

        self._stop_evt = threading.Event()
        self._thread = None

    # -----------------------------------------------------
    # Hardware
    # -----------------------------------------------------

    def _init_hardware(self):
        try:
            from gpiozero import AngularServo, DigitalInputDevice

            self.servo = AngularServo(
                SERVO_PIN,
                initial_angle=SERVO_INITIAL_ANGLE,
                min_angle=SERVO_MIN_ANGLE,
                max_angle=SERVO_MAX_ANGLE,
                min_pulse_width=0.001,
                max_pulse_width=0.002,
                frame_width=0.020,
            )

            self.ir = DigitalInputDevice(
                IR_PIN,
                pull_up=None,
                active_state=(not IR_ACTIVE_LOW),
            )

            self.hardware = True
            self.current_angle = SERVO_INITIAL_ANGLE
            print(
                f"Conveyor hardware ready: positional SG90 GPIO{SERVO_PIN}, "
                f"IR sensor GPIO{IR_PIN}"
            )
        except Exception as e:
            self.hardware = False
            self.hardware_error = str(e)
            print("WARNING: conveyor hardware unavailable:", e)
            print("         The conveyor runs in simulation (no servo movement).")
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

    def _set_angle(self, angle):
        """Set a safe servo angle and remember the commanded position."""
        angle = max(SERVO_MIN_ANGLE, min(SERVO_MAX_ANGLE, float(angle)))
        self.current_angle = angle
        if self.servo is not None:
            try:
                self.servo.angle = angle
            except Exception as e:
                self.hardware_error = f"servo angle error: {e}"
                print("Servo angle error:", e)

    def _motor(self, on, reason):
        """Update logical run/stop state and log transitions."""
        with self.lock:
            self.reason = reason
            if on == self.motor_on:
                return

            now = time.monotonic()
            if self.motor_on:
                self.run_total += now - self.motor_since

            self.motor_on = on
            self.motor_since = now
            self.last_sweep_step = now
            self.db.add_event(
                "motor_start" if on else "motor_stop",
                reason,
            )
            self.events_seq += 1

    # -----------------------------------------------------
    # Logging helpers
    # -----------------------------------------------------

    def _log(self, event, detail=""):
        self.db.add_event(event, detail)
        self.events_seq += 1

    # -----------------------------------------------------
    # Operator commands
    # -----------------------------------------------------

    def set_mode(self, mode):
        with self.lock:
            now = time.monotonic()

            if mode == "auto":
                if self.mode == "auto":
                    return

                # Every fresh Run starts at the initial position.
                self._set_angle(SERVO_INITIAL_ANGLE)
                self.sweep_direction = 1
                self.last_sweep_step = now

                self.mode = "auto"
                self.state = "run"
                self.armed = True
                self.run_started = now
                self._log("mode_auto", "Operator started the servo sweep")

            elif mode == "stop":
                if self.mode == "stop" and not self.motor_on:
                    return

                self.mode = "stop"
                self.state = "manual"
                self._log("mode_stop", "Operator stopped the servo sweep")
                self._motor(False, "Operator stopped the servo sweep")
                # Do not keep changing the angle; the servo stays at its
                # last commanded position while Stop is selected.

    # -----------------------------------------------------
    # Sensor debounce and control logic
    # -----------------------------------------------------

    def _debounce(self, raw, now):
        if raw != self._raw:
            self._raw = raw
            self._raw_since = now

        stable = now - self._raw_since

        if raw and not self.object_present and stable >= IR_DEBOUNCE_ON_S:
            self.object_present = True
            self._log("ir_object", "IR sensor sees an object")

        elif (
            not raw
            and self.object_present
            and stable >= IR_DEBOUNCE_OFF_S
        ):
            self.object_present = False
            self._log("ir_clear", "IR sensor is clear")

    def _step(self, now):
        with self.lock:
            if self.mode != "auto":
                if self.motor_on:
                    self._motor(False, "Operator stopped the servo sweep")
                return

            if self.state == "hold":
                removed = not self.object_present
                timed_out = (
                    STOP_HOLD_SECONDS > 0
                    and now - self.hold_start >= STOP_HOLD_SECONDS
                )

                if removed or timed_out:
                    self.state = "run"
                    self.armed = False
                    self.run_started = now
                    self._motor(
                        True,
                        "Object removed" if removed else "Inspection time finished",
                    )
                return

            # State is "run".
            if not self.armed and (
                not self.object_present
                or now - self.run_started >= 8.0
            ):
                self.armed = True

            if self.armed and self.object_present:
                self.state = "hold"
                self.hold_start = now
                self.stops += 1
                self.objects_today += 1
                self._motor(False, "Object detected by the IR sensor")
                return

            if not self.motor_on:
                self._motor(True, "No object detected; servo sweeping")

            # Sweep only while running and no object is being held for inspection.
            if self.motor_on and now - self.last_sweep_step >= SWEEP_INTERVAL_S:
                next_angle = self.current_angle + (
                    self.sweep_direction * SWEEP_STEP_DEGREES
                )

                if next_angle >= SERVO_MAX_ANGLE:
                    next_angle = SERVO_MAX_ANGLE
                    self.sweep_direction = -1
                elif next_angle <= SERVO_MIN_ANGLE:
                    next_angle = SERVO_MIN_ANGLE
                    self.sweep_direction = 1

                self._set_angle(next_angle)
                self.last_sweep_step = now

    # -----------------------------------------------------
    # Background loop
    # -----------------------------------------------------

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
                        self.db.queue_sample(
                            self.motor_on,
                            SERVO_SPEED,
                            self.object_present,
                        )

                if now >= next_flush:
                    next_flush = now + FLUSH_INTERVAL_S
                    self.db.flush()

            except Exception as e:
                if now - last_error > 5:
                    print("Conveyor loop error:", e)
                    last_error = now

            time.sleep(LOOP_INTERVAL_S)

    # -----------------------------------------------------
    # Start, stop, status
    # -----------------------------------------------------

    def start(self):
        if self._thread and self._thread.is_alive():
            return

        self._stop_evt.clear()
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
            try:
                self.db.flush()
            except Exception:
                pass

        for dev in (self.servo, self.ir):
            try:
                if dev is not None:
                    dev.close()
            except Exception:
                pass

    def status(self):
        with self.lock:
            now = time.monotonic()
            run_seconds = self.run_total + (
                (now - self.motor_since) if self.motor_on else 0.0
            )

            hold_left = None
            if self.state == "hold" and STOP_HOLD_SECONDS > 0:
                hold_left = max(
                    0.0,
                    STOP_HOLD_SECONDS - (now - self.hold_start),
                )

            return {
                "hardware": self.hardware,
                "hardware_error": self.hardware_error,
                "mode": self.mode,
                "state": self.state,
                "motor": "running" if self.motor_on else "stopped",
                "reason": self.reason,
                "speed": SERVO_SPEED,
                "direction": self.sweep_direction,
                "angle": round(self.current_angle, 1),
                "object_present": self.object_present,
                "objects_today": self.objects_today,
                "stops": self.stops,
                "run_seconds": round(run_seconds, 1),
                "hold_seconds": STOP_HOLD_SECONDS,
                "hold_remaining_s": (
                    None if hold_left is None else round(hold_left, 1)
                ),
                "events_seq": self.events_seq,
                "pins": {"servo": SERVO_PIN, "ir": IR_PIN},
            }
