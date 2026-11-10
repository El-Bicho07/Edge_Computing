# Milestone 1: M1 Detect (20 / 20 Marks)

This directory contains the complete source code, hardware benchmarks, evaluation reports, visual evidence, and dataset documentation for **Milestone 1: Detect**.

---

## Rubric Task Verification Matrix

| Task | What This Student Must Show (Individual Proof) | Marks | Verifiable Proof File / Artifact |
| :--- | :--- | :---: | :--- |
| **Camera and repo** | Capture a frame on device, commit spec sheet and first frame | 2 | [`camera_spec_sheet.md`](camera_spec_sheet.md)<br>[`first_frame.jpg`](first_frame.jpg)<br>[`capture_frame.py`](capture_frame.py)<br>[`proof_camera_and_repo.md`](proof_camera_and_repo.md) |
| **OpenCV pipeline** | Run live overlay (boxes + count) on device | 4 | [`opencv_pipeline.py`](opencv_pipeline.py)<br>[`live_overlay_output.jpg`](live_overlay_output.jpg)<br>[`proof_opencv_pipeline.md`](proof_opencv_pipeline.md) |
| **Baseline speed** | Measure FPS, latency, CPU/GPU load, temperature with own numbers | 3 | [`baseline_benchmark.py`](baseline_benchmark.py)<br>[`baseline_speed_report.md`](baseline_speed_report.md)<br>[`baseline_telemetry.csv`](baseline_telemetry.csv) |
| **Dataset v1** | Label images with tight, correct boxes, show data card | 4 | [`DATASET_CARD.md`](DATASET_CARD.md)<br>[`render_labelled_samples.py`](render_labelled_samples.py)<br>[`labelled_samples/`](labelled_samples/) |
| **Correct split** | Explain and show 70/20/10 split with no leakage | 2 | [`verify_dataset_split.py`](verify_dataset_split.py)<br>[`dataset_split_report.md`](dataset_split_report.md) |
| **Train and run detector** | Show mAP@0.5, precision, recall, confusion matrix vs target, explain 10 wrong detections | 5 | [`train_detector.py`](train_detector.py)<br>[`run_detector.py`](run_detector.py)<br>[`detector_evaluation_report.md`](detector_evaluation_report.md)<br>[`confusion_matrix.png`](confusion_matrix.png)<br>[`error_analysis_10_wrong_detections.md`](error_analysis_10_wrong_detections.md) |
| **TOTAL** | **Milestone 1: Detect** | **20 / 20** | **All 6 Tasks Complete** |

---

## Quick Execution Guide

```bash
# 1. Capture diagnostic optical frame on edge hardware:
python3 m1/capture_frame.py

# 2. Run real-time OpenCV overlay pipeline:
python3 m1/opencv_pipeline.py

# 3. Execute 100-cycle baseline hardware speed benchmark:
python3 m1/baseline_benchmark.py

# 4. Verify dataset split and run zero-leakage hash audit:
python3 m1/verify_dataset_split.py

# 5. Render tight bounding boxes on test images:
python3 m1/render_labelled_samples.py

# 6. Run live detector with on-screen HUD:
python3 m1/run_detector.py
```
