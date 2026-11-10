#!/usr/bin/env python3
"""
Milestone 1: YOLOv8 Blister Pack Defect Detector Training Script
Veyra Pharma Vision Edge System

Trains YOLOv8n on the custom 929-image Roboflow pharmaceutical defect dataset.
"""

import os
import sys

def train_blister_detector(epochs=50, img_size=416, batch_size=16, model_type="yolov8n.pt"):
    print("\n" + "="*65)
    print("      M1 YOLOv8 BLISTER PACK DEFECT DETECTOR TRAINING      ")
    print("="*65)
    print(f"[*] Base Weights      : {model_type}")
    print(f"[*] Training Epochs   : {epochs}")
    print(f"[*] Input Resolution  : {img_size} x {img_size}")
    print(f"[*] Batch Size        : {batch_size}")

    data_yaml = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "dataset", "Defect Detection.v1i.yolov8", "data.yaml"
    ))
    print(f"[*] Dataset Config    : {data_yaml}")

    try:
        from ultralytics import YOLO
    except ImportError:
        print("[!] Ultralytics library not installed in current environment.")
        print("[*] To execute training on Raspberry Pi 5 / GPU host:")
        print("    pip install ultralytics")
        print("    python3 m1/train_detector.py")
        return None

    # Load baseline model
    model = YOLO(model_type)

    # Train model
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        patience=15,
        save=True,
        device="0" if sys.platform != "darwin" else "mps",
        workers=4,
        optimizer="SGD",
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        plots=True,
        name="blister_defect_detector"
    )

    print("\n[+] Training session finished.")
    return results

if __name__ == "__main__":
    train_blister_detector()
