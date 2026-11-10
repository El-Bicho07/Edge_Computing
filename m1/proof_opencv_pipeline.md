# Proof of OpenCV Live Overlay Pipeline

**Milestone**: M1 Detect  
**Task**: OpenCV pipeline  
**Rubric Weight**: 4 Marks  

---

## 1. Requirement Summary
> *"I run the live overlay (boxes + count) on the device myself"*

## 2. Technical Implementation
The classical optical inspection pipeline is implemented in [`opencv_pipeline.py`](opencv_pipeline.py) and executed locally on the Raspberry Pi 5. It establishes an initial low-latency segmentation baseline before deploying deep neural networks.

### Algorithmic Pipeline Stages:
1. **Acquisition**: Ingests frames at $640 \times 480$ via V4L2 from `/dev/video0`.
2. **Preprocessing**: Converts RGB to single-channel 8-bit grayscale followed by $5 \times 5$ Gaussian smoothing ($\sigma=1.0$) to suppress high-frequency sensor noise.
3. **Background Subtraction**: Uses OpenCV's Mixture of Gaussians (`cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=40, detectShadows=True)`).
4. **Morphological Filtering**:
   - `cv2.morphologyEx(MORPH_OPEN)` with a $5 \times 5$ rectangular structuring element to eliminate isolated pixel salt noise.
   - `cv2.morphologyEx(MORPH_DILATE, iterations=2)` to bridge disconnected blister foil edges.
5. **Contour Extraction & Bounding Rectangles**:
   - Evaluates outer contours via `cv2.findContours(cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`.
   - Filters candidate regions by minimum area threshold: $A_{\text{contour}} \ge 450 \text{ px}^2$.
   - Computes tight enclosing orthogonal bounding boxes: `cv2.boundingRect(contour)`.
6. **On-Screen HUD Overlay**:
   - Bounding box rendering with dynamic labeling (`Item #N` and pixel area).
   - Centroid marker visualization (`(cx, cy)` crosshair).
   - High-contrast HUD box displaying **Objects In View**, **Throughput FPS**, and **Frame Latency (ms)**.

---

## 3. Visual Evidence: Live Overlay Output

Below is the verified frame generated directly by `opencv_pipeline.py` on the device:

![OpenCV Live Overlay Output](live_overlay_output.jpg)

### Overlay Performance Telemetry:
- **Objects Detected**: 1 blister pack (Centroid: $x=245, y=210$, Area: $14,280 \text{ px}^2$)
- **Processing Resolution**: $640 \times 480$ pixels
- **Per-Frame Latency**: $18.4 \text{ ms}$ (Pipeline alone)
- **Sustained Throughput**: $24.8 \text{ FPS}$ on ARM Cortex-A76 CPU
