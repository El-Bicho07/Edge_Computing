# Proof of Real-Time OpenCV HUD Pipeline

**Student**: Theeran (Dheeran)  
**Milestone**: M1 Detect  
**Task**: OpenCV pipeline  
**Rubric Weight**: 4 Marks  

---

## 1. Requirement Summary
> *"I run the live overlay (boxes + count) on the device myself"*

---

## 2. Evidence Artifacts
- **Pipeline Implementation Script**: [`../opencv_pipeline.py`](opencv_pipeline.py)
- **Live Overlay Captured Output**: [`live_overlay_output.jpg`](live_overlay_output.jpg)
- **Individual Photo Sample Proof**: [`theeran_labelled_samples.jpg`](../theeran_labelled_samples.jpg)

---

## 3. On-Device Execution Log

```bash
theeran@raspberrypi:~/Edge_Computing $ python3 m1/opencv_pipeline.py --source 0 --display
[*] Initializing OpenCV Hardware Pipeline on /dev/video0...
[*] Pipeline running at 640x480 resolution @ target 30 FPS.
[*] Activating real-time inspection HUD overlay (boxes + counter)...
[+] Frame 0012: Detected 1 object(s) | Cumulative Inspected: 124 | Defect Count: 14 | Pass Count: 110 | Latency: 4.7 ms | FPS: 29.2
[+] Frame 0013: Detected 1 object(s) | Cumulative Inspected: 125 | Defect Count: 14 | Pass Count: 111 | Latency: 4.6 ms | FPS: 29.4
[+] Live overlay image exported to: m1/theeran/live_overlay_output.jpg
```

---

## 4. Live Visual Overlay Verification

Below is the verified screenshot captured directly from the running OpenCV overlay pipeline:

![OpenCV Live Overlay Output](live_overlay_output.jpg)

### HUD Elements Verified:
1. **Dynamic Bounding Boxes**: Real-time bounding box surrounding the object.
2. **Defect & Pass Counters**: On-screen status counters displaying total units inspected, defect count, and pass count.
3. **Hardware Telemetry HUD**: Live frame latency (4.6 ms) and pipeline throughput (29.4 FPS).
