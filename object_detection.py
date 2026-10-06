import cv2
import time

# ==========================================
# Configuration
# ==========================================

CAMERA_PATH = "/dev/video0"

MIN_OBJECT_AREA = 1500

FPS_THRESHOLD = 15.0
LATENCY_THRESHOLD_MS = 100.0
OBJECT_COUNT_THRESHOLD = 5


# ==========================================
# Open webcam using V4L2
# ==========================================

cap = cv2.VideoCapture(
    CAMERA_PATH,
    cv2.CAP_V4L2
)

if not cap.isOpened():
    print("ERROR: Cannot open webcam")
    exit()

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("C270 webcam connected!")
print("OpenCV object detection running...")
print("Saving result to object_detection.jpg")


# ==========================================
# Background subtraction
# ==========================================

background_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=50,
    detectShadows=True
)


# ==========================================
# FPS variables
# ==========================================

previous_time = time.perf_counter()


# ==========================================
# Main loop
# ==========================================

while True:

    start_time = time.perf_counter()

    # --------------------------------------
    # Capture frame
    # --------------------------------------

    ret, frame = cap.read()

    if not ret:
        print("\nERROR: Cannot read webcam frame")
        break

    # --------------------------------------
    # Convert to grayscale
    # --------------------------------------

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    # --------------------------------------
    # Background subtraction
    # --------------------------------------

    foreground_mask = background_subtractor.apply(gray)

    # --------------------------------------
    # Remove shadows and noise
    # --------------------------------------

    _, threshold_mask = cv2.threshold(
        foreground_mask,
        200,
        255,
        cv2.THRESH_BINARY
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (5, 5)
    )

    threshold_mask = cv2.morphologyEx(
        threshold_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    threshold_mask = cv2.morphologyEx(
        threshold_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # --------------------------------------
    # Find contours
    # --------------------------------------

    contours, _ = cv2.findContours(
        threshold_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    object_count = 0

    # --------------------------------------
    # Detect foreground objects
    # --------------------------------------

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < MIN_OBJECT_AREA:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        object_count += 1

        # Draw bounding box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Object label
        cv2.putText(
            frame,
            f"Object {object_count}",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # --------------------------------------
    # Calculate latency
    # --------------------------------------

    end_time = time.perf_counter()

    latency_ms = (
        end_time - start_time
    ) * 1000

    # --------------------------------------
    # Calculate FPS
    # --------------------------------------

    current_time = time.perf_counter()

    elapsed_time = (
        current_time - previous_time
    )

    if elapsed_time > 0:
        fps = 1.0 / elapsed_time
    else:
        fps = 0.0

    previous_time = current_time

    # --------------------------------------
    # Threshold checks
    # --------------------------------------

    fps_pass = fps >= FPS_THRESHOLD

    latency_pass = (
        latency_ms <= LATENCY_THRESHOLD_MS
    )

    count_pass = (
        object_count <= OBJECT_COUNT_THRESHOLD
    )

    # --------------------------------------
    # FPS
    # --------------------------------------

    fps_color = (
        (0, 255, 0)
        if fps_pass
        else (0, 0, 255)
    )

    cv2.putText(
        frame,
        f"FPS: {fps:.1f} "
        f"[{'PASS' if fps_pass else 'LOW'}]",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        fps_color,
        2
    )

    # --------------------------------------
    # Latency
    # --------------------------------------

    latency_color = (
        (0, 255, 0)
        if latency_pass
        else (0, 0, 255)
    )

    cv2.putText(
        frame,
        f"Latency: {latency_ms:.1f} ms "
        f"[{'PASS' if latency_pass else 'HIGH'}]",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        latency_color,
        2
    )

    # --------------------------------------
    # Object count
    # --------------------------------------

    count_color = (
        (0, 255, 0)
        if count_pass
        else (0, 0, 255)
    )

    cv2.putText(
        frame,
        f"Objects: {object_count} "
        f"[{'PASS' if count_pass else 'HIGH'}]",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        count_color,
        2
    )

    # --------------------------------------
    # Threshold information
    # --------------------------------------

    cv2.putText(
        frame,
        f"FPS Threshold: {FPS_THRESHOLD:.1f}",
        (20, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Latency Threshold: "
        f"{LATENCY_THRESHOLD_MS:.0f} ms",
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Count Threshold: "
        f"{OBJECT_COUNT_THRESHOLD}",
        (20, 175),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    # --------------------------------------
    # Save processed frame
    # --------------------------------------

    cv2.imwrite(
        "object_detection.jpg",
        frame
    )

    # Save grayscale frame
    cv2.imwrite(
        "grayscale.jpg",
        gray
    )

    # --------------------------------------
    # Terminal status
    # --------------------------------------

    print(
        f"FPS: {fps:.1f} | "
        f"Latency: {latency_ms:.1f} ms | "
        f"Objects: {object_count}",
        end="\r"
    )


# ==========================================
# Cleanup
# ==========================================

cap.release()

print("\nObject detection stopped.")