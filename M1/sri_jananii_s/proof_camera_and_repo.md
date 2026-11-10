# Proof of Camera Ingestion & Repository Initialization

**Student**: Sri Jananii S (`sri` / Sri Janani S)  
**Milestone**: M1 Detect  
**Task**: Camera and repo  
**Rubric Weight**: 2 Marks  

---

## 1. Requirement Summary
> *"I capture a frame on the device and make my own commit with the spec sheet and first frame"*

## 2. Evidence Artifacts
- **Camera Specification Sheet**: [`camera_spec_sheet.md`](camera_spec_sheet.md)
- **First Captured Frame**: [`first_frame.jpg`](first_frame.jpg)
- **Individual Photo Proof**: [`sri_labelled_samples.jpg`](sri_labelled_samples.jpg) (also linked as [`sri.jpg`](sri.jpg))
- **Acquisition Script**: [`../capture_frame.py`](../capture_frame.py)

---

## 3. Student Commit Evidence

```text
commit f389e17b81920ac3918f0291471029487192bc01
Author: Sri Jananii S <sri.jananii@edge-computing.internal>
Date:   Wed Oct 7 10:25:02 2026 +0530

    feat(m1-srijananii): register camera sensor spec sheet and push first operational frame
    
    - Validate /dev/video0 optical capture stream on Raspberry Pi 5
    - Measure channel intensity statistics and calculate SHA-256 hash
    - Document UVC 1.1 camera characteristics and fixed focal distance
    - Hash: 4c89f41b8a5b28784d166885df4f808728d5bf30e1be32fa39b343cb6bc1209b
```

---

## 4. Visual Verification

![First Captured Frame](first_frame.jpg)
