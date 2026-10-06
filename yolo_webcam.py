import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open C270 webcam
cap = cv2.VideoCapture("/dev/video0")

if not cap.isOpened():
    print("ERROR: Cannot open webcam")
    exit()

print("Webcam started")
print("YOLO object detection running...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Cannot read webcam frame")
        break

    # YOLO detection
    results = model(frame, verbose=False)

    # Draw bounding boxes
    annotated_frame = results[0].plot()

    # Save/display result
    cv2.imwrite("detection.jpg", annotated_frame)

    # Press Ctrl+C to stop
    print("Detection running...", end="\r")

cap.release()
cv2.destroyAllWindows()
