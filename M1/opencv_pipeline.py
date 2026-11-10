#!/usr/bin/env python3
"""
Milestone 1: Real-Time Classical OpenCV Pipeline with Live Overlay
Veyra Pharma Vision Edge System

Demonstrates live optical overlay on Raspberry Pi 5:
- Adaptive MOG2 background subtraction
- Morphological cleaning (Open + Dilate)
- Contour extraction and bounding box localization
- Live object count HUD overlay
- Real-time FPS and latency calculation
"""

import os
import sys
import time
import cv2
import numpy as np

def run_opencv_pipeline(source=0, max_frames=300, min_area=450, display=False):
    print("\n" + "="*60)
    print("   VEYRA PHARMA VISION: OPENCV LIVE OVERLAY PIPELINE   ")
    print("="*60)
    print(f"[*] Initializing video source: {source}")
    print(f"[*] Minimum contour area threshold: {min_area} px")

    cap = cv2.VideoCapture(source)
    use_fallback = False
    
    if not cap.isOpened():
        print("[!] Hardware video device not available. Switching to simulated edge video stream...")
        use_fallback = True
        sample_img_path = os.path.join(os.path.dirname(__file__), "first_frame.jpg")
        if not os.path.exists(sample_img_path):
            sample_img_path = os.path.join(os.path.dirname(__file__), "..", "Pictures", "test_frame.jpg")
        base_img = cv2.imread(sample_img_path) if os.path.exists(sample_img_path) else np.zeros((480, 640, 3), dtype=np.uint8)

    # Initialize MOG2 Background Subtractor
    subtractor = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=40, detectShadows=True)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    frame_count = 0
    start_time = time.perf_counter()
    prev_time = start_time
    fps_smooth = 24.0

    output_dir = os.path.dirname(__file__)
    saved_sample_path = os.path.join(output_dir, "live_overlay_output.jpg")

    try:
        while frame_count < max_frames:
            t0 = time.perf_counter()
            
            if not use_fallback:
                ret, frame = cap.read()
                if not ret or frame is None:
                    break
            else:
                # Synthesize motion across conveyor field
                frame = base_img.copy()
                offset = int((frame_count * 5) % (frame.shape[1] - 120))
                # Add simulated moving blister pack object
                cv2.rectangle(frame, (offset, 180), (offset + 140, 300), (200, 200, 200), -1)
                cv2.circle(frame, (offset + 35, 215), 15, (50, 50, 50), -1)
                cv2.circle(frame, (offset + 105, 215), 15, (50, 50, 50), -1)
                cv2.circle(frame, (offset + 35, 265), 15, (50, 50, 50), -1)
                cv2.circle(frame, (offset + 105, 265), 15, (50, 50, 50), -1)
                time.sleep(0.033) # 30 FPS throttle

            # Preprocessing: Grayscale & Blur
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Apply MOG2 Subtraction
            fg_mask = subtractor.apply(blurred)

            # Morphological noise removal
            cleaned = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=1)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_DILATE, kernel, iterations=2)

            # Contour Detection
            contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            detected_boxes = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area >= min_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    detected_boxes.append((x, y, w, h, area))

            # Render Overlay HUD
            overlay = frame.copy()
            object_count = len(detected_boxes)

            # Draw bounding boxes & labels
            for idx, (x, y, w, h, area) in enumerate(detected_boxes, 1):
                cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 2)
                label = f"Item #{idx} ({int(area)}px)"
                cv2.putText(overlay, label, (x, max(20, y - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # Draw center crosshair
                cx, cy = x + w // 2, y + h // 2
                cv2.circle(overlay, (cx, cy), 4, (0, 0, 255), -1)

            # Calculate Latency & FPS
            t1 = time.perf_counter()
            latency_ms = (t1 - t0) * 1000.0
            dt = t1 - prev_time
            prev_time = t1
            inst_fps = 1.0 / max(dt, 1e-6)
            fps_smooth = 0.9 * fps_smooth + 0.1 * inst_fps

            # Render HUD Banners
            cv2.rectangle(overlay, (10, 10), (330, 95), (0, 0, 0), -1)
            cv2.rectangle(overlay, (10, 10), (330, 95), (0, 255, 255), 1)

            cv2.putText(overlay, "M1 OPENCV LIVE OVERLAY", (20, 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(overlay, f"Objects In View : {object_count}", (20, 52),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if object_count > 0 else (200, 200, 200), 2)
            cv2.putText(overlay, f"Throughput Rate : {fps_smooth:.1f} FPS", (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(overlay, f"Frame Latency   : {latency_ms:.1f} ms", (20, 88),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            frame_count += 1
            if frame_count % 30 == 0:
                print(f"[Frame {frame_count:03d}] Objects: {object_count} | FPS: {fps_smooth:.1f} | Latency: {latency_ms:.1f} ms")

            # Save sample overlay frame
            if frame_count == 40 or (frame_count == 1 and not os.path.exists(saved_sample_path)):
                cv2.imwrite(saved_sample_path, overlay)

            if display:
                cv2.imshow("M1 Live OpenCV Overlay", overlay)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    finally:
        if not use_fallback:
            cap.release()
        if display:
            cv2.destroyAllWindows()

    total_time = time.perf_counter() - start_time
    avg_fps = frame_count / max(total_time, 1e-6)
    print("\n[+] OpenCV Pipeline Test Completed Successfully.")
    print(f"[+] Total Frames Processed: {frame_count}")
    print(f"[+] Average Throughput   : {avg_fps:.2f} FPS")
    print(f"[+] Saved Overlay Proof   : {saved_sample_path}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_opencv_pipeline(max_frames=60, display=False)
