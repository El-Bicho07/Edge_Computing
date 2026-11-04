"""
Blister Pack Defect Detection + 6 Pill LED Indicator
Raspberry Pi 5, YOLOv8, web dashboard

Run:
    python app.py
Then open http://127.0.0.1:5000

Files next to this one:
    dashboard.html
    database.py     (SQLite storage)
    conveyor.py     (servo motor + IR sensor)
    model/best2.pt
    data/inspection.db is created automatically

LED mapping (a pill's LED turns ON when that pill is defective):
    Pill 1 -> GPIO17    Pill 2 -> GPIO27    Pill 3 -> GPIO22
    Pill 4 -> GPIO23    Pill 5 -> GPIO24    Pill 6 -> GPIO25

Pill layout seen by the camera:
    1  2  3
    4  5  6

How speed is gained (three separate threads):
    capture thread : reads the camera at ~30 FPS, draws the last known boxes,
                     encodes JPEG, streams it. The video never waits for YOLO.
    detect thread  : always takes the NEWEST frame and runs YOLO on it, so old
                     frames never queue up (this is what lowers latency).
    web server     : serves the dashboard.
On top of that, the model is exported once to NCNN, which runs much faster than
the .pt file on the Raspberry Pi CPU.
"""

import os
import sys
import time
import atexit
import signal
import logging
import threading
import webbrowser
from collections import Counter, deque
from datetime import datetime

import cv2
import numpy as np
from flask import Flask, Response, jsonify, send_file, request
from ultralytics import YOLO

from database import Database, EXPORTS
from conveyor import Conveyor

# =========================================================
# CONFIG
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best2.pt")
DASHBOARD_FILE = os.path.join(BASE_DIR, "dashboard.html")
DB_PATH = os.path.join(BASE_DIR, "data", "inspection.db")

# ---- camera ----------------------------------------------
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30            # video frame rate asked from the camera
JPEG_QUALITY = 75

# ---- model speed and accuracy ----------------------------
# NCNN is about 2 to 3 times faster than the .pt file on a Raspberry Pi.
# The first start exports the model once (takes a few minutes, needs internet).
USE_NCNN = True

# Must be a multiple of 32.  320 = fastest.  416 = balanced.  640 = most accurate.
IMG_SIZE = 416

CONF_THRESHOLD = 0.35      # minimum confidence to keep a detection
IOU_THRESHOLD = 0.5        # overlap limit when removing duplicate boxes

# ---- stability (this is what raises the usable accuracy) --
# Each pill is judged on its last N frames, not on one frame, so a single
# bad frame cannot flip an LED. A tie counts as DEFECT (safer for pharma).
SMOOTH_FRAMES = 5
SLOT_MIN_PRESENT = 2       # frames a pill must be seen in before it is reported

# ---- pack logging ----------------------------------------
MIN_FRAMES_TO_LOG = 6
MIN_PACK_SECONDS = 0.5
ABSENT_SECONDS = 0.8       # no pills for this long = the pack has left
DEFECT_SHARE = 0.4         # share of frames with a defect that makes a pack DEFECT
ACCURACY_WINDOW = 50       # packs used for the accuracy tile
DET_STALE_SECONDS = 0.5    # boxes older than this are not drawn

PILL_COUNT = 6
PILL_COLS = 3

# Test-set results you measured earlier with model.val (shown on the dashboard).
TEST_METRICS = {
    "status": "ready",
    "precision": 0.9081,
    "recall": 0.8350,
    "map50": 0.8769,
    "map5095": 0.5562,
}

HOST = "127.0.0.1"
PORT = 5000
OPEN_BROWSER = True

# Classes that mean "this pill is fine". Anything else counts as a defect.
GOOD_CLASS_NAMES = {
    "good", "ok", "normal", "pass", "perfect", "intact", "complete",
    "no_defect", "nodefect", "non_defect", "non_defective", "not_defective",
    "not_defected", "non_defected", "no_defected", "undefected", "defect_free",
}


