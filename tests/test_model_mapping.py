import unittest
import os
import yaml
import sys

# Ensure MOCK_HARDWARE is active before importing app
os.environ["MOCK_HARDWARE"] = "1"
from app import is_defect_class, EXPECTED_CLASS_MAPPING

class TestModelMapping(unittest.TestCase):
    """
    Tests for model checkpoint class mappings and validation logic:
    - Expected production mapping: {0: 'defect', 1: 'no defect'}
    - best.pt inverted mapping: {0: 'NoDefect', 1: 'defect'}
    - Strict validation enforcing expected class order and rejecting inverted checkpoints
    - is_defect_class() normalization and matching
    - NCNN metadata alignment with production model
    """

    def setUp(self):
        self.best1_names = {0: "NoDefect", 1: "defect"}
        self.best2_names = {0: "defect", 1: "no defect"}

    def test_best1_mapping(self):
        """In best.pt, 0 is NoDefect (good) and 1 is defect (bad)."""
        self.assertFalse(is_defect_class(0, self.best1_names))
        self.assertTrue(is_defect_class(1, self.best1_names))

    def test_best2_mapping(self):
        """In best2.pt, 0 is defect (bad) and 1 is no defect (good)."""
        self.assertTrue(is_defect_class(0, self.best2_names))
        self.assertFalse(is_defect_class(1, self.best2_names))

    def test_production_expected_class_mapping(self):
        """Production EXPECTED_CLASS_MAPPING must be {0: 'defect', 1: 'no defect'}."""
        self.assertEqual(EXPECTED_CLASS_MAPPING, {0: "defect", 1: "no defect"})
        self.assertTrue(is_defect_class(EXPECTED_CLASS_MAPPING[0]))
        self.assertFalse(is_defect_class(EXPECTED_CLASS_MAPPING[1]))

    def test_rejection_of_inverted_or_unexpected_checkpoints(self):
        """
        Initialization validation must reject checkpoints where class 0 is not defect
        or class 1 is not non-defect, preventing reversed inspection verdicts.
        """
        def validate_mapping(names):
            if len(names) != len(EXPECTED_CLASS_MAPPING):
                raise ValueError("Class count mismatch")
            for cid, cname in EXPECTED_CLASS_MAPPING.items():
                if cid not in names:
                    raise ValueError(f"Missing class ID {cid}")
                if is_defect_class(names[cid]) != is_defect_class(cname):
                    raise ValueError(f"Class semantic mismatch for ID {cid}")
            return True

        # Valid production mapping (best2.pt)
        self.assertTrue(validate_mapping(self.best2_names))

        # Inverted mapping (best.pt) must be rejected
        with self.assertRaises(ValueError):
            validate_mapping(self.best1_names)

        # Missing classes must be rejected
        with self.assertRaises(ValueError):
            validate_mapping({0: "defect"})

        # Reversed order with same names
        with self.assertRaises(ValueError):
            validate_mapping({0: "no defect", 1: "defect"})

    def test_class_normalization_variations(self):
        """is_defect_class must handle case variations, whitespace, and hyphens."""
        names_custom = {
            0: "Defect-Pill",
            1: "NO_DEFECT",
            2: "Good_Pill",
            3: "Defective_Capsule",
            4: "OK"
        }
        self.assertTrue(is_defect_class(0, names_custom))
        self.assertFalse(is_defect_class(1, names_custom))
        self.assertFalse(is_defect_class(2, names_custom))
        self.assertTrue(is_defect_class(3, names_custom))
        self.assertFalse(is_defect_class(4, names_custom))

    def test_string_keys_handling(self):
        """is_defect_class should tolerate string or int keys in dictionary."""
        names_str = {"0": "defect", "1": "no defect"}
        self.assertTrue(is_defect_class(0, names_str))
        self.assertFalse(is_defect_class(1, names_str))
        self.assertTrue(is_defect_class("0", names_str))
        self.assertFalse(is_defect_class("1", names_str))

    def test_unknown_class_id_defaults_to_safe_detection(self):
        """Unknown class ID with no match in names returns False."""
        self.assertFalse(is_defect_class(99, self.best2_names))

    def test_ncnn_metadata_file_consistency(self):
        """Verify NCNN metadata matches the 416x416 unquantized export specifications."""
        meta_path = os.path.join(os.path.dirname(__file__), "..", "model", "best2_ncnn_model", "metadata.yaml")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                data = yaml.safe_load(f)
            self.assertEqual(data.get("imgsz"), [416, 416])
            self.assertEqual(data.get("names"), EXPECTED_CLASS_MAPPING)
            self.assertIsNone(data.get("quantize"))


if __name__ == "__main__":
    unittest.main()
