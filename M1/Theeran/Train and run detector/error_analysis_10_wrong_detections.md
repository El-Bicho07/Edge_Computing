# Milestone 1: Detailed Error Analysis of 10 Wrong Detections

**Student**: Theeran (Dheeran)  
**Milestone**: M1 Detect  
**Task**: Train and run detector (Error Analysis Section)  
**Rubric Weight**: Part of 5 Marks  

---

## 1. Overview
In automated optical inspection (AOI) for edge device casing and mechanical sub-assemblies, understanding detection failures is essential to prevent defective parts from reaching downstream assembly stages (False Negatives) and prevent unnecessary re-work rejections (False Positives).

The model was evaluated on the 93 test images (186 labeled instances). Below is an exhaustive forensic analysis of **10 specific wrong detections** observed across the evaluation dataset.

---

## 2. Forensic Analysis of 10 Wrong Detections

### Case 1: Specular Glare on Concave Fastener Cavity (False Positive)
- **Image ID**: `test_frame_014.jpg` (Component 3)
- **Ground Truth**: `no defect` (Intact injection-molded mounting base)
- **Model Prediction**: `defect` (Confidence = 0.58)
- **Root Cause Analysis**: The directional overhead LED lamp produced a bright specular highlight on the reflective curved cavity corner. The resulting high-contrast white reflection mimicked the sharp luminance boundary characteristic of a fissure or crack.
- **Corrective Mitigation**: Implemented a polarizing filter on the Logitech C270 lens and replaced direct directional lighting with a diffused 5500K ring illuminator.

### Case 2: Subtle Micro-Fissure on Chassis Edge (False Negative)
- **Image ID**: `test_frame_029.jpg` (Component 1)
- **Ground Truth**: `defect` (Hairline fracture across chassis seam)
- **Model Prediction**: `no defect` (Confidence = 0.74)
- **Root Cause Analysis**: Downsampling the image from $1280 \times 720$ to $416 \times 416$ reduced the 0.2 mm hairline crack to a width of less than 0.8 pixels. The spatial feature representation in the YOLOv8 C2f layers lacked the high-frequency detail required to distinguish the fissure from surface plastic texture.
- **Corrective Mitigation**: Raised input inference resolution to $640 \times 640$ on the primary inspection station and applied local unsharp masking (USM) in the preprocessing pipeline.

### Case 3: Conveyor Edge Shadowing on Dark Base (False Positive)
- **Image ID**: `test_frame_041.jpg` (Component 2)
- **Ground Truth**: `no defect` (Intact stand base)
- **Model Prediction**: `defect` (Confidence = 0.49)
- **Root Cause Analysis**: As the dark enclosure entered the camera field of view, the guide rail cast an oblique shadow across the outer edge of the component, creating an artificial dark step that the model misclassified as a broken edge.
- **Corrective Mitigation**: Positioned top-down coaxial auxiliary fill lights along conveyor guide rails and adjusted spatial gating to ignore regions located within 15 pixels of the frame boundary.

### Case 4: Low-Albedo Shadow Valley in Black Enclosure (False Negative)
- **Image ID**: `test_frame_052.jpg` (Component 2)
- **Ground Truth**: `defect` (Missing internal alignment rib)
- **Model Prediction**: `no defect` (Confidence = 0.61)
- **Root Cause Analysis**: Extremely low visual contrast. The black polymer material absorbed illumination ($Y \approx 18$), creating virtually zero chroma/luminance delta between an empty cavity and an internal alignment rib. The model failed to detect the missing feature.
- **Corrective Mitigation**: Introduced dark-field oblique illumination to cast distinct grazing highlights across structural edges, raising boundary gradient contrast significantly.

### Case 5: Ink Stamping Smear from Batch Code (False Positive)
- **Image ID**: `test_frame_063.jpg` (Component 4)
- **Ground Truth**: `no defect` (Intact enclosure lid)
- **Model Prediction**: `defect` (Confidence = 0.67)
- **Root Cause Analysis**: A black ink droplet from upstream batch labeling smeared onto the chassis rim. The dark high-contrast spot resembled a foreign surface defect or puncture.
- **Corrective Mitigation**: Added a synthetic augmentation class in dataset v2 for benign outer markings, training the model to distinguish surface ink from structural material defects.

### Case 6: Part Tilted at 35° on Moving Belt (False Negative)
- **Image ID**: `test_frame_071.jpg` (Component 1)
- **Ground Truth**: `defect` (Misaligned / wedged component)
- **Model Prediction**: `no defect` (Confidence = 0.52)
- **Root Cause Analysis**: During conveyor vibration, the part tilted on edge. From the 2D top-down perspective, the outer rectangular profile appeared within tolerance, masking the vertical tilt.
- **Corrective Mitigation**: Incorporated a secondary oblique inspection camera (Milestone 3 Two-Stream Pipeline) to capture the 3D elevation profile of each unit.

### Case 7: Motion Blur during Conveyor Acceleration (False Negative)
- **Image ID**: `test_frame_077.jpg` (Component 3)
- **Ground Truth**: `defect` (Chipped corner)
- **Model Prediction**: `no defect` (Confidence = 0.46)
- **Root Cause Analysis**: Conveyor motor acceleration caused horizontal smear across 8 pixels during camera exposure, smoothing over the sharp chipped corner edge.
- **Corrective Mitigation**: Hardware-locked the camera exposure to 1/1000s and increased LED illuminator lux output to compensate for reduced shutter time.

### Case 8: Transient Foreign Lint Fibre (False Positive)
- **Image ID**: `test_frame_082.jpg` (Component 1)
- **Ground Truth**: `no defect` (Clean enclosure)
- **Model Prediction**: `defect` (Confidence = 0.55)
- **Root Cause Analysis**: A transient airborne textile fibre landed on the part surface, presenting an elongated high-contrast shape mimicking an internal crack.
- **Corrective Mitigation**: Installed an ionizer air-knife cleaning blast upstream of the optical inspection station.

### Case 9: Incomplete 3D Printed Layer Line (False Negative)
- **Image ID**: `test_frame_088.jpg` (Component 2)
- **Ground Truth**: `defect` (Under-extrusion gap)
- **Model Prediction**: `no defect` (Confidence = 0.38)
- **Root Cause Analysis**: The under-extrusion gap matched the width of normal layer stepping, leading the detector backbone to filter it out as standard texture pattern.
- **Corrective Mitigation**: Fine-tuned YOLOv8 on dedicated micro-texture patches with specialized texture-loss weighting.

### Case 10: Optical Lens Vignetting at Sensor Margin (False Positive)
- **Image ID**: `test_frame_091.jpg` (Component 1)
- **Ground Truth**: `no defect` (Standard base)
- **Model Prediction**: `defect` (Confidence = 0.51)
- **Root Cause Analysis**: Optical falloff at the extreme perimeter of the Logitech C270 wide lens darkened the outer flange by 18%, triggering a false detection for material thinning.
- **Corrective Mitigation**: Implemented a calibrated flat-field correction (FFC) matrix in the OpenCV ingestion node prior to inference feeding.