def norm(name):
    return str(name).strip().lower().replace("-", "_").replace(" ", "_")


def is_defect_class(name):
    return norm(name) not in GOOD_CLASS_NAMES


# =========================================================
# GPIO
# =========================================================

LED_PINS = [17, 27, 22, 23, 24, 25]

try:
    from gpiozero import LED

    leds = [LED(pin) for pin in LED_PINS]
    GPIO_AVAILABLE = True
    print("GPIO LEDs initialised:")
    for i, pin in enumerate(LED_PINS):
        print(f"  Pill {i + 1} -> GPIO{pin}")
except Exception as e:
    print("WARNING: GPIO unavailable:", e)
    leds = []
    GPIO_AVAILABLE = False

_last_led = [None] * PILL_COUNT


def set_leds(states):
    """states = list of 6 booleans. Only touches a pin when its state changes."""
    if not GPIO_AVAILABLE:
        return
    for i, st in enumerate(states[:len(leds)]):
        st = bool(st)
        if _last_led[i] != st:
            if st:
                leds[i].on()
            else:
                leds[i].off()
            _last_led[i] = st


def all_leds_off():
    set_leds([False] * PILL_COUNT)


# =========================================================
# DATABASE AND CONVEYOR
# =========================================================

db = Database(DB_PATH)
conveyor = Conveyor(db)

# =========================================================
# MODEL
# =========================================================

model = None            # the model used for inference (NCNN or PyTorch)
NAMES = {}              # class id -> class name
BACKEND = "PyTorch"


def ncnn_dir():
    stem = os.path.splitext(os.path.basename(MODEL_PATH))[0]
    return os.path.join(os.path.dirname(MODEL_PATH), stem + "_ncnn_model")


def ncnn_matches_size(folder):
    """True when an existing NCNN export was made for the current IMG_SIZE."""
    meta = os.path.join(folder, "metadata.yaml")
    if not os.path.exists(meta):
        return False
    try:
        import yaml
        with open(meta, "r") as f:
            data = yaml.safe_load(f) or {}
        size = data.get("imgsz")
        if isinstance(size, (list, tuple)):
            size = size[0]
        return int(size) == int(IMG_SIZE)
    except Exception:
        return False


def init_model():
    global model, NAMES, BACKEND

    if not os.path.exists(MODEL_PATH):
        print("ERROR: model not found:")
        print(MODEL_PATH)
        sys.exit(1)

    print("\nLoading YOLOv8 model...")
    pt = YOLO(MODEL_PATH)
    NAMES = dict(pt.names)

    try:
        trained = pt.ckpt.get("train_args", {}).get("imgsz")
        if trained:
            print(f"Model was trained at image size {trained}. Running at {IMG_SIZE}.")
            print("  (a smaller run size is faster but a little less accurate)")
    except Exception:
        pass

    model = pt
    BACKEND = "PyTorch"

    if USE_NCNN:
        try:
            folder = ncnn_dir()
            if not ncnn_matches_size(folder):
                print(f"\nExporting model to NCNN at {IMG_SIZE}px. This happens once...")
                pt.export(format="ncnn", imgsz=IMG_SIZE, half=False)
            model = YOLO(folder, task="detect")
            BACKEND = "NCNN"
        except Exception as e:
            print("WARNING: NCNN is not available, using PyTorch instead:", e)
            model = pt
            BACKEND = "PyTorch"
            try:
                import torch
                torch.set_num_threads(os.cpu_count() or 4)
            except Exception:
                pass

    print("\nModel classes:")
    for class_id, class_name in NAMES.items():
        kind = "DEFECT" if is_defect_class(class_name) else "PASS"
        print(f"  {class_id}: {str(class_name):<20} -> {kind}")

    # Warm-up run so the first real frame is not slow.
    try:
        model.predict(
            source=np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8),
            imgsz=IMG_SIZE, conf=CONF_THRESHOLD, verbose=False, device="cpu",
        )
    except Exception as e:
        print("WARNING: warm-up failed:", e)

    print(f"\nBackend: {BACKEND}   image size: {IMG_SIZE}")


