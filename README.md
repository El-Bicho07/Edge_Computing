# Day 1 - Object Detection

Work completed on **October 6, 2026** and pushed to the `Day-1` branch. The work explored webcam capture, YOLO-based detection, grayscale processing, and a classical OpenCV foreground-detection prototype.

## What was done

- Tested webcam access and frame capture. [camera_test.py](./camera_test.py) saves a test frame as [test_frame.jpg](./test_frame.jpg); [camera_detect.py](./camera_detect.py) continuously reads the `/dev/video0` camera and saves frames to [camera.jpg](./camera.jpg).
- Added a webcam object-detection experiment using the Ultralytics YOLO model in [yolo_webcam.py](./yolo_webcam.py). It draws predicted bounding boxes and writes annotated frames to `detection.jpg` while running.
- Added a grayscale webcam stream in [greyscale_webcam.py](./greyscale_webcam.py), saving frames to `grayscale.jpg`.
- Built and refined an OpenCV foreground-detection prototype in [object_detection.py](./object_detection.py). It converts frames to grayscale, applies MOG2 background subtraction, thresholds and cleans the foreground mask, finds contours, and draws boxes around regions larger than the configured minimum area.
- Added live FPS, processing-latency, and object-count indicators to the OpenCV prototype. Its configured thresholds are 15 FPS, 100 ms, and 5 objects; these are comparison targets displayed at runtime, not reported benchmark results.
- Committed image artifacts and examples for basic detection, grayscale, camera capture, thresholding, and object detection. See [Basic_detection.png](./Basic_detection.png), [Greyscale.png](./Greyscale.png), [object threshold.jpeg](./object%20threshold.jpeg), and the other images listed below.

## Run the experiments

Install OpenCV and Ultralytics in the Python environment, connect a webcam, and run the desired script from the repository root:

```bash
python camera_test.py
python camera_detect.py
python yolo_webcam.py
python greyscale_webcam.py
python object_detection.py
```

The camera scripts expect the device at `/dev/video0`. The YOLO experiment loads `yolo11n.pt`; make that model available from the working directory before running it. The OpenCV foreground detector does not use a trained YOLO model.

## Files pushed on `Day-1`

### Python scripts

- [camera_test.py](./camera_test.py) - verifies webcam access and saves one test frame.
- [camera_detect.py](./camera_detect.py) - continuously captures and saves webcam frames.
- [yolo_webcam.py](./yolo_webcam.py) - runs YOLO inference on webcam frames and saves annotated output.
- [greyscale_webcam.py](./greyscale_webcam.py) - converts webcam frames to grayscale and saves them.
- [object_detection.py](./object_detection.py) - performs OpenCV foreground detection with contour boxes and runtime metrics.

### Committed images and examples

- [Basic_detection.png](./Basic_detection.png)
- [Greyscale.png](./Greyscale.png)
- [camera.jpg](./camera.jpg)
- [grayscale.jpg](./grayscale.jpg)
- [grayscale.png](./grayscale.png)
- [grscale.png](./grscale.png)
- [object threshold.jpeg](./object%20threshold.jpeg)
- [object_detection.jpg](./object_detection.jpg)
- [test.jpg](./test.jpg)
- [test_frame.jpg](./test_frame.jpg)

## Day 1 commits

- `448f587` - First Commit
- `564d87e` - Day-1 Tasks commit
- `a1b62d1` - Modified file push
- `89cfb29` - fix: object_detection.py modified
