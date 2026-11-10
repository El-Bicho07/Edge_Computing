#!/usr/bin/env python3
"""
Milestone 3: Asynchronous Two-Stream Concurrent Inspection Pipeline
Veyra Pharma Vision Edge System

Runs two simultaneous video streams on Raspberry Pi 5:
- Stream 1: Primary Top-Down Inspection Camera (/dev/video0 or fallback)
- Stream 2: Secondary Oblique Side-Seal Camera (/dev/video2 or simulated stream)
Measures and logs throughput (FPS) per stream independently without thread locking.
"""

import os
import sys
import time
import threading
import cv2
import numpy as np

class VideoStreamWorker(threading.Thread):
    def __init__(self, stream_id, name, source=0, width=640, height=480, max_frames=150):
        super().__init__(name=name)
        self.stream_id = stream_id
        self.stream_name = name
        self.source = source
        self.width = width
        self.height = height
        self.max_frames = max_frames

        self.running = True
        self.frame_count = 0
        self.fps_measured = 0.0
        self.latencies = []
        self._lock = threading.Lock()

    def run(self):
        print(f"[*] Starting {self.stream_name} (Source: {self.source})...")
        cap = cv2.VideoCapture(self.source)
        use_fallback = not cap.isOpened()

        if use_fallback:
            # Generate or load synthetic test frames
            base_dir = os.path.dirname(__file__)
            img_path = os.path.join(base_dir, "..", "m1", "first_frame.jpg")
            base_frame = cv2.imread(img_path) if os.path.exists(img_path) else np.zeros((self.height, self.width, 3), dtype=np.uint8)
            base_frame = cv2.resize(base_frame, (self.width, self.height))

        t_start = time.perf_counter()
        prev_time = t_start

        while self.running and self.frame_count < self.max_frames:
            t0 = time.perf_counter()

            if not use_fallback:
                ret, frame = cap.read()
                if not ret or frame is None:
                    break
            else:
                # Add motion variation per stream
                frame = base_frame.copy()
                shift = int((self.frame_count * (4 if self.stream_id == 1 else 6)) % 200)
                color = (0, 255, 0) if self.stream_id == 1 else (255, 100, 0)
                cv2.circle(frame, (100 + shift, 200), 25, color, -1)
                cv2.putText(frame, f"{self.stream_name} - Frame {self.frame_count}", (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                time.sleep(0.030) # Simulated camera acquisition rate (~30 FPS)

            # Processing workload: Convert color, resize, apply spatial thresholding
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _ = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

            t1 = time.perf_counter()
            self.latencies.append((t1 - t0) * 1000.0)

            self.frame_count += 1
            dt = t1 - prev_time
            prev_time = t1
            self.fps_measured = 0.9 * self.fps_measured + 0.1 * (1.0 / max(dt, 1e-6))

        total_elapsed = time.perf_counter() - t_start
        self.fps_measured = self.frame_count / max(total_elapsed, 1e-6)

        if not use_fallback:
            cap.release()
        print(f"[+] {self.stream_name} Completed: {self.frame_count} frames | Average Rate: {self.fps_measured:.2f} FPS")

    def stop(self):
        self.running = False

def run_two_stream_pipeline(duration_frames=120):
    print("\n" + "="*70)
    print("      M3 TWO-STREAM CONCURRENT INSPECTION PIPELINE BENCHMARK      ")
    print("="*70)
    print("[*] Stream 1: Top-Down Primary Defect Camera")
    print("[*] Stream 2: Oblique Side-Seal Inspection Camera")
    print(f"[*] Processing Target: {duration_frames} frames per stream concurrently\n")

    worker1 = VideoStreamWorker(stream_id=1, name="Stream 1 [Top-Down Camera]", source=0, max_frames=duration_frames)
    worker2 = VideoStreamWorker(stream_id=2, name="Stream 2 [Oblique Seal Camera]", source=2, max_frames=duration_frames)

    start_all = time.perf_counter()
    worker1.start()
    worker2.start()

    # Monitor periodically
    while worker1.is_alive() or worker2.is_alive():
        time.sleep(1.0)
        print(f"--> [Throughput Telemetry] Stream 1: {worker1.fps_measured:.1f} FPS ({worker1.frame_count} frames) | "
              f"Stream 2: {worker2.fps_measured:.1f} FPS ({worker2.frame_count} frames)")

    worker1.join()
    worker2.join()
    total_time = time.perf_counter() - start_all

    print("\n" + "="*70)
    print("               CONCURRENT PIPELINE SUMMARY               ")
    print("="*70)
    print(f"Total Test Duration   : {total_time:.2f} seconds")
    print(f"Stream 1 Final Rate   : {worker1.fps_measured:.2f} FPS (Median Latency: {np.median(worker1.latencies):.2f} ms)")
    print(f"Stream 2 Final Rate   : {worker2.fps_measured:.2f} FPS (Median Latency: {np.median(worker2.latencies):.2f} ms)")
    print(f"Combined Throughput   : {worker1.fps_measured + worker2.fps_measured:.2f} Total Frames/Sec")
    print("="*70 + "\n")

    return {
        "stream1_fps": worker1.fps_measured,
        "stream2_fps": worker2.fps_measured,
        "total_time": total_time
    }

if __name__ == "__main__":
    run_two_stream_pipeline()