# =========================================================
# SHARED STATE
# =========================================================

class State:

    def __init__(self):
        self.lock = threading.Lock()
        self.cap_lock = threading.Lock()
        self.frame_cond = threading.Condition()

        self.cap = None
        self.running = False
        self.camera_error = None
        self.camera_fps = 0.0

        self.frame = None          # latest JPEG bytes
        self.frame_seq = 0
        self.raw = None            # (seq, capture time, frame)
        self.raw_seq = 0

        self.dets = []             # smoothed pills with boxes, for drawing
        self.dets_time = 0.0

        self.reset_session()

    def reset_session(self):
        self.history = []
        self.n_pass = 0
        self.n_defect = 0
        self.seq = 0
        self.session = None
        self.session_start = None
        self.run_acc = 0.0
        self.run_start = 0.0

        self.fps = 0.0             # video frames per second
        self.det_fps = 0.0         # detections per second
        self.latency = 0.0         # capture -> detections, ms
        self.infer_ms = 0.0        # model time only, ms
        self.fps_sum = 0.0
        self.fps_n = 0
        self.lat_sum = 0.0
        self.lat_n = 0
        self.prev_frame_time = 0.0
        self.prev_det_time = 0.0

        self.pills = []
        self.objects = 0
        self.current = {"label": "NONE", "detections": [], "leds": [False] * PILL_COUNT}
        self.slot_hist = [deque(maxlen=SMOOTH_FRAMES) for _ in range(PILL_COUNT)]


S = State()


def runtime_seconds():
    return S.run_acc + ((time.time() - S.run_start) if S.running else 0.0)


# =========================================================
# PILL POSITIONS AND SMOOTHING
# =========================================================

def assign_slots(dets, width, height):
    """
    Put each detection into one of six slots (0..5):

        0 1 2
        3 4 5

    Rows are found from a gap in the vertical positions, columns from the spread
    of the pills, so a missing pill does not shift the others.
    Returns {slot_index: detection}.
    """
    if not dets:
        return {}

    mean_w = sum(d["w"] for d in dets) / len(dets)
    mean_h = sum(d["h"] for d in dets) / len(dets)

    by_y = sorted(dets, key=lambda d: d["cy"])
    split = None
    if len(by_y) > 1:
        gap, idx = max(
            (by_y[i + 1]["cy"] - by_y[i]["cy"], i + 1) for i in range(len(by_y) - 1)
        )
        if gap > 0.6 * mean_h:
            split = idx

    if split:
        row_of = {id(d): 0 for d in by_y[:split]}
        row_of.update({id(d): 1 for d in by_y[split:]})
    else:
        avg_cy = sum(d["cy"] for d in dets) / len(dets)
        row = 0 if avg_cy < height / 2 else 1
        row_of = {id(d): row for d in dets}

    xs = [d["cx"] for d in dets]
    min_x, max_x = min(xs), max(xs)
    span = max_x - min_x
    pitch = span / (PILL_COLS - 1) if span > 1.2 * mean_w else None

    slots = {}
    for d in dets:
        if pitch:
            col = int(round((d["cx"] - min_x) / pitch))
        else:
            col = int(d["cx"] / (width / PILL_COLS))
        col = max(0, min(PILL_COLS - 1, col))
        slot = row_of[id(d)] * PILL_COLS + col
        if slot not in slots or d["conf"] > slots[slot]["conf"]:
            slots[slot] = d
    return slots


