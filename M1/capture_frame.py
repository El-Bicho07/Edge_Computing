#!/usr/bin/env python3
"""
Milestone 1: Camera Acquisition and Frame Verification Script
Veyra Pharma Vision Edge System

Captures a diagnostic frame from /dev/video0 (or mock test frame if camera is unavailable),
computes image telemetry (resolution, channels, mean intensity, SHA-256), and saves first_frame.jpg.
"""

import os
import sys
import time
import hashlib
import cv2
import numpy as np

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "first_frame.jpg")
FALLBACK_SOURCE = os.path.join(os.path.dirname(__file__), "..", "Pictures", "test_frame.jpg")

def capture_diagnostic_frame(device_index=0, width=640, height=480):
    print(f"[*] Initializing optical capture device index {device_index}...")
    cap = cv2.VideoCapture(device_index, cv2.CAP_V4L2 if sys.platform.startswith("linux") else cv2.CAP_ANY)
    
    frame = None
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # Flush initial 5 frames for auto-exposure stabilization
        for _ in range(5):
            cap.read()
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None:
            print("[+] Live frame successfully acquired from hardware camera.")
    
    if frame is None:
        print("[!] Camera hardware node busy or not detected. Loading repository verification frame...")
        if os.path.exists(FALLBACK_SOURCE):
            frame = cv2.imread(FALLBACK_SOURCE)
            print(f"[+] Loaded verified edge reference frame from: {FALLBACK_SOURCE}")
        else:
            # Generate synthetic calibration pattern
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            cv2.rectangle(frame, (100, 100), (540, 380), (50, 50, 50), -1)
            cv2.putText(frame, "Veyra Edge Diagnostic Frame", (120, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            print("[+] Generated synthetic optical calibration frame.")

    # Calculate telemetry
    h, w, c = frame.shape
    mean_val = float(np.mean(frame))
    std_val = float(np.std(frame))
    
    # Save frame
    cv2.imwrite(OUTPUT_PATH, frame)
    file_bytes = open(OUTPUT_PATH, "rb").read()
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()

    print("\n" + "="*50)
    print("      FRAME ACQUISITION TELEMETRY REPORT      ")
    print("="*50)
    print(f"Target Path     : {OUTPUT_PATH}")
    print(f"Resolution      : {w} x {h} (Aspect Ratio: {w/h:.2f}:1)")
    print(f"Color Channels  : {c} (BGR format)")
    print(f"Mean Intensity  : {mean_val:.2f} / 255.0")
    print(f"Std Deviation   : {std_val:.2f}")
    print(f"File Size       : {len(file_bytes):,} bytes")
    print(f"SHA-256 Digest  : {sha256_hash}")
    print("="*50 + "\n")
    return OUTPUT_PATH, sha256_hash

if __name__ == "__main__":
    capture_diagnostic_frame()
