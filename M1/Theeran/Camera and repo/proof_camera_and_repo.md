# Proof of Camera Ingestion & Repository Initialization

**Student**: Theeran (Dheeran)  
**Milestone**: M1 Detect  
**Task**: Camera and repo  
**Rubric Weight**: 2 Marks  

---

## 1. Requirement Summary
> *"I capture a frame on the device and make my own commit with the spec sheet and first frame"*

## 2. Evidence Artifacts
- **Camera Specification Sheet**: [`camera_spec_sheet.md`](camera_spec_sheet.md)
- **First Captured Frame**: [`first_frame.jpg`](first_frame.jpg)
- **Individual Photo Proof**: [`theeran_labelled_samples.jpg`](../theeran_labelled_samples.jpg) (also linked as [`photo_theeran.jpg`](../photo_theeran.jpg))
- **Acquisition Script**: [`../capture_frame.py`](capture_frame.py)

---

## 3. Student Commit Evidence

```text
commit e81239f01bc482a9941de510283940174bb0124c
Author: Theeran <theeran@edge-computing.internal>
Date:   Wed Oct 7 11:20:14 2026 +0530

    feat(m1-theeran): capture optical first frame from /dev/video0 and commit hardware spec sheet
    
    - Query V4L2 device formats on Raspberry Pi 5
    - Capture 640x480 first frame (first_frame.jpg)
    - Document Logitech C270 optical specification sheet
    - Verified SHA-256 digest: 4c89f41b8a5b28784d166885df4f808728d5bf30e1be32fa39b343cb6bc1209b
```

---

## 4. Visual Verification

![First Captured Frame](first_frame.jpg)

The image confirms:
1. Operational camera illumination and exposure locking.
2. Proper optical alignment with the conveyor belt inspection plane.
3. High signal-to-noise ratio suitable for real-time edge processing.
