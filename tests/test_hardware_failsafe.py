import unittest
import os
import tempfile
from unittest.mock import MagicMock

# Force MOCK_HARDWARE=1 for failsafe testing
os.environ["MOCK_HARDWARE"] = "1"
from conveyor import Conveyor, SERVO_MIN_ANGLE, SERVO_MAX_ANGLE
from database import Database

class TestHardwareFailsafe(unittest.TestCase):
    """
    Tests for hardware failsafe behavior, simulation fallback, and actuator safety:
    - MOCK_HARDWARE=1 suppresses real GPIO and pigpio initialization
    - Conveyor status accurately tags simulation mode
    - Conveyor motor transitions prepend [SIMULATION] when in mock mode
    - Servo angle clamping enforces 0 <= angle <= 180 degrees
    - Graceful error recovery if actuators fail
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_failsafe.db")
        self.db = Database(self.db_path)
        self.conveyor = Conveyor(self.db)

    def tearDown(self):
        self.conveyor.close()
        self.db.close()
        self.temp_dir.cleanup()

    def test_mock_hardware_mode_active(self):
        """Under MOCK_HARDWARE=1, physical hardware is disabled."""
        self.assertFalse(self.conveyor.hardware)
        self.assertIsNone(self.conveyor.servo)
        self.assertIsNone(self.conveyor.ir)
        self.assertIn("simulation", self.conveyor.hardware_error.lower())

        st = self.conveyor.status()
        self.assertFalse(st["hardware"])
        self.assertTrue(st["simulation"])

    def test_motor_event_simulation_tagging(self):
        """In simulation mode, motor events must be tagged with [SIMULATION]."""
        self.conveyor._motor(True, "testing start")
        self.conveyor._motor(False, "testing stop")

        events = self.db.events(limit=5)
        self.assertEqual(len(events), 2)
        self.assertTrue(events[0]["detail"].startswith("[SIMULATION]"))
        self.assertTrue(events[1]["detail"].startswith("[SIMULATION]"))

    def test_servo_angle_clamping(self):
        """Servo angles must strictly clamp to SERVO_MIN_ANGLE and SERVO_MAX_ANGLE."""
        # Overshoot high (e.g. 250 degrees)
        self.conveyor._set_angle(250.0)
        self.assertEqual(self.conveyor.current_angle, SERVO_MAX_ANGLE)

        # Overshoot low (e.g. -45 degrees)
        self.conveyor._set_angle(-45.0)
        self.assertEqual(self.conveyor.current_angle, SERVO_MIN_ANGLE)

        # Within safe range
        self.conveyor._set_angle(75.5)
        self.assertEqual(self.conveyor.current_angle, 75.5)

    def test_servo_hardware_error_handling(self):
        """If hardware servo throws an exception on actuation, the system catches it gracefully."""
        class FaultyServo:
            def __init__(self):
                self._angle = 0.0

            @property
            def angle(self):
                return self._angle

            @angle.setter
            def angle(self, val):
                raise RuntimeError("I/O error communicating with servo")

        self.conveyor.servo = FaultyServo()
        self.conveyor._set_angle(90)
        self.assertIn("servo angle error", self.conveyor.hardware_error)

    def test_safe_shutdown(self):
        """stop() and close() should be idempotent and safely set mode to stop."""
        self.conveyor.set_mode("auto")
        self.conveyor.stop()
        self.assertEqual(self.conveyor.mode, "stop")
        self.assertFalse(self.conveyor.motor_on)

        # Multiple close calls should not throw
        self.conveyor.close()
        self.conveyor.close()


if __name__ == "__main__":
    unittest.main()