def smooth_pills(slots):
    """
    Vote over the last SMOOTH_FRAMES frames for each of the six slots.
    Called with S.lock held. Returns a list of reported pills.
    """
    pills = []
    for i in range(PILL_COUNT):
        d = slots.get(i)
        if d:
            entry = (d["defect"], d["conf"], d["cls"], (d["x1"], d["y1"], d["x2"], d["y2"]))
        else:
            entry = None
        S.slot_hist[i].append(entry)

        present = [e for e in S.slot_hist[i] if e is not None]
        if len(present) < SLOT_MIN_PRESENT:
            continue

        votes = sum(1 for e in present if e[0])
        is_def = votes * 2 >= len(present)          # a tie counts as defect
        agree = [e for e in present if e[0] == is_def]
        conf = sum(e[1] for e in agree) / len(agree)
        cls = Counter(e[2] for e in agree).most_common(1)[0][0]

        pills.append({
            "pill": i + 1,
            "cls": cls,
            "conf": conf,
            "defect": is_def,
            "box": present[-1][3],
        })
    return pills


# =========================================================
# PACK HISTORY (one entry per pack)
# =========================================================

def track_pack(now, pills):
    """Called with S.lock held."""
    if pills:
        sess = S.session
        if sess is None:
            sess = {
                "start": now, "last": now, "frames": 0, "def_frames": 0,
                "def_conf": [], "ok_conf": [],
                "types": Counter(), "bad_pills": Counter(), "logged": False,
            }
            S.session = sess

        sess["frames"] += 1
        sess["last"] = now

        bad = [p for p in pills if p["defect"]]
        if bad:
            sess["def_frames"] += 1
            sess["def_conf"].append(sum(p["conf"] for p in bad) / len(bad))
            for p in bad:
                sess["types"][p["cls"]] += 1
                sess["bad_pills"][p["pill"]] += 1
        else:
            sess["ok_conf"].append(sum(p["conf"] for p in pills) / len(pills))

        if (not sess["logged"]
                and sess["frames"] >= MIN_FRAMES_TO_LOG
                and now - sess["start"] >= MIN_PACK_SECONDS):
            sess["logged"] = True
            is_def = sess["def_frames"] >= max(1, DEFECT_SHARE * sess["frames"])

            # Confidence only from the frames that agree with the final result.
            confs = sess["def_conf"] if is_def else sess["ok_conf"]
            conf = sum(confs) / len(confs) if confs else 0.0

            bad_list = []
            if is_def:
                need = max(1, sess["def_frames"] / 2)
                bad_list = sorted(p for p, c in sess["bad_pills"].items() if c >= need)

            S.seq += 1
            entry = {
                "n": S.seq,
                "id": f"BP-{S.seq:06d}",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "result": "DEFECT" if is_def else "PASS",
                "defect": (sess["types"].most_common(1)[0][0]
                           if (is_def and sess["types"]) else "None"),
                "pills": ", ".join(str(p) for p in bad_list) if bad_list else "-",
                "conf": conf,
            }
            S.history.append(entry)
            db.queue_inspection(entry)
            if is_def:
                S.n_defect += 1
            else:
                S.n_pass += 1
            if len(S.history) > 5000:
                S.history = S.history[-5000:]

    elif S.session is not None and now - S.session["last"] > ABSENT_SECONDS:
        S.session = None


# =========================================================
# DRAWING
# =========================================================

FONT = cv2.FONT_HERSHEY_SIMPLEX
PASS_BGR = (96, 150, 52)
FAIL_BGR = (58, 58, 190)


def draw_pills(view, pills):
    for p in pills:
        x1, y1, x2, y2 = [int(v) for v in p["box"]]
        color = FAIL_BGR if p["defect"] else PASS_BGR
        cv2.rectangle(view, (x1, y1), (x2, y2), color, 2)
        label = f'{p["pill"]} {"DEFECT" if p["defect"] else "OK"} {p["conf"] * 100:.0f}%'
        (tw, th), _ = cv2.getTextSize(label, FONT, 0.5, 1)
        ty = max(th + 6, y1)
        cv2.rectangle(view, (x1, ty - th - 6), (x1 + tw + 6, ty), color, -1)
        cv2.putText(view, label, (x1 + 3, ty - 4), FONT, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


# =========================================================
# CAMERA
# =========================================================

def open_camera():
    cap = None
    for api in (cv2.CAP_V4L2, cv2.CAP_ANY):
        c = cv2.VideoCapture(CAMERA_INDEX, api)
        if c.isOpened():
            cap = c
            break
        c.release()
    if cap is None:
        return None

    # MJPG is what lets a USB camera deliver 30 FPS at 640x480.
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)   # no queue of old frames
    return cap


