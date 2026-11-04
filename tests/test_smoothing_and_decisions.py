import unittest
import os
import time
from collections import deque

os.environ["MOCK_HARDWARE"] = "1"
from app import S, smooth_pills, track_pack, SMOOTH_FRAMES, PILL_COUNT, SLOT_MIN_PRESENT, MIN_FRAMES_TO_LOG, MIN_PACK_SECONDS, ABSENT_SECONDS

class TestSmoothingAndDecisions(unittest.TestCase):
    """
    Tests for temporal pill voting (smooth_pills) and pack session state tracking (track_pack):
    - Majority voting with tie handling (tie counts as defect)
    - Minimum presence threshold before reporting
    - State clearance across packs to prevent defect leakage
    - Fail-safe rejection of incomplete packs with detected defects
    """

    def setUp(self):
        # Reset global state S before each test
        with S.lock:
            S.slot_hist = [deque(maxlen=SMOOTH_FRAMES) for _ in range(PILL_COUNT)]
            S.session = None
            S.history = []
            S.n_pass = 0
            S.n_defect = 0
            S.seq = 0

    def test_smooth_pills_min_presence_filter(self):
        """Slots with fewer than SLOT_MIN_PRESENT (2) frames in history are ignored."""
        slots = {0: {"defect": False, "conf": 0.9, "cls": "no defect",
                     "x1": 10, "y1": 10, "x2": 50, "y2": 50}}
        # 1 frame only
        with S.lock:
            pills = smooth_pills(slots)
        self.assertEqual(len(pills), 0)

        # 2nd frame
        with S.lock:
            pills = smooth_pills(slots)
        self.assertEqual(len(pills), 1)
        self.assertEqual(pills[0]["pill"], 1)

    def test_smooth_pills_tie_counts_as_defect(self):
        """When defect and non-defect votes are tied (e.g., 2 vs 2), vote resolves to DEFECT."""
        # Frame 1 & 2: defect = False
        good = {0: {"defect": False, "conf": 0.9, "cls": "no defect", "x1": 10, "y1": 10, "x2": 50, "y2": 50}}
        # Frame 3 & 4: defect = True
        bad = {0: {"defect": True, "conf": 0.8, "cls": "defect", "x1": 10, "y1": 10, "x2": 50, "y2": 50}}

        with S.lock:
            smooth_pills(good)
            smooth_pills(good)
            smooth_pills(bad)
            pills = smooth_pills(bad)

        self.assertEqual(len(pills), 1)
        # votes=2, len(present)=4 -> votes*2 >= 4 -> True
        self.assertTrue(pills[0]["defect"])

    def test_pack_tracking_pass_decision(self):
        """A complete blister pack without defects should result in PASS."""
        now = time.time()
        good_pills = [
            {"pill": i + 1, "cls": "no defect", "conf": 0.95, "defect": False, "box": (0, 0, 10, 10)}
            for i in range(6)
        ]

        with S.lock:
            # Simulate frames meeting MIN_FRAMES_TO_LOG and MIN_PACK_SECONDS
            for f in range(MIN_FRAMES_TO_LOG + 2):
                track_pack(now + f * 0.1, good_pills)

        self.assertEqual(S.n_pass, 1)
        self.assertEqual(S.n_defect, 0)
        self.assertEqual(len(S.history), 1)
        self.assertEqual(S.history[0]["result"], "PASS")

    def test_pack_tracking_defect_decision(self):
        """A blister pack with persistent defects should result in DEFECT."""
        now = time.time()
        defective_pills = [
            {"pill": 1, "cls": "defect", "conf": 0.90, "defect": True, "box": (0, 0, 10, 10)},
            {"pill": 2, "cls": "no defect", "conf": 0.95, "defect": False, "box": (0, 0, 10, 10)},
        ]

        with S.lock:
            for f in range(MIN_FRAMES_TO_LOG + 2):
                track_pack(now + f * 0.1, defective_pills)

        self.assertEqual(S.n_defect, 1)
        self.assertEqual(S.n_pass, 0)
        self.assertEqual(S.history[0]["result"], "DEFECT")
        self.assertIn("1", S.history[0]["pills"])

    def test_state_isolation_between_consecutive_packs(self):
        """New pack session must clear slot history to avoid defect leakage from previous pack."""
        with S.lock:
            # Fill slot 0 history with defects
            for _ in range(SMOOTH_FRAMES):
                S.slot_hist[0].append((True, 0.99, "defect", (0, 0, 10, 10)))
            self.assertEqual(len(S.slot_hist[0]), SMOOTH_FRAMES)

            # Starting a new pack session with track_pack() clears slot_hist
            now = time.time()
            track_pack(now, [{"pill": 1, "cls": "no defect", "conf": 0.9, "defect": False, "box": (0, 0, 10, 10)}])

            # History of slot 0 should now be cleared
            self.assertEqual(len(S.slot_hist[0]), 0)

    def test_failsafe_departure_incomplete_pack_with_defect(self):
        """If an incomplete pack departs with observed defect frames, it must be logged as DEFECT."""
        now = time.time()
        defective_pills = [
            {"pill": 1, "cls": "defect", "conf": 0.88, "defect": True, "box": (0, 0, 10, 10)}
        ]

        with S.lock:
            # Only 2 frames (fewer than MIN_FRAMES_TO_LOG=5)
            track_pack(now, defective_pills)
            track_pack(now + 0.05, defective_pills)
            self.assertEqual(len(S.history), 0) # Not yet logged

            # Pack departs: absent for longer than ABSENT_SECONDS
            departure_time = now + ABSENT_SECONDS + 1.0
            track_pack(departure_time, [])

            # Must have logged as DEFECT
            self.assertEqual(len(S.history), 1)
            self.assertEqual(S.history[0]["result"], "DEFECT")
            self.assertEqual(S.n_defect, 1)


if __name__ == "__main__":
    unittest.main()

