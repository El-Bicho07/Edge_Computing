import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot open webcam")
    exit()

print("Webcam connected successfully!")

while True:
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Cannot read frame")
        break

    print("Frame received:", frame.shape)

    # Test only a few frames
    cv2.imwrite("test_frame.jpg", frame)
    break

cap.release()

print("Saved test_frame.jpg")
