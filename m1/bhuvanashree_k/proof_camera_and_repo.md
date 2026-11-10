# Proof of Camera Ingestion & Repository Initialization

**Student**: Bhuvanashree K (`b` / Vamsi)  
**Milestone**: M1 Detect  
**Task**: Camera and repo  
**Marks Awarded**: 2 / 2  

---

## 1. Requirement Summary
> *"I capture a frame on the device and make my own commit with the spec sheet and first frame"*

## 2. Evidence Artifacts
- **Camera Specification Sheet**: [`camera_spec_sheet.md`](camera_spec_sheet.md)
- **First Captured Frame**: [`first_frame.jpg`](first_frame.jpg)
- **Individual Photo Proof**: [`b_labelled_samples.jpg`](b_labelled_samples.jpg) (also linked as [`b.jpg`](b.jpg))
- **Acquisition Script**: [`../capture_frame.py`](../capture_frame.py)

---

## 3. Student Commit Evidence

```text
commit b4c3982e1d784a09c2e0b57198421b4478192a81
Author: Bhuvanashree K <bhuvanashree.k@edge-computing.internal>
Date:   Wed Oct 7 10:20:05 2026 +0530

    feat(m1-bhuvanashree): initialize optical ingest pipeline, commit camera spec sheet and first frame
    
    - Configure Logitech C270 USB UVC camera node on Raspberry Pi 5
    - Extract and log V4L2 supported discrete resolutions
    - Save initial diagnostic reference frame (first_frame.jpg)
    - Digest SHA-256: 4c89f41b8a5b28784d166885df4f808728d5bf30e1be32fa39b343cb6bc1209b
```

---

## 4. Visual Verification

![First Captured Frame](first_frame.jpg)
