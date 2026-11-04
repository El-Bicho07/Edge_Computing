import unittest
import os

os.environ["MOCK_HARDWARE"] = "1"
from app import assign_slots

def make_pill(cx, cy, w=40, h=40, conf=0.85, defect=False, cls="no defect"):
    """Helper to create detection dictionary."""
    return {
        "cx": cx,
        "cy": cy,
        "w": w,
        "h": h,
        "x1": cx - w / 2,
        "y1": cy - h / 2,
        "x2": cx + w / 2,
        "y2": cy + h / 2,
        "conf": conf,
        "defect": defect,
        "cls": cls,
    }

class TestSlotAssignment(unittest.TestCase):
    """
    Validation of blister pack 6-slot assignment algorithm (assign_slots).
    Grid topology:
        Slot 0 | Slot 1 | Slot 2
        Slot 3 | Slot 4 | Slot 5
    """

    def setUp(self):
        self.width = 640
        self.height = 480
        # Standard centered 2x3 blister pack
        # Row 0 at y=150, Row 1 at y=300 (gap = 150 > 0.6 * 40 = 24)
        # Col 0 at x=120, Col 1 at x=320, Col 2 at x=520 (pitch = 200)
        self.r0_y = 150
        self.r1_y = 300
        self.c0_x = 120
        self.c1_x = 320
        self.c2_x = 520

    def test_scenario_1_six_correct_positions(self):
        """Scenario 1: Standard ideal blister pack with all 6 pills detected."""
        dets = [
            make_pill(self.c0_x, self.r0_y, defect=False), # Slot 0
            make_pill(self.c1_x, self.r0_y, defect=False), # Slot 1
            make_pill(self.c2_x, self.r0_y, defect=False), # Slot 2
            make_pill(self.c0_x, self.r1_y, defect=False), # Slot 3
            make_pill(self.c1_x, self.r1_y, defect=False), # Slot 4
            make_pill(self.c2_x, self.r1_y, defect=False), # Slot 5
        ]
        slots = assign_slots(dets, self.width, self.height)
        self.assertEqual(len(slots), 6)
        for s in range(6):
            self.assertIn(s, slots)
            self.assertFalse(slots[s]["defect"])

    def test_scenario_2_missing_pill_middle_column(self):
        """Scenario 2: Missing pill where outer columns preserve full horizontal span."""
        # Slot 1 and Slot 4 missing (entire middle column missing)
        dets = [
            make_pill(self.c0_x, self.r0_y), # Slot 0
            make_pill(self.c2_x, self.r0_y), # Slot 2
            make_pill(self.c0_x, self.r1_y), # Slot 3
            make_pill(self.c2_x, self.r1_y), # Slot 5
        ]
        slots = assign_slots(dets, self.width, self.height)
        self.assertEqual(set(slots.keys()), {0, 2, 3, 5})
        self.assertNotIn(1, slots)
        self.assertNotIn(4, slots)

    def test_scenario_3_single_defective_pill(self):
        """Scenario 3: One defective pill in slot 4."""
        dets = [
            make_pill(self.c0_x, self.r0_y, defect=False),
            make_pill(self.c1_x, self.r0_y, defect=False),
            make_pill(self.c2_x, self.r0_y, defect=False),
            make_pill(self.c0_x, self.r1_y, defect=False),
            make_pill(self.c1_x, self.r1_y, defect=True, cls="defect"), # Slot 4
            make_pill(self.c2_x, self.r1_y, defect=False),
        ]
        slots = assign_slots(dets, self.width, self.height)
        self.assertEqual(len(slots), 6)
        self.assertTrue(slots[4]["defect"])
        for s in [0, 1, 2, 3, 5]:
            self.assertFalse(slots[s]["defect"])

    def test_scenario_4_multiple_defective_pills(self):
        """Scenario 4: Multiple defective pills in slots 0, 2, and 5."""
        dets = [
            make_pill(self.c0_x, self.r0_y, defect=True, cls="defect"), # 0
            make_pill(self.c1_x, self.r0_y, defect=False),
            make_pill(self.c2_x, self.r0_y, defect=True, cls="defect"), # 2
            make_pill(self.c0_x, self.r1_y, defect=False),
            make_pill(self.c1_x, self.r1_y, defect=False),
            make_pill(self.c2_x, self.r1_y, defect=True, cls="defect"), # 5
        ]
        slots = assign_slots(dets, self.width, self.height)
        self.assertTrue(slots[0]["defect"])
        self.assertFalse(slots[1]["defect"])
        self.assertTrue(slots[2]["defect"])
        self.assertFalse(slots[3]["defect"])
        self.assertFalse(slots[4]["defect"])
        self.assertTrue(slots[5]["defect"])

    def test_scenario_5_duplicate_detections_same_slot(self):
        """Scenario 5: Two detections for Slot 1; higher confidence must be selected."""
        dets = [
            make_pill(self.c0_x, self.r0_y, conf=0.8),
            make_pill(self.c1_x, self.r0_y, conf=0.6, defect=False), # Lower conf
            make_pill(self.c1_x + 2, self.r0_y - 2, conf=0.92, defect=True), # Higher conf
            make_pill(self.c2_x, self.r0_y, conf=0.85),
            make_pill(self.c0_x, self.r1_y, conf=0.88),
            make_pill(self.c1_x, self.r1_y, conf=0.84),
            make_pill(self.c2_x, self.r1_y, conf=0.89),
        ]
        slots = assign_slots(dets, self.width, self.height)
        self.assertEqual(len(slots), 6)
        self.assertEqual(slots[1]["conf"], 0.92)
        self.assertTrue(slots[1]["defect"])

    def test_scenario_6_overlapping_bounding_boxes(self):
        """Scenario 6: Overlapping bounding boxes clustered around a single pill."""
        dets = [
            make_pill(self.c0_x, self.r0_y, conf=0.75, defect=False),
            make_pill(self.c0_x + 3, self.r0_y + 3, conf=0.95, defect=True),
        ]
        # Should assign to slot 0 and pick highest confidence
        slots = assign_slots(dets, self.width, self.height)
        self.assertIn(0, slots)
        self.assertEqual(slots[0]["conf"], 0.95)
        self.assertTrue(slots[0]["defect"])

    def test_scenario_7_shifted_blister_pack(self):
        """Scenario 7: Shifted blister pack (translated by dx=+100, dy=+60)."""
        dx, dy = 100, 60
        dets = [
            make_pill(self.c0_x + dx, self.r0_y + dy),
            make_pill(self.c1_x + dx, self.r0_y + dy),
            make_pill(self.c2_x + dx, self.r0_y + dy),
            make_pill(self.c0_x + dx, self.r1_y + dy),
            make_pill(self.c1_x + dx, self.r1_y + dy),
            make_pill(self.c2_x + dx, self.r1_y + dy),
        ]
        slots = assign_slots(dets, self.width, self.height)
        self.assertEqual(len(slots), 6)
        self.assertEqual(set(slots.keys()), {0, 1, 2, 3, 4, 5})

    def test_scenario_8_partially_visible_top_row(self):
        """Scenario 8: Partially visible blister pack (only top row in frame)."""
        dets = [
            make_pill(self.c0_x, 100),
            make_pill(self.c1_x, 100),
            make_pill(self.c2_x, 100),
        ]
        # Since avg_cy is 100 < height/2 (240), assigned to row 0 (slots 0, 1, 2)
        slots = assign_slots(dets, self.width, self.height)
        self.assertEqual(set(slots.keys()), {0, 1, 2})

    def test_scenario_9_rotated_pack_algorithmic_limitation(self):
        """
        Scenario 9: Rotated blister pack.
        Demonstrate that:
        1. Small rotations (e.g. 5 degrees) are tolerated and correctly yield all 6 slots {0..5}.
        2. Severe rotations (e.g. 45 degrees) break Cartesian axis-alignment, causing vertical/horizontal
           projection collapse, collision of centroids, and failure to recover all 6 discrete slots.
        """
        import math

        def create_rotated_pack(deg):
            angle = math.radians(deg)
            cx_mid, cy_mid = 320, 240
            orig_points = [
                (self.c0_x, self.r0_y), (self.c1_x, self.r0_y), (self.c2_x, self.r0_y),
                (self.c0_x, self.r1_y), (self.c1_x, self.r1_y), (self.c2_x, self.r1_y)
            ]
            dets = []
            for ox, oy in orig_points:
                rx = cx_mid + (ox - cx_mid) * math.cos(angle) - (oy - cy_mid) * math.sin(angle)
                ry = cy_mid + (ox - cx_mid) * math.sin(angle) + (oy - cy_mid) * math.cos(angle)
                dets.append(make_pill(rx, ry))
            return dets

        # 1. Tolerable rotation (5 deg): Successfully resolves all 6 slots
        dets_5deg = create_rotated_pack(5)
        slots_5deg = assign_slots(dets_5deg, self.width, self.height)
        self.assertEqual(set(slots_5deg.keys()), {0, 1, 2, 3, 4, 5},
                         "Minor 5-degree tilt must maintain correct 6-slot partitioning")

        # 2. Severe rotation (45 deg): Fails to partition into 6 discrete slots
        dets_45deg = create_rotated_pack(45)
        slots_45deg = assign_slots(dets_45deg, self.width, self.height)
        self.assertNotEqual(set(slots_45deg.keys()), {0, 1, 2, 3, 4, 5},
                            "45-degree rotation is expected to break axis-aligned slot assignment")
        self.assertLess(len(slots_45deg), 6,
                        "45-degree tilt causes centroid collision, losing discrete slot assignments")


if __name__ == "__main__":
    unittest.main()
