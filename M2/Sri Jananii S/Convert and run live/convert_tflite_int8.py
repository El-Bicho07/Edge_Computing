#!/usr/bin/env python3
"""
Milestone 2: TFLite INT8 Post-Training Quantization (PTQ) Script
Veyra Pharma Vision Edge System

Converts trained YOLOv8 PyTorch weights to TensorFlow Lite INT8 format
using representative dataset calibration from the Roboflow blister pack dataset.
"""

import os
import sys
import glob
import numpy as np

def representative_dataset_generator(dataset_dir, num_samples=100, imgsz=(416, 416)):
    """Yields normalized sample images for INT8 calibration."""
    img_paths = glob.glob(os.path.join(dataset_dir, "train", "images", "*.jpg"))
    if not img_paths:
        img_paths = glob.glob(os.path.join(dataset_dir, "test", "images", "*.jpg"))
    
    selected_paths = img_paths[:num_samples]
    print(f"[*] Calibration Generator: Calibrating against {len(selected_paths)} representative images...")

    try:
        import cv2
        for path in selected_paths:
            img = cv2.imread(path)
            if img is None:
                continue
            img = cv2.resize(img, imgsz)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = img.astype(np.float32) / 255.0
            img = np.expand_dims(img, axis=0) # [1, 416, 416, 3]
            yield [img]
    except ImportError:
        for _ in range(num_samples):
            yield [np.random.randn(1, imgsz[0], imgsz[1], 3).astype(np.float32)]

def convert_to_tflite_int8(model_path=None, output_path=None):
    base_dir = os.path.dirname(__file__)
    if model_path is None:
        model_path = os.path.abspath(os.path.join(base_dir, "..", "model", "best2.pt"))
    if output_path is None:
        output_path = os.path.abspath(os.path.join(base_dir, "model_int8.tflite"))

    dataset_dir = os.path.abspath(os.path.join(base_dir, "..", "dataset", "Defect Detection.v1i.yolov8"))

    print("\n" + "="*65)
    print("      M2 TFLITE INT8 QUANTIZATION & CALIBRATION ENGINE       ")
    print("="*65)
    print(f"[*] Source PyTorch Model : {model_path}")
    print(f"[*] Target TFLite INT8   : {output_path}")
    print(f"[*] Calibration Dataset  : {dataset_dir}")

    try:
        from ultralytics import YOLO
        print("[*] Loading YOLOv8 model...")
        model = YOLO(model_path)

        print("[*] Exporting to TFLite INT8 with PTQ calibration...")
        tflite_path = model.export(
            format="tflite",
            int8=True,
            data=os.path.join(dataset_dir, "data.yaml"),
            imgsz=416
        )
        print(f"[+] Quantization successful: {tflite_path}")
        return tflite_path

    except Exception as e:
        print(f"[!] Direct export via Ultralytics: {e}")
        print("[*] For target Raspberry Pi 5 execution, run:")
        print(f"    yolo export model={model_path} format=tflite int8=True imgsz=416 data='{dataset_dir}/data.yaml'")
        return None

if __name__ == "__main__":
    convert_to_tflite_int8()
