#!/usr/bin/env python3
"""
Milestone 2: PyTorch to ONNX Model Export Script
Veyra Pharma Vision Edge System

Exports trained YOLOv8 defect detection weights (best2.pt) to ONNX format
optimized for edge CPU/GPU inference with static batch size 1 and opset 17.
"""

import os
import sys
import time

def export_model_to_onnx(model_path=None, output_path=None, imgsz=(416, 416), opset=17):
    base_dir = os.path.dirname(__file__)
    if model_path is None:
        model_path = os.path.abspath(os.path.join(base_dir, "..", "model", "best2.pt"))
    if output_path is None:
        output_path = os.path.abspath(os.path.join(base_dir, "model.onnx"))

    print("\n" + "="*65)
    print("         M2 YOLOv8 TO ONNX EXPORT ENGINE         ")
    print("="*65)
    print(f"[*] Input PyTorch Checkpoint : {model_path}")
    print(f"[*] Target ONNX File         : {output_path}")
    print(f"[*] Input Tensor Dimensions  : 1 x 3 x {imgsz[0]} x {imgsz[1]}")
    print(f"[*] ONNX Opset Version       : {opset}")

    if not os.path.exists(model_path):
        print(f"[!] Error: Model checkpoint not found at: {model_path}")
        return False

    t0 = time.perf_counter()
    try:
        from ultralytics import YOLO
        print("[*] Loading YOLOv8 model into memory...")
        model = YOLO(model_path)

        print("[*] Initiating ONNX export with simplification...")
        exported_path = model.export(
            format="onnx",
            imgsz=imgsz,
            opset=opset,
            simplify=True,
            dynamic=False,
            batch=1
        )
        t_export = time.perf_counter() - t0
        print(f"[+] ONNX export completed in {t_export:.2f} seconds.")
        print(f"[+] Exported Artifact: {exported_path}")

        # Check file size
        if os.path.exists(exported_path):
            size_mb = os.path.getsize(exported_path) / (1024 * 1024)
            print(f"[+] Model Disk Size  : {size_mb:.2f} MB")
            return exported_path

    except Exception as e:
        print(f"[!] Ultralytics export unavailable ({e}).")
        print("[*] On Raspberry Pi 5 / Linux target, execute:")
        print(f"    yolo export model={model_path} format=onnx imgsz={imgsz[0]} opset={opset} simplify=True")
        return None

if __name__ == "__main__":
    export_model_to_onnx()
