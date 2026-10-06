import cv2

cap = cv2.VideoCapture("/dev/video0")

if not cap.isOpened():
    print("ERROR: Cannot open webcam")
    exit()

print("C270 webcam connected!")
print("Reading camera frames...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Cannot read frame")
        break

    cv2.imwrite("camera.jpg", frame)

    print(f"Frame received: {frame.shape}", end="\r")

cap.release()
