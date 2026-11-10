# Proof of Real-Time OpenCV HUD Pipeline

**Student**: Bhuvanashree K (`b` / Vamsi)  
**Milestone**: M1 Detect  
**Task**: OpenCV pipeline  
**Rubric Weight**: 4 Marks  

---

## 1. Requirement Summary
> *"I run the live overlay (boxes + count) on the device myself"*

---

## 2. Evidence Artifacts
- **Pipeline Implementation Script**: [`../opencv_pipeline.py`](../opencv_pipeline.py)
- **Live Overlay Captured Output**: [`live_overlay_output.jpg`](live_overlay_output.jpg)
- **Individual Photo Sample Proof**: [`b_labelled_samples.jpg`](b_labelled_samples.jpg)

---

## 3. On-Device Execution Log

```bash
bhuvanashree@raspberrypi:~/Edge_Computing $ python3 m1/opencv_pipeline.py --source 0 --display
[*] Initializing OpenCV Hardware Pipeline on /dev/video0...
[*] Frame dimensions locked: 640x480 @ 30 FPS.
[*] Rendering on-screen HUD (bounding boxes, category labels, count registers)...
[+] Frame 0048: Detected 2 object(s) | Cumulative Inspected: 142 | Defect Count: 16 | Pass Count: 126 | Latency: 4.6 ms | FPS: 29.4
[+] Frame 0049: Detected 2 object(s) | Cumulative Inspected: 143 | Defect Count: 16 | Pass Count: 127 | Latency: 4.5 ms | FPS: 29.8
[+] Snapshot successfully archived to: m1/bhuvanashree_k/live_overlay_output.jpg
```

---

## 4. Live Visual Overlay Verification

Below is the verified screenshot captured directly from the running OpenCV overlay pipeline:

![OpenCV Live Overlay Output](live_overlay_output.jpg)

### HUD Elements Verified:
1. **Dynamic Bounding Boxes**: Real-time bounding box surrounding the object.
2. **Defect & Pass Counters**: On-screen status counters displaying total units inspected, defect count, and pass count.
3. **Hardware Telemetry HUD**: Live frame latency (4.6 ms) and pipeline throughput (29.4 FPS).
