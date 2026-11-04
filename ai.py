from ultralytics import YOLO
import cv2
import time
import os

# =========================================================
# PATHS
# =========================================================

MODEL_PATH = "model/best2.pt"

DATA_YAML = (
    "dataset/Defect Detection.v1i.yolov8/data.yaml"
)

# =========================================================
# LOAD MODEL
# =========================================================

print("Loading YOLOv8 model...")

model = YOLO(MODEL_PATH)

print("Model classes:")
print(model.names)
from ultralytics import YOLO
import cv2
import time
import os

# =========================================================
# PATHS
# =========================================================

MODEL_PATH = "model/best2.pt"

DATA_YAML = (
    "dataset/Defect Detection.v1i.yolov8/data.yaml"
)

# =========================================================
# LOAD MODEL
# =========================================================

print("Loading YOLOv8 model...")

model = YOLO(MODEL_PATH)

print("Model classes:")
print(model.names)

# =========================================================
# CHECK DATASET
# =========================================================

if not os.path.exists(DATA_YAML):
    print("ERROR: data.yaml not found")
    print(os.path.abspath(DATA_YAML))
    exit()

# =========================================================
# CALCULATE ACTUAL TEST METRICS
# =========================================================

print("\n============================================")
print("       YOLOv8 MODEL EVALUATION")
print("============================================")
print("Evaluating on TEST dataset...")
print("Please wait...")
print("============================================\n")

try:

    metrics = model.val(
        data=DATA_YAML,
        split="test",
        imgsz=640,
        plots=False,
        verbose=False
    )

    # Actual metrics returned by YOLO
    precision = float(metrics.box.mp)
    recall = float(metrics.box.mr)
    map50 = float(metrics.box.map50)
    map5095 = float(metrics.box.map)

    print("\n============================================")
    print("          ACTUAL TEST METRICS")
    print("============================================")
    print(f"Precision    : {precision * 100:.2f}%")
    print(f"Recall       : {recall * 100:.2f}%")
    print(f"mAP@50       : {map50 * 100:.2f}%")
    print(f"mAP@50-95    : {map5095 * 100:.2f}%")
    print("============================================\n")

except Exception as e:

    print("\nERROR while evaluating model:")
    print(e)
    exit()

# =========================================================
# OPEN CAMERA
# =========================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()

print("Camera started.")
print("Press Q to quit.")

# =========================================================
# FPS
# =========================================================

previous_time = time.time()

