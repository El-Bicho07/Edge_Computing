import unittest
import os
import tempfile
import time
from database import Database

class TestDatabase(unittest.TestCase):
    """
    Tests for SQLite database operations in database.py:
    - Isolated temporary SQLite database fixture
    - WAL mode configuration
    - Event insertion and retrieval
    - In-memory sample queuing and batch flushing
    - Automatic flush on CSV export
    - Sample pruning based on age cutoff
    - Accurate row counting (SELECT COUNT(*)) after deletion/pruning
    """

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_inspection.db")
        self.db = Database(self.db_path, keep_sample_days=30)

    def tearDown(self):
        self.db.close()
        self.temp_dir.cleanup()

    def test_wal_mode_enabled(self):
        """Database must initialize with PRAGMA journal_mode=WAL."""
        mode = self.db._conn.execute("PRAGMA journal_mode").fetchone()[0]
        self.assertEqual(mode.lower(), "wal")

    def test_add_and_retrieve_events(self):
        """Events are written immediately and retrieved in reverse chronological order."""
        self.db.add_event("motor_start", "duty=80")
        self.db.add_event("object_detected", "IR trigger")
        self.db.add_event("motor_stop", "normal")

        events = self.db.events(limit=10)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0]["event"], "motor_stop")
        self.assertEqual(events[1]["event"], "object_detected")
        self.assertEqual(events[2]["event"], "motor_start")
        self.assertEqual(events[2]["detail"], "duty=80")

    def test_count_events_today(self):
        """count_events_today filters by event type and detail prefix."""
        self.db.add_event("reject", "defective pill in slot 2")
        self.db.add_event("reject", "defective pill in slot 5")
        self.db.add_event("pass", "clean pack")

        rejects = self.db.count_events_today("reject")
        self.assertEqual(rejects, 2)
        passes = self.db.count_events_today("pass")
        self.assertEqual(passes, 1)

        filtered = self.db.count_events_today("reject", detail_prefix="defective pill in slot 2")
        self.assertEqual(filtered, 1)

    def test_queue_sample_and_flush(self):
        """Samples are queued in RAM and persisted only when flush() is invoked."""
        self.db.queue_sample(motor_running=True, speed=50.0, object_present=False)
        self.db.queue_sample(motor_running=True, speed=50.0, object_present=True)

        # Before flush, database samples table should be empty
        self.assertEqual(self.db.counts()["samples"], 0)

        self.db.flush()
        # After flush, 2 rows should be in database
        self.assertEqual(self.db.counts()["samples"], 2)

    def test_export_csv_auto_flushes(self):
        """export_csv() must automatically flush queued samples before querying."""
        self.db.queue_sample(motor_running=True, speed=75.0, object_present=True)
        # Verify not yet flushed
        self.assertEqual(len(self.db._samples), 1)

        # Calling export_csv generator triggers flush
        csv_chunks = list(self.db.export_csv("conveyor_samples"))
        full_csv = "".join(csv_chunks)

        self.assertIn("motor_running,speed,object_present", full_csv)
        self.assertIn("1,75.0,1", full_csv)
        self.assertEqual(len(self.db._samples), 0)

    def test_prune_and_accurate_counts(self):
        """prune() deletes expired samples; counts() uses COUNT(*) and reflects actual rows."""
        # Insert 5 old samples (epoch 100 days ago) directly into table
        old_epoch = time.time() - 100 * 86400
        with self.db._lock:
            for _ in range(5):
                self.db._conn.execute(
                    "INSERT INTO conveyor_samples (ts, epoch, motor_running, speed, object_present) "
                    "VALUES (?, ?, 1, 50.0, 0)",
                    ("old_time", old_epoch)
                )
            self.db._conn.commit()

        # Insert 3 fresh samples
        for _ in range(3):
            self.db.queue_sample(motor_running=True, speed=50.0, object_present=False)
        self.db.flush()

        # Total is currently 8 rows
        self.assertEqual(self.db.counts()["samples"], 8)

        # Prune older than 30 days
        self.db.prune(keep_sample_days=30)

        # Counts must now reflect exactly 3 remaining rows, NOT 8 (MAX(id) bug verification)
        self.assertEqual(self.db.counts()["samples"], 3)


if __name__ == "__main__":
    unittest.main()

