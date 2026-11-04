# Day 2 - Blister Pack Defect Detection

Work completed on **October 7, 2026**. Day 2 advanced the project from general object-detection experiments to running a YOLO model for blister-pack defect detection using a live webcam.

## What was done

- Added [ai.py](./ai.py), a live camera inference program using Ultralytics YOLO and OpenCV.
- Loaded the project weights from [model/best.pt](./model/best.pt) and applied predictions to webcam frames with a confidence threshold of `0.25`.
- Displayed annotated frames in a window titled **Blister Pack Defect Detection**. Press **Q** to exit.
- Recorded image preparation settings: auto-orientation applied, images stretched to `512 x 512`, and augmentations enabled.
- Generated sample prediction outputs:
  - [Prediction of test.jpg](./runs/detect/predict/test.jpg)
  - [Prediction of test.jpg (second run)](./runs/detect/predict-2/test.jpg)
  - [Prediction of Basic_detection.png](./runs/detect/predict-3/Basic_detection.jpg)
- Kept a snapshot of the working Python environment in [working-packages.txt](./working-packages.txt).

## Run live detection

From the repository root, with a webcam connected and the model weights in place:

```bash
python ai.py
```

The script opens camera index `0` and loads `model/best.pt`. Install OpenCV and Ultralytics in the Python environment if they are not already available. Press **Q** in the preview window to stop detection.

## Day 2 files

- [ai.py](./ai.py) - live webcam inference and display of annotated YOLO results.
- [model/best.pt](./model/best.pt) - weights loaded by the Day 2 inference script.
- [runs/detect/predict/test.jpg](./runs/detect/predict/test.jpg) - first saved prediction output.
- [runs/detect/predict-2/test.jpg](./runs/detect/predict-2/test.jpg) - second saved prediction output.
- [runs/detect/predict-3/Basic_detection.jpg](./runs/detect/predict-3/Basic_detection.jpg) - saved prediction output for `Basic_detection.png`.
- [working-packages.txt](./working-packages.txt) - Python package/version snapshot.