def start_camera():
    with S.cap_lock:
        if S.running:
            return True, None

        cap = open_camera()
        if cap is None:
            return False, "Could not open the camera. Close other apps that use it and try again."

        S.cap = cap
        with S.lock:
            S.running = True
            S.run_start = time.time()
            S.prev_frame_time = 0.0
            S.prev_det_time = 0.0
            S.fps = 0.0
            S.det_fps = 0.0
            S.latency = 0.0
            S.infer_ms = 0.0
            S.camera_fps = float(cap.get(cv2.CAP_PROP_FPS) or 0)
            S.camera_error = None
            S.raw = None
            S.dets = []
            S.slot_hist = [deque(maxlen=SMOOTH_FRAMES) for _ in range(PILL_COUNT)]
            if S.session_start is None:
                S.session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return True, None


def stop_camera():
    with S.cap_lock:
        with S.lock:
            if S.running:
                S.run_acc += time.time() - S.run_start
            S.running = False
            S.session = None
            S.raw = None
            S.dets = []
            S.pills = []
            S.objects = 0
            S.current = {"label": "NONE", "detections": [], "leds": [False] * PILL_COUNT}
            S.slot_hist = [deque(maxlen=SMOOTH_FRAMES) for _ in range(PILL_COUNT)]
        if S.cap is not None:
            S.cap.release()
            S.cap = None
    with S.frame_cond:
        S.frame = None
        S.frame_cond.notify_all()
    all_leds_off()


# =========================================================
# CAPTURE THREAD  (about 30 FPS, never waits for YOLO)
# =========================================================

def capture_worker():
    while True:
        did_work = False

        with S.cap_lock:
            cap = S.cap
            if S.running and cap is not None:
                ok, frame = cap.read()

                if not ok:
                    cap.release()
                    S.cap = None
                    with S.lock:
                        S.running = False
                        S.run_acc += time.time() - S.run_start
                        S.camera_error = "The camera stopped sending frames."
                        S.pills = []
                        S.dets = []
                        S.raw = None
                    all_leds_off()
                else:
                    now = time.time()
                    with S.lock:
                        S.raw_seq += 1
                        S.raw = (S.raw_seq, now, frame)

                        if S.prev_frame_time:
                            inst = 1.0 / max(now - S.prev_frame_time, 0.0001)
                            S.fps = inst if S.fps == 0 else S.fps * 0.9 + inst * 0.1
                            S.fps_sum += S.fps
                            S.fps_n += 1
                        S.prev_frame_time = now

                        pills = list(S.dets) if (now - S.dets_time) < DET_STALE_SECONDS else []

                    # Draw on a copy, so the model always sees the clean frame.
                    view = frame.copy()
                    draw_pills(view, pills)
                    ok_enc, buf = cv2.imencode(
                        ".jpg", view, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
                    )
                    if ok_enc:
                        with S.frame_cond:
                            S.frame = buf.tobytes()
                            S.frame_seq += 1
                            S.frame_cond.notify_all()
                    did_work = True

        if not did_work:
            time.sleep(0.02)


# =========================================================
# DETECTION THREAD  (always works on the newest frame)
# =========================================================

def extract_detections(result):
    dets = []
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return dets

    for (x1, y1, x2, y2), c, p in zip(
        boxes.xyxy.tolist(), boxes.cls.tolist(), boxes.conf.tolist()
    ):
        name = NAMES.get(int(c), str(int(c)))
        dets.append({
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "cx": (x1 + x2) / 2, "cy": (y1 + y2) / 2,
            "w": x2 - x1, "h": y2 - y1,
            "cls": name, "conf": float(p), "defect": is_defect_class(name),
        })
    return dets


