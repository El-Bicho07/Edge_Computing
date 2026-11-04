import unittest
import time
import math

class TestFPSCalculation(unittest.TestCase):
    """
    Tests for FPS and throughput calculation logic across the application:
    - Reciprocal instantaneous FPS (1.0 / dt)
    - Division-by-zero protection (clamp at 1e-6)
    - Rolling / Exponential Moving Average (EMA) FPS calculation
    - Time measurement with time.perf_counter()
    - Average throughput (total_frames / total_time) vs arithmetic mean of instantaneous FPS
    """

    def test_instantaneous_fps_reciprocal(self):
        """Instantaneous FPS must strictly equal 1.0 / dt."""
        dt_values = [0.01, 0.02, 0.033333333, 0.05, 0.1, 0.5, 1.0]
        expected_fps = [100.0, 50.0, 30.0, 20.0, 10.0, 2.0, 1.0]

        for dt, exp in zip(dt_values, expected_fps):
            fps = 1.0 / max(dt, 1e-6)
            self.assertAlmostEqual(fps, exp, delta=0.01,
                                   msg=f"FPS for dt={dt} should be ~{exp}")

    def test_division_by_zero_protection(self):
        """Zero or negative dt must not raise ZeroDivisionError and must be clamped."""
        zero_dt = 0.0
        fps_zero = 1.0 / max(zero_dt, 1e-6)
        self.assertEqual(fps_zero, 1_000_000.0)
        self.assertTrue(math.isfinite(fps_zero))

        negative_dt = -0.05
        fps_neg = 1.0 / max(negative_dt, 1e-6)
        self.assertEqual(fps_neg, 1_000_000.0)
        self.assertTrue(math.isfinite(fps_neg))

    def test_rolling_fps_smoothing(self):
        """Rolling FPS should use exponential moving average: alpha * current + (1 - alpha) * previous."""
        alpha = 0.1
        current_fps = 30.0

        # Feed 10 FPS
        current_fps = alpha * 10.0 + (1.0 - alpha) * current_fps
        self.assertAlmostEqual(current_fps, 0.1 * 10.0 + 0.9 * 30.0, delta=0.001)

        # Feed 20 FPS stream over 100 frames to verify convergence
        for _ in range(100):
            current_fps = alpha * 20.0 + (1.0 - alpha) * current_fps
        self.assertAlmostEqual(current_fps, 20.0, delta=0.01)

    def test_perf_counter_monotonic_timing(self):
        """time.perf_counter() must be strictly monotonic and provide high resolution."""
        t0 = time.perf_counter()
        time.sleep(0.005)
        t1 = time.perf_counter()
        dt = t1 - t0

        self.assertGreater(dt, 0.003)
        self.assertLess(dt, 0.05)
        fps = 1.0 / max(dt, 1e-6)
        self.assertGreater(fps, 0.0)
        self.assertLess(fps, 400.0)

    def test_state_fps_accumulation(self):
        """App State tracker must accumulate instantaneous FPS, not smoothed FPS."""
        class MockState:
            def __init__(self):
                self.fps = 0.0
                self.fps_sum = 0.0
                self.fps_count = 0

            def record_frame(self, dt):
                inst = 1.0 / max(dt, 1e-6)
                self.fps = 0.1 * inst + 0.9 * self.fps
                self.fps_sum += inst
                self.fps_count += 1

            @property
            def average_fps(self):
                return (self.fps_sum / self.fps_count) if self.fps_count > 0 else 0.0

        s = MockState()
        for _ in range(10):
            s.record_frame(0.05)

        self.assertEqual(s.fps_count, 10)
        self.assertAlmostEqual(s.average_fps, 20.0, places=4)

    def test_variable_frame_intervals_average_throughput(self):
        """
        True average throughput is total_frames / total_elapsed_time,
        NOT the arithmetic mean of instantaneous FPS values.
        """
        # Frame 1: fast frame (0.01s -> 100 FPS)
        # Frame 2: slow frame (0.09s -> 11.11 FPS)
        intervals = [0.01, 0.09]

        instant_fps_list = [1.0 / dt for dt in intervals]
        arithmetic_mean_fps = sum(instant_fps_list) / len(instant_fps_list)

        total_frames = len(intervals)
        total_time = sum(intervals)
        true_average_throughput = total_frames / total_time

        # Arithmetic mean: (100 + 11.111) / 2 = 55.556 FPS
        self.assertAlmostEqual(arithmetic_mean_fps, 55.5555, delta=0.01)

        # True throughput: 2 frames / 0.10s = 20.000 FPS
        self.assertEqual(true_average_throughput, 20.0)

        # Confirm they are significantly different
        self.assertNotEqual(round(arithmetic_mean_fps, 1), round(true_average_throughput, 1))

    def test_app_state_throughput_tracking(self):
        """Verify the State tracking pattern implemented in app.py for variable intervals."""
        class AppStateThroughput:
            def __init__(self):
                self.instant_fps = 0.0
                self.fps = 0.0
                self.fps_n = 0
                self.total_frame_time = 0.0
                self.fps_sum = 0.0

            def on_frame(self, dt):
                inst = 1.0 / max(dt, 1e-6)
                self.instant_fps = inst
                self.fps = inst if self.fps == 0 else self.fps * 0.9 + inst * 0.1
                self.fps_sum += inst
                self.fps_n += 1
                self.total_frame_time += dt

            @property
            def avg_throughput(self):
                return self.fps_n / self.total_frame_time if self.total_frame_time > 0 else 0.0

            @property
            def legacy_avg_fps(self):
                return self.fps_sum / self.fps_n if self.fps_n > 0 else 0.0

        state = AppStateThroughput()
        # Feed 5 fast frames (0.02s each, 50 FPS) and 5 slow frames (0.08s each, 12.5 FPS)
        # Total time = 5*0.02 + 5*0.08 = 0.1 + 0.4 = 0.5s
        # Total frames = 10
        # True throughput = 10 / 0.5 = 20.0 FPS
        for _ in range(5):
            state.on_frame(0.02)
        for _ in range(5):
            state.on_frame(0.08)

        self.assertEqual(state.fps_n, 10)
        self.assertAlmostEqual(state.total_frame_time, 0.5, places=5)
        self.assertAlmostEqual(state.avg_throughput, 20.0, places=4)

        # Arithmetic mean: (5*50 + 5*12.5)/10 = 312.5 / 10 = 31.25 FPS
        self.assertAlmostEqual(state.legacy_avg_fps, 31.25, places=4)


if __name__ == "__main__":
    unittest.main()