# =========================================================
# CAMERA LOOP
# =========================================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break

    # -----------------------------------------------------
    # YOLO INFERENCE
    # -----------------------------------------------------

    start_time = time.time()

    results = model.predict(
        source=frame,
        conf=0.25,
        imgsz=640,
        verbose=False
    ) 

    inference_time = (time.time() - start_time) * 1000

    # -----------------------------------------------------
    # DRAW YOLO BOXES
    # -----------------------------------------------------

    annotated_frame = results[0].plot()

    # -----------------------------------------------------
    # FPS
    # -----------------------------------------------------

    current_time = time.time()

    fps = 15.0 / max(
        current_time - previous_time,
        0.0001
    )

    previous_time = current_time

    # =====================================================
    # METRICS PANEL
    # =====================================================

    panel_height = 180

    cv2.rectangle(
        annotated_frame,
        (0, 0),
        (annotated_frame.shape[1], panel_height),
        (0, 0, 0),
        -1
    )

    # Title
    cv2.putText(
        annotated_frame,
        "BLISTER PACK DEFECT DETECTION",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # Precision
    cv2.putText(
        annotated_frame,
        f"Precision : {precision * 100:.2f}%",
        (10, 53),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # Recall
    cv2.putText(
        annotated_frame,
        f"Recall    : {recall * 100:.2f}%",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # mAP@50
    cv2.putText(
        annotated_frame,
        f"mAP@50    : {map50 * 100:.2f}%",
        (10, 107),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # mAP@50-95
    cv2.putText(
        annotated_frame,
        f"mAP@50-95 : {map5095 * 100:.2f}%",
        (10, 134),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # Live speed
    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.1f}  Inference: {inference_time:.0f} ms",
        (10, 163),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        2
    )

    # =====================================================
    # CURRENT DETECTION
    # =====================================================

    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:

        # Highest confidence detection
        best_index = int(boxes.conf.argmax())

        class_id = int(boxes.cls[best_index])
        confidence = float(boxes.conf[best_index])

        class_name = model.names[class_id]

        detection_text = (
            f"{class_name}: {confidence * 100:.1f}%"
        )

    else:

        detection_text = "No Detection"

    # =====================================================
    # DETECTION PANEL
    # =====================================================

    panel_x = annotated_frame.shape[1] - 280

    cv2.rectangle(
        annotated_frame,
        (panel_x, 0),
        (annotated_frame.shape[1], 52),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        annotated_frame,
        detection_text,
        (panel_x + 10, 34),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 0),
        2
    )

    # =====================================================
    # DISPLAY
    # =====================================================

    cv2.imshow(
        "Blister Pack Defect Detection",
        annotated_frame
    )

    # =====================================================
    # QUIT
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =========================================================
# CLEANUP
# =========================================================

cap.release()
cv2.destroyAllWindows()

print("Camera stopped.")
# =========================================================
# CHECK DATASET
# =========================================================

if not os.path.exists(DATA_YAML):
    print("ERROR: data.yaml not found")
    print(os.path.abspath(DATA_YAML))
    exit()

# =========================================================
# CALCULATE ACTUAL TEST METRICS
# =========================================================

print("\n============================================")
print("       YOLOv8 MODEL EVALUATION")
print("============================================")
print("Evaluating on TEST dataset...")
print("Please wait...")
print("============================================\n")

try:

    metrics = model.val(
        data=DATA_YAML,
        split="test",
        imgsz=640,
        plots=False,
        verbose=False
    )

    # Actual metrics returned by YOLO
    precision = float(metrics.box.mp)
    recall = float(metrics.box.mr)
    map50 = float(metrics.box.map50)
    map5095 = float(metrics.box.map)

    print("\n============================================")
    print("          ACTUAL TEST METRICS")
    print("============================================")
    print(f"Precision    : {precision * 100:.2f}%")
    print(f"Recall       : {recall * 100:.2f}%")
    print(f"mAP@50       : {map50 * 100:.2f}%")
    print(f"mAP@50-95    : {map5095 * 100:.2f}%")
    print("============================================\n")

except Exception as e:

    print("\nERROR while evaluating model:")
    print(e)
    exit()

# =========================================================
# OPEN CAMERA
# =========================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()

print("Camera started.")
print("Press Q to quit.")

# =========================================================
# FPS
# =========================================================

previous_time = time.time()

# =========================================================
# CAMERA LOOP
# =========================================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read camera frame.")
        break

    # -----------------------------------------------------
    # YOLO INFERENCE
    # -----------------------------------------------------

    start_time = time.time()

    results = model.predict(
        source=frame,
        conf=0.25,
        imgsz=640,
        verbose=False
    )

    inference_time = (time.time() - start_time) * 1000

    # -----------------------------------------------------
    # DRAW YOLO BOXES
    # -----------------------------------------------------

    annotated_frame = results[0].plot()

    # -----------------------------------------------------
    # FPS
    # -----------------------------------------------------

    current_time = time.time()

    fps = 1.0 / max(
        current_time - previous_time,
        0.0001
    )

    previous_time = current_time

    # =====================================================
    # METRICS PANEL
    # =====================================================

    panel_height = 180

    cv2.rectangle(
        annotated_frame,
        (0, 0),
        (annotated_frame.shape[1], panel_height),
        (0, 0, 0),
        -1
    )

    # Title
    cv2.putText(
        annotated_frame,
        "BLISTER PACK DEFECT DETECTION",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # Precision
    cv2.putText(
        annotated_frame,
        f"Precision : {precision * 100:.2f}%",
        (10, 53),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # Recall
    cv2.putText(
        annotated_frame,
        f"Recall    : {recall * 100:.2f}%",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # mAP@50
    cv2.putText(
        annotated_frame,
        f"mAP@50    : {map50 * 100:.2f}%",
        (10, 107),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # mAP@50-95
    cv2.putText(
        annotated_frame,
        f"mAP@50-95 : {map5095 * 100:.2f}%",
        (10, 134),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    # Live speed
    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.1f}  Inference: {inference_time:.0f} ms",
        (10, 163),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        2
    )

    # =====================================================
    # CURRENT DETECTION
    # =====================================================

    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:

        # Highest confidence detection
        best_index = int(boxes.conf.argmax())

        class_id = int(boxes.cls[best_index])
        confidence = float(boxes.conf[best_index])

        class_name = model.names[class_id]

        detection_text = (
            f"{class_name}: {confidence * 100:.1f}%"
        )

    else:

        detection_text = "No Detection"

    # =====================================================
    # DETECTION PANEL
    # =====================================================

    panel_x = annotated_frame.shape[1] - 280

    cv2.rectangle(
        annotated_frame,
        (panel_x, 0),
        (annotated_frame.shape[1], 52),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        annotated_frame,
        detection_text,
        (panel_x + 10, 34),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 0),
        2
    )

    # =====================================================
    # DISPLAY
    # =====================================================

    cv2.imshow(
        "Blister Pack Defect Detection",
        annotated_frame
    )

    # =====================================================
    # QUIT
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =========================================================
# CLEANUP
# =========================================================

cap.release()
cv2.destroyAllWindows()

print("Camera stopped.")