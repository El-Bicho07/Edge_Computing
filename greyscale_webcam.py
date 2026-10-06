import cv2

cap = cv2.VideoCapture("/dev/video0")

if not cap.isOpened():
    print("ERROR: Cannot open webcam")
    exit()

print("C270 grayscale webcam connected!")
print("Reading camera frames...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("\nERROR: Cannot read frame")
        break

    # Convert color frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Save grayscale image
    cv2.imwrite("grayscale.jpg", gray_frame)

    print(f"Grayscale frame received: {gray_frame.shape}", end="\r")

cap.release()