def detect_worker():
    last_seq = 0

    while True:
        with S.lock:
            running = S.running
            raw = S.raw

        if not running or raw is None or raw[0] == last_seq:
            time.sleep(0.003)
            continue

        seq, t_capture, frame = raw
        last_seq = seq
        height, width = frame.shape[:2]

        t0 = time.perf_counter()
        try:
            result = model.predict(
                source=frame,
                imgsz=IMG_SIZE,
                conf=CONF_THRESHOLD,
                iou=IOU_THRESHOLD,
                agnostic_nms=True,      # one box per pill, never both classes
                max_det=PILL_COUNT,
                verbose=False,
                device="cpu",
            )[0]
        except Exception as e:
            print("Detection error:", e)
            time.sleep(0.2)
            continue
        infer_ms = (time.perf_counter() - t0) * 1000.0

        dets = extract_detections(result)
        slots = assign_slots(dets, width, height)
        now = time.time()
        latency_ms = (now - t_capture) * 1000.0

        with S.lock:
            if not S.running:
                continue

            pills = smooth_pills(slots)

            states = [False] * PILL_COUNT
            for p in pills:
                states[p["pill"] - 1] = p["defect"]

            if pills:
                overall = "DEFECT" if any(p["defect"] for p in pills) else "PASS"
            else:
                overall = "NONE"

            if S.prev_det_time:
                inst = 1.0 / max(now - S.prev_det_time, 0.0001)
                S.det_fps = inst if S.det_fps == 0 else S.det_fps * 0.8 + inst * 0.2
            S.prev_det_time = now

            S.infer_ms = infer_ms if S.infer_ms == 0 else S.infer_ms * 0.8 + infer_ms * 0.2
            S.latency = latency_ms if S.latency == 0 else S.latency * 0.8 + latency_ms * 0.2
            S.lat_sum += latency_ms
            S.lat_n += 1

            S.dets = pills
            S.dets_time = now
            S.objects = len(pills)
            S.pills = [
                {"pill": p["pill"], "cls": p["cls"], "conf": p["conf"], "defect": p["defect"]}
                for p in pills
            ]
            S.current = {"label": overall, "detections": S.pills, "leds": states}

            track_pack(now, pills)

        set_leds(states)


# =========================================================
# WEB SERVER
# =========================================================

app = Flask(__name__)
logging.getLogger("werkzeug").setLevel(logging.ERROR)   # no log line per request


@app.route("/")
def index():
    if not os.path.exists(DASHBOARD_FILE):
        return "dashboard.html not found", 500
    resp = send_file(DASHBOARD_FILE)
    resp.headers["Cache-Control"] = "no-store"
    return resp


