"""
SQLite storage for the conveyor belt and the inspections.

One file, no server, nothing to install: data/inspection.db

Tables
    conveyor_events   every motor start/stop, every IR object/clear, operator actions
    conveyor_samples  one row per second: motor running?, speed, object at the IR sensor?
    inspections       one row per inspected blister pack (result, defect type, pills)

View the data later with the sqlite3 command line, DB Browser for SQLite,
or the CSV download buttons on the dashboard.
"""

import csv
import io
import os
import sqlite3
import threading
import time

SCHEMA = """
CREATE TABLE IF NOT EXISTS conveyor_events (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ts      TEXT    NOT NULL,
    epoch   REAL    NOT NULL,
    event   TEXT    NOT NULL,
    detail  TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_epoch ON conveyor_events(epoch);

CREATE TABLE IF NOT EXISTS conveyor_samples (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ts             TEXT    NOT NULL,
    epoch          REAL    NOT NULL,
    motor_running  INTEGER NOT NULL,
    speed          REAL    NOT NULL,
    object_present INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_samples_epoch ON conveyor_samples(epoch);

CREATE TABLE IF NOT EXISTS inspections (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    ts               TEXT    NOT NULL,
    epoch            REAL    NOT NULL,
    pack_id          TEXT    NOT NULL,
    result           TEXT    NOT NULL,
    defect_type      TEXT,
    defective_pills  TEXT,
    confidence       REAL
);
CREATE INDEX IF NOT EXISTS idx_insp_epoch ON inspections(epoch);
"""

# Table name -> columns written to the CSV download.
EXPORTS = {
    "conveyor_events": ("ts", "event", "detail"),
    "conveyor_samples": ("ts", "motor_running", "speed", "object_present"),
    "inspections": ("ts", "pack_id", "result", "defect_type", "defective_pills", "confidence"),
}

MAX_QUEUE = 20000     # safety limit if the disk is ever unwritable


def stamp():
    """(local time text, epoch seconds)"""
    t = time.time()
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)), t


class Database:

    def __init__(self, path, keep_sample_days=30):
        self.path = path
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

        self._samples = []
        self._inspections = []

        self.prune(keep_sample_days)

    # -----------------------------------------------------
    # writing
    # -----------------------------------------------------

    def add_event(self, event, detail=""):
        """Written straight away (events are rare)."""
        ts, epoch = stamp()
        try:
            with self._lock:
                self._conn.execute(
                    "INSERT INTO conveyor_events (ts, epoch, event, detail) VALUES (?,?,?,?)",
                    (ts, epoch, event, detail),
                )
                self._conn.commit()
        except sqlite3.Error as e:
            print("Database error (event):", e)

    def queue_sample(self, motor_running, speed, object_present):
        """Kept in memory and written in batches by flush() to spare the SD card."""
        ts, epoch = stamp()
        with self._lock:
            if len(self._samples) < MAX_QUEUE:
                self._samples.append(
                    (ts, epoch, int(bool(motor_running)), float(speed), int(bool(object_present)))
                )

    def queue_inspection(self, entry):
        """entry = one dict from the inspection history."""
        ts, epoch = stamp()
        row = (
            entry.get("time") or ts,
            epoch,
            entry.get("id", ""),
            entry.get("result", ""),
            entry.get("defect", ""),
            entry.get("pills", ""),
            float(entry.get("conf", 0.0)),
        )
        with self._lock:
            if len(self._inspections) < MAX_QUEUE:
                self._inspections.append(row)

    def flush(self):
        with self._lock:
            if not self._samples and not self._inspections:
                return
            samples, inspections = self._samples, self._inspections
            self._samples, self._inspections = [], []
            try:
                if samples:
                    self._conn.executemany(
                        "INSERT INTO conveyor_samples "
                        "(ts, epoch, motor_running, speed, object_present) VALUES (?,?,?,?,?)",
                        samples,
                    )
                if inspections:
                    self._conn.executemany(
                        "INSERT INTO inspections "
                        "(ts, epoch, pack_id, result, defect_type, defective_pills, confidence) "
                        "VALUES (?,?,?,?,?,?,?)",
                        inspections,
                    )
                self._conn.commit()
            except sqlite3.Error as e:
                print("Database error (flush):", e)
                self._samples = (samples + self._samples)[-MAX_QUEUE:]
                self._inspections = (inspections + self._inspections)[-MAX_QUEUE:]

    def prune(self, keep_sample_days):
        """Old one-second samples are deleted. Events and inspections are kept."""
        cutoff = time.time() - keep_sample_days * 86400
        try:
            with self._lock:
                self._conn.execute("DELETE FROM conveyor_samples WHERE epoch < ?", (cutoff,))
                self._conn.commit()
        except sqlite3.Error as e:
            print("Database error (prune):", e)

    # -----------------------------------------------------
    # reading
    # -----------------------------------------------------

    def events(self, limit=50):
        with self._lock:
            rows = self._conn.execute(
                "SELECT id, ts, event, detail FROM conveyor_events ORDER BY id DESC LIMIT ?",
                (int(limit),),
            ).fetchall()
        return [{"id": r[0], "time": r[1], "event": r[2], "detail": r[3] or ""} for r in rows]

    def samples(self, seconds=600, max_points=1500):
        since = time.time() - float(seconds)
        with self._lock:
            rows = self._conn.execute(
                "SELECT epoch, motor_running, object_present FROM conveyor_samples "
                "WHERE epoch >= ? ORDER BY epoch ASC",
                (since,),
            ).fetchall()
        if len(rows) > max_points:
            step = -(-len(rows) // max_points)
            rows = rows[::step]
        return [{"t": r[0], "m": r[1], "o": r[2]} for r in rows]

    def count_events_today(self, event, detail_prefix=None):
        lt = time.localtime()
        midnight = time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday, 0, 0, 0, 0, 0, -1))
        sql = "SELECT COUNT(*) FROM conveyor_events WHERE event=? AND epoch>=?"
        args = [event, midnight]
        if detail_prefix:
            sql += " AND detail LIKE ?"
            args.append(detail_prefix + "%")
        with self._lock:
            return int(self._conn.execute(sql, args).fetchone()[0])

    def counts(self):
        """Rows written so far (all time). Uses the largest id, so it is instant."""
        out = {"path": self.path}
        with self._lock:
            for key, table in (("events", "conveyor_events"),
                               ("samples", "conveyor_samples"),
                               ("inspections", "inspections")):
                out[key] = int(self._conn.execute(
                    f"SELECT COALESCE(MAX(id), 0) FROM {table}").fetchone()[0])
        return out

    def export_csv(self, table):
        """Generator of CSV text, read through its own connection."""
        cols = EXPORTS[table]
        conn = sqlite3.connect(self.path)
        try:
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(cols)
            yield buf.getvalue()

            cur = conn.execute(f"SELECT {', '.join(cols)} FROM {table} ORDER BY id")
            while True:
                rows = cur.fetchmany(2000)
                if not rows:
                    break
                buf = io.StringIO()
                csv.writer(buf).writerows(rows)
                yield buf.getvalue()
        finally:
            conn.close()

    def close(self):
        self.flush()
        with self._lock:
            try:
                self._conn.commit()
                self._conn.close()
            except sqlite3.Error:
                pass