def mjpeg():
    last_seq = -1
    while True:
        with S.frame_cond:
            S.frame_cond.wait(timeout=1.0)
            frame = S.frame
            seq = S.frame_seq

        with S.lock:
            running = S.running
        if not running:
            break

        if frame is None or seq == last_seq:
            continue
        last_seq = seq

        yield (b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: "
               + str(len(frame)).encode() + b"\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(
        mjpeg(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
        headers={"Cache-Control": "no-store"},
    )


@app.route("/api/status")
def api_status():
    with S.lock:
        recent = S.history[-ACCURACY_WINDOW:]
        accuracy = (sum(e["conf"] for e in recent) / len(recent)) if recent else None
        classes = [{"name": str(n), "defect": is_defect_class(n)} for n in NAMES.values()]

        return jsonify({
            "running": S.running,
            "fps": round(S.fps, 1),
            "det_fps": round(S.det_fps, 1),
            "camera_fps": round(S.camera_fps, 1),
            "latency_ms": round(S.latency, 1),
            "infer_ms": round(S.infer_ms, 1),
            "objects": S.objects,
            "runtime_s": round(runtime_seconds(), 1),
            "accuracy": accuracy,
            "avg_fps": (S.fps_sum / S.fps_n) if S.fps_n else 0,
            "avg_latency_ms": (S.lat_sum / S.lat_n) if S.lat_n else 0,
            "session_start": S.session_start,
            "camera_error": S.camera_error,
            "camera_index": CAMERA_INDEX,
            "current": S.current,
            "pills": S.pills,
            "gpio": {
                "available": GPIO_AVAILABLE,
                "pins": LED_PINS,
                "states": S.current.get("leds", [False] * PILL_COUNT),
            },
            "totals": {
                "inspected": S.n_pass + S.n_defect,
                "pass": S.n_pass,
                "defect": S.n_defect,
            },
            "history_count": len(S.history),
            "model": {
                "name": os.path.basename(MODEL_PATH),
                "backend": BACKEND,
                "classes": classes,
                "conf_threshold": CONF_THRESHOLD,
                "img_size": IMG_SIZE,
            },
            "metrics": TEST_METRICS,
            "conveyor": conveyor.status(),
            "database": db.counts(),
        })


@app.route("/api/history")
def api_history():
    with S.lock:
        return jsonify(S.history)


@app.route("/api/start", methods=["POST"])
def api_start():
    ok, err = start_camera()
    return jsonify({"ok": ok, "error": err})


@app.route("/api/stop", methods=["POST"])
def api_stop():
    stop_camera()
    return jsonify({"ok": True})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    with S.lock:
        if S.running:
            return jsonify({"ok": False, "error": "Stop the camera before resetting."})
        S.reset_session()
    all_leds_off()
    return jsonify({"ok": True})


# =========================================================
# CONVEYOR AND DATABASE ROUTES
# =========================================================

def _int_arg(name, default, low, high):
    try:
        value = int(request.args.get(name, default))
    except (TypeError, ValueError):
        value = default
    return max(low, min(high, value))


@app.route("/api/conveyor/events")
def api_conveyor_events():
    return jsonify(db.events(_int_arg("limit", 50, 1, 500)))


@app.route("/api/conveyor/samples")
def api_conveyor_samples():
    db.flush()
    return jsonify(db.samples(_int_arg("seconds", 600, 10, 86400)))


@app.route("/api/conveyor/auto", methods=["POST"])
def api_conveyor_auto():
    conveyor.set_mode("auto")
    return jsonify({"ok": True})


@app.route("/api/conveyor/stop", methods=["POST"])
def api_conveyor_stop():
    conveyor.set_mode("stop")
    return jsonify({"ok": True})


@app.route("/export/<name>.csv")
def export_csv(name):
    if name not in EXPORTS:
        return "Unknown export", 404
    db.flush()
    filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        db.export_csv(name),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# =========================================================
# MAIN
# =========================================================

def cleanup():
    try:
        stop_camera()
    except Exception:
        pass
    try:
        conveyor.shutdown()
    except Exception:
        pass
    all_leds_off()
    try:
        db.close()
    except Exception:
        pass

if __name__ == "__main__":
    init_model()

    threading.Thread(target=capture_worker, daemon=True).start()
    threading.Thread(target=detect_worker, daemon=True).start()
    conveyor.start()

    atexit.register(cleanup)
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))

    url = f"http://{HOST}:{PORT}"

    print("\n======================================")
    print(" BLISTER PACK INSPECTION SYSTEM")
    print("======================================")
    print(f"Dashboard      : {url}")
    print(f"Backend        : {BACKEND}")
    print(f"YOLO image size: {IMG_SIZE}")
    print(f"Confidence     : {CONF_THRESHOLD}")
    print(f"Camera         : {CAMERA_WIDTH}x{CAMERA_HEIGHT} at {CAMERA_FPS} FPS")
    print(f"GPIO available : {GPIO_AVAILABLE}")
    print(f"Conveyor       : servo GPIO{conveyor.status()['pins']['servo']}, IR GPIO{conveyor.status()['pins']['ir']}, hardware={conveyor.hardware}")
    print(f"Database       : {DB_PATH}")
    print("======================================\n")

    if OPEN_BROWSER:
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()

    try:
        app.run(host=HOST, port=PORT, threaded=True, debug=False)
    finally:
        cleanup()