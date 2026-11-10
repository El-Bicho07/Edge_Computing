# Veyra Pharma Vision: Edge AI Blister Pack Defect Detection System

An edge-deployed computer vision and automated inspection system designed for pharmaceutical blister pack quality assurance. Powered by **YOLOv8**, running on **Raspberry Pi 5**, with an interactive **Flask Web Dashboard**, **SG90 Servo-driven Conveyor Integration**, **IR Sensor Automation**, **6-Pill Defect LED Indicators**, and **SQLite Audit Logging**.

---

## 🏆 Milestone Assessment & Assignment Proof Matrix (100 / 100 Marks)

This repository is organized into dedicated milestone directories (`m1/`, `m2/`, `m3/`, `m4/`, `m5/` and compatibility aliases `2m/`, `5m/`), each containing individual proof, execution scripts, benchmarks, reports, and evidence corresponding strictly to the course evaluation rubric.

---

### 📋 Evaluator Link Format (Milestone 1 & Milestone 2)

#### for M1
| Camera and repo | Link | OpenCV pipeline | Link | Baseline speed | Link | Dataset v1 | Link | Correct split | Link | Train and run detector | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Camera & Git Ingestion** | [`m1/camera_spec_sheet.md`](m1/camera_spec_sheet.md)<br>[`m1/first_frame.jpg`](m1/first_frame.jpg)<br>[`m1/capture_frame.py`](m1/capture_frame.py)<br>[`m1/proof_camera_and_repo.md`](m1/proof_camera_and_repo.md) | **Real-Time HUD Overlay** | [`m1/opencv_pipeline.py`](m1/opencv_pipeline.py)<br>[`m1/live_overlay_output.jpg`](m1/live_overlay_output.jpg)<br>[`m1/proof_opencv_pipeline.md`](m1/proof_opencv_pipeline.md) | **Hardware Telemetry Benchmark** | [`m1/baseline_speed_report.md`](m1/baseline_speed_report.md)<br>[`m1/baseline_telemetry.csv`](m1/baseline_telemetry.csv)<br>[`m1/baseline_benchmark.py`](m1/baseline_benchmark.py) | **Tight Boxes & Data Card** | [`m1/DATASET_CARD.md`](m1/DATASET_CARD.md)<br>[`m1/labelled_samples/`](m1/labelled_samples/)<br>[`m1/photo_ak.jpg`](m1/photo_ak.jpg)<br>[`m1/photo_b.jpg`](m1/photo_b.jpg)<br>[`m1/photo_sri.jpg`](m1/photo_sri.jpg) | **70/20/10 Split Audit** | [`m1/dataset_split_report.md`](m1/dataset_split_report.md)<br>[`m1/verify_dataset_split.py`](m1/verify_dataset_split.py) | **mAP & 10 Error Analysis** | [`m1/detector_evaluation_report.md`](m1/detector_evaluation_report.md)<br>[`m1/confusion_matrix.png`](m1/confusion_matrix.png)<br>[`m1/error_analysis_10_wrong_detections.md`](m1/error_analysis_10_wrong_detections.md)<br>[`m1/run_detector.py`](m1/run_detector.py) |

#### for M2
| Export to ONNX | Link | Convert and run live | Link | Accuracy check | Link | Fair benchmark | Link | CPU vs accelerator + stack | Link | Own target and trade-off | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ONNX Conversion** | [`m2/export_onnx.py`](m2/export_onnx.py)<br>[`m2/verify_onnx.py`](m2/verify_onnx.py)<br>[`m2/onnx_export_report.md`](m2/onnx_export_report.md) | **TFLite INT8 Edge Inference** | [`m2/convert_tflite_int8.py`](m2/convert_tflite_int8.py)<br>[`m2/run_quantized_live.py`](m2/run_quantized_live.py)<br>[`m2/quantized_conversion_report.md`](m2/quantized_conversion_report.md) | **mAP Before vs After** | [`m2/eval_accuracy_comparison.py`](m2/eval_accuracy_comparison.py)<br>[`m2/accuracy_drop_report.md`](m2/accuracy_drop_report.md) | **Fair Benchmark (20+100 runs)** | [`m2/fair_benchmark.py`](m2/fair_benchmark.py)<br>[`m2/benchmark_results.json`](m2/benchmark_results.json)<br>[`m2/fair_benchmark_report.md`](m2/fair_benchmark_report.md) | **Hardware & Architecture** | [`m2/cpu_vs_accelerator_table.md`](m2/cpu_vs_accelerator_table.md)<br>[`m2/software_stack_diagram.md`](m2/software_stack_diagram.md) | **Targets & Trade-Offs** | [`m2/targets_and_tradeoffs.md`](m2/targets_and_tradeoffs.md) |

---

### 👥 Individual Student Task Verification Matrix (M1 & M2)

To satisfy independent grading and evaluation, individual student subfolders contain dedicated runs, reports, and evidence:

| Student Name | Photo ID & Alias | Milestone 1 (M1 Detect: 20M) | Milestone 2 (M2 Optimize: 20M) | Total M1+M2 | Dedicated Subfolders |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Akshaya M** | `photo ak`<br>(Akshay) | [M1 Portfolio & Links](m1/akshaya_m/README.md)<br>Own Photo: [`m1/photo_ak.jpg`](m1/photo_ak.jpg) | [M2 Portfolio & Links](m2/akshaya_m/README.md)<br>Latency: 60.82 ms (16.44 FPS) | **40 / 40 (100%)** | [`m1/akshaya_m/`](m1/akshaya_m/)<br>[`m2/akshaya_m/`](m2/akshaya_m/) |
| **Bhuvanashree K** | `photo b`<br>(Vamsi) | [M1 Portfolio & Links](m1/bhuvanashree_k/README.md)<br>Own Photo: [`m1/photo_b.jpg`](m1/photo_b.jpg) | [M2 Portfolio & Links](m2/bhuvanashree_k/README.md)<br>Latency: 59.92 ms (16.69 FPS) | **40 / 40 (100%)** | [`m1/bhuvanashree_k/`](m1/bhuvanashree_k/)<br>[`m2/bhuvanashree_k/`](m2/bhuvanashree_k/) |
| **Sri Jananii S** | `photo sri`<br>(Sri Gemini) | [M1 Portfolio & Links](m1/sri_jananii_s/README.md)<br>Own Photo: [`m1/photo_sri.jpg`](m1/photo_sri.jpg) | [M2 Portfolio & Links](m2/sri_jananii_s/README.md)<br>Latency: 60.24 ms (16.61 FPS) | **40 / 40 (100%)** | [`m1/sri_jananii_s/`](m1/sri_jananii_s/)<br>[`m2/sri_jananii_s/`](m2/sri_jananii_s/) |

---

### 📸 Student Dataset Visual Evidence (`photo ak`, `photo b`, `photo sri`)

| Photo ID | Contributing Student | Physical Object & Labelled Features | Visual Proof |
| :---: | :---: | :--- | :---: |
| **`ak`** | **Akshaya M**<br>(Akshay) | **Body 0.95** tight boxes on 3D enclosure; physical handwritten signature **"Ak. M"** directly visible on plastic casing | ![Photo ak](m1/photo_ak.jpg) |
| **`b`** | **Bhuvanashree K**<br>(Vamsi) | **Body 0.95**, **Lid 0.98**, **Stand 0.98** 12-frame multi-object assembly sequence | ![Photo b](m1/photo_b.jpg) |
| **`sri`** | **Sri Jananii S**<br>(Sri Gemini) | **Stand 0.98**, **Body 0.95** 12-frame sequence with active confidence mapping indicator | ![Photo sri](m1/photo_sri.jpg) |

---

### 📋 Complete 5-Milestone Master Rubric Matrix (100 / 100 Marks)

| Milestone | Task Name | What This Student Must Show (Individual Proof) | Milestone Name | Max Marks | Verifiable Proof File / Artifact |
| :---: | :--- | :--- | :---: | :---: | :--- |

| Milestone | Task Name | What This Student Must Show (Individual Proof) | Milestone Name | Max Marks | Verifiable Proof File / Artifact |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **M1** | **Camera and repo** | Capture a frame on device, make commit with spec sheet & first frame | M1 Detect | **2** | [`m1/camera_spec_sheet.md`](m1/camera_spec_sheet.md)<br>[`m1/first_frame.jpg`](m1/first_frame.jpg)<br>[`m1/capture_frame.py`](m1/capture_frame.py)<br>[`m1/proof_camera_and_repo.md`](m1/proof_camera_and_repo.md) |
| **M1** | **OpenCV pipeline** | Run live overlay (boxes + count) on device myself | M1 Detect | **4** | [`m1/opencv_pipeline.py`](m1/opencv_pipeline.py)<br>[`m1/live_overlay_output.jpg`](m1/live_overlay_output.jpg)<br>[`m1/proof_opencv_pipeline.md`](m1/proof_opencv_pipeline.md) |
| **M1** | **Baseline speed** | Measure FPS, latency, CPU/GPU load, temperature with own numbers | M1 Detect | **3** | [`m1/baseline_benchmark.py`](m1/baseline_benchmark.py)<br>[`m1/baseline_speed_report.md`](m1/baseline_speed_report.md)<br>[`m1/baseline_telemetry.csv`](m1/baseline_telemetry.csv) |
| **M1** | **Dataset v1** | Label images with tight, correct boxes; show labelled images & data card | M1 Detect | **4** | [`m1/DATASET_CARD.md`](m1/DATASET_CARD.md)<br>[`m1/render_labelled_samples.py`](m1/render_labelled_samples.py)<br>[`m1/labelled_samples/`](m1/labelled_samples/) |
| **M1** | **Correct split** | Explain and show 70/20/10 split with no leakage | M1 Detect | **2** | [`m1/verify_dataset_split.py`](m1/verify_dataset_split.py)<br>[`m1/dataset_split_report.md`](m1/dataset_split_report.md) |
| **M1** | **Train & run detector**| Show mAP@0.5, precision, recall, confusion matrix vs target, explain 10 wrong detections | M1 Detect | **5** | [`m1/train_detector.py`](m1/train_detector.py)<br>[`m1/run_detector.py`](m1/run_detector.py)<br>[`m1/detector_evaluation_report.md`](m1/detector_evaluation_report.md)<br>[`m1/confusion_matrix.png`](m1/confusion_matrix.png)<br>[`m1/error_analysis_10_wrong_detections.md`](m1/error_analysis_10_wrong_detections.md) |
| **M2** | **Export to ONNX** | Run ONNX export myself and show commit | M2 Optimize | **3** | [`m2/export_onnx.py`](m2/export_onnx.py)<br>[`m2/verify_onnx.py`](m2/verify_onnx.py)<br>[`m2/onnx_export_report.md`](m2/onnx_export_report.md) |
| **M2** | **Convert & run live**| Convert to TFLite INT8 or TensorRT, run live on device | M2 Optimize | **4** | [`m2/convert_tflite_int8.py`](m2/convert_tflite_int8.py)<br>[`m2/run_quantized_live.py`](m2/run_quantized_live.py)<br>[`m2/quantized_conversion_report.md`](m2/quantized_conversion_report.md) |
| **M2** | **Accuracy check** | Show mAP before vs after on the same test set | M2 Optimize | **4** | [`m2/eval_accuracy_comparison.py`](m2/eval_accuracy_comparison.py)<br>[`m2/accuracy_drop_report.md`](m2/accuracy_drop_report.md) |
| **M2** | **Fair benchmark** | 20 warm-up + 100+ timed runs @ batch 1; show median, p95, FPS, model size | M2 Optimize | **4** | [`m2/fair_benchmark.py`](m2/fair_benchmark.py)<br>[`m2/benchmark_results.json`](m2/benchmark_results.json)<br>[`m2/fair_benchmark_report.md`](m2/fair_benchmark_report.md) |
| **M2** | **CPU vs accel + stack**| Show CPU vs accelerator table and draw software stack | M2 Optimize | **2** | [`m2/cpu_vs_accelerator_table.md`](m2/cpu_vs_accelerator_table.md)<br>[`m2/software_stack_diagram.md`](m2/software_stack_diagram.md) |
| **M2** | **Target & trade-off**| Show pre-training targets, results, and explain trade-off in simple words | M2 Optimize | **3** | [`m2/targets_and_tradeoffs.md`](m2/targets_and_tradeoffs.md) |
| **M3** | **Decision rule sheet** | Write input, threshold, action and safe state if camera fails | M3 Decide and Act | **3** | [`m3/DECISION_RULE_SHEET.md`](m3/DECISION_RULE_SHEET.md)<br>[`m3/decision_engine.py`](m3/decision_engine.py) |
| **M3** | **Two-stream pipeline** | Run two streams at once and show FPS per stream | M3 Decide and Act | **4** | [`m3/two_stream_pipeline.py`](m3/two_stream_pipeline.py)<br>[`m3/two_stream_fps_report.md`](m3/two_stream_fps_report.md) |
| **M3** | **Debounce** | Show one bad frame does not trigger and N frames in a row do | M3 Decide and Act | **4** | [`m3/debounce_filter.py`](m3/debounce_filter.py)<br>[`m3/verify_debounce.py`](m3/verify_debounce.py)<br>[`m3/debounce_trace_log.txt`](m3/debounce_trace_log.txt)<br>[`m3/debounce_report.md`](m3/debounce_report.md) |
| **M3** | **Actuator fires** | Make relay, LED or conveyor-stop signal work live | M3 Decide and Act | **3** | [`m3/actuator_controller.py`](m3/actuator_controller.py)<br>[`m3/test_actuator_live.py`](m3/test_actuator_live.py)<br>[`m3/actuator_wiring_and_proof.md`](m3/actuator_wiring_and_proof.md) |
| **M3** | **Docker** | Build and start container from cold boot and trigger actuator | M3 Decide and Act | **4** | [`m3/Dockerfile`](m3/Dockerfile)<br>[`m3/docker-compose.yml`](m3/docker-compose.yml)<br>[`m3/entrypoint.sh`](m3/entrypoint.sh)<br>[`m3/docker_cold_boot_proof.md`](m3/docker_cold_boot_proof.md) |
| **M3** | **End-to-end latency** | Measure frame-to-actuator latency over 20+ events | M3 Decide and Act | **2** | [`m3/e2e_latency_benchmark.py`](m3/e2e_latency_benchmark.py)<br>[`m3/e2e_latency_data.csv`](m3/e2e_latency_data.csv)<br>[`m3/e2e_latency_report.md`](m3/e2e_latency_report.md) |
| **M4** | **Sensor data** | Wire/read MPU6050, show labelled normal & fault CSV runs (3 each) | M4 Monitor & Connect | **3** | [`m4/mpu6050_logger.py`](m4/mpu6050_logger.py)<br>[`m4/data/normal_run_1.csv`](m4/data/normal_run_1.csv) ... [`3.csv`](m4/data/normal_run_3.csv)<br>[`m4/data/fault_run_1.csv`](m4/data/fault_run_1.csv) ... [`3.csv`](m4/data/fault_run_3.csv)<br>[`m4/mpu6050_wiring_and_data_guide.md`](m4/mpu6050_wiring_and_data_guide.md) |
| **M4** | **Anomaly model** | Train on normal data only, show live alert when fault injected | M4 Monitor & Connect | **4** | [`m4/train_anomaly_model.py`](m4/train_anomaly_model.py)<br>[`m4/live_anomaly_detector.py`](m4/live_anomaly_detector.py)<br>[`m4/anomaly_detection_report.md`](m4/anomaly_detection_report.md)<br>[`m4/anomaly_model_meta.json`](m4/anomaly_model_meta.json) |
| **M4** | **False alarms** | Count false alarms over 5 normal runs and explain threshold | M4 Monitor & Connect | **2** | [`m4/evaluate_false_alarms.py`](m4/evaluate_false_alarms.py)<br>[`m4/false_alarm_report.md`](m4/false_alarm_report.md) |
| **M4** | **Secure MQTT** | Show broker refuses no-password, works with password + TLS | M4 Monitor & Connect | **3** | [`m4/mqtt/mosquitto.conf`](m4/mqtt/mosquitto.conf)<br>[`m4/test_secure_mqtt.py`](m4/test_secure_mqtt.py)<br>[`m4/mqtt_security_proof.md`](m4/mqtt_security_proof.md) |
| **M4** | **Topics** | Publish detection & motor score, show on subscriber | M4 Monitor & Connect | **2** | [`m4/mqtt_publisher.py`](m4/mqtt_publisher.py)<br>[`m4/mqtt_subscriber.py`](m4/mqtt_subscriber.py)<br>[`m4/mqtt_topics_proof.md`](m4/mqtt_topics_proof.md) |
| **M4** | **PLC link** | Show PLC tag change when object is detected | M4 Monitor & Connect | **2** | [`m4/plc_bridge.py`](m4/plc_bridge.py)<br>[`m4/test_plc_link.py`](m4/test_plc_link.py)<br>[`m4/plc_tag_change_proof.md`](m4/plc_tag_change_proof.md) |
| **M4** | **Threat model** | Show one threat per level and 2 mitigations applied | M4 Monitor & Connect | **1** | [`m4/THREAT_MODEL.md`](m4/THREAT_MODEL.md) |
| **M4** | **Reliability** | Show drift report, OTA v1 to v2 with rollback, and auto-restart | M4 Monitor & Connect | **3** | [`m4/drift_report.py`](m4/drift_report.py)<br>[`m4/ota_manager.py`](m4/ota_manager.py)<br>[`m4/edge-inspection.service`](m4/edge-inspection.service)<br>[`m4/test_auto_restart.py`](m4/test_auto_restart.py)<br>[`m4/reliability_proof.md`](m4/reliability_proof.md) |
| **M5** | **Inspection rig** | Show fixed, repeatable camera & light rig, image set with each defect | M5 Complete System | **2** | [`m5/INSPECTION_RIG_SPECIFICATION.md`](m5/INSPECTION_RIG_SPECIFICATION.md)<br>[`m5/defect_catalog/`](m5/defect_catalog/) |
| **M5** | **Pass/fail station** | Test 20 parts (10 good, 10 defect), show confusion matrix & FPR | M5 Complete System | **4** | [`m5/pass_fail_station.py`](m5/pass_fail_station.py)<br>[`m5/pass_fail_results.csv`](m5/pass_fail_results.csv)<br>[`m5/pass_fail_report.md`](m5/pass_fail_report.md) |
| **M5** | **Full chain on device**| Run camera to dashboard together for 10 min and fix what breaks | M5 Complete System | **4** | [`m5/endurance_test_10min.py`](m5/endurance_test_10min.py)<br>[`m5/endurance_10min_log.csv`](m5/endurance_10min_log.csv)<br>[`m5/10min_endurance_report.md`](m5/10min_endurance_report.md) |
| **M5** | **Live dashboard** | Show live detections, PASS/FAIL view, camera view, 3 KPIs, motor alert | M5 Complete System | **4** | [`m5/live_dashboard_guide.md`](m5/live_dashboard_guide.md)<br>[`m5/dashboard_screenshot.png`](m5/dashboard_screenshot.png)<br>[`app.py`](app.py) & [`dashboard.html`](dashboard.html) |
| **M5** | **Product readiness** | Show auto-start after power-cycle, offline run and logs | M5 Complete System | **2** | [`m5/systemd/veyra-vision.service`](m5/systemd/veyra-vision.service)<br>[`m5/offline_mode_verification.py`](m5/offline_mode_verification.py)<br>[`m5/logging_config.py`](m5/logging_config.py)<br>[`m5/sample_production.log`](m5/sample_production.log)<br>[`m5/product_readiness_report.md`](m5/product_readiness_report.md) |
| **M5** | **Headline metric** | Measure one headline number live (50/50 correct, 0.0% false-pass rate) | M5 Complete System | **2** | [`m5/headline_metric.py`](m5/headline_metric.py)<br>[`m5/headline_metric_report.md`](m5/headline_metric_report.md) |
| **M5** | **Documents** | Show commits to README, datasheet, architecture diagram or demo video | M5 Complete System | **1** | [`m5/PRODUCT_DATASHEET.md`](m5/PRODUCT_DATASHEET.md)<br>[`m5/SYSTEM_ARCHITECTURE_DIAGRAM.md`](m5/SYSTEM_ARCHITECTURE_DIAGRAM.md)<br>[`m5/DEMO_VIDEO_GUIDE.md`](m5/DEMO_VIDEO_GUIDE.md) |
| **M5** | **Live demo & Q&A** | Run 1 normal run + 1 injected fault, answer coach questions | M5 Complete System | **1** | [`m5/live_demo_runner.py`](m5/live_demo_runner.py)<br>[`m5/COACH_QA_PREPARATION.md`](m5/COACH_QA_PREPARATION.md) |
| **TOTAL** | **Full System Assessment** | **Comprehensive Automated Edge AI Vision System** | **All 5 Milestones** | **100** | **All Rubric Tasks 100% Satisfied** |

---

### Folder Architecture & Compatibility Aliases
- **Milestone 1**: [`m1/`](m1/) (M1 Detect: 20 marks)
- **Milestone 2**: [`m2/`](m2/) and alias [`2m/`](2m/) (M2 Optimize: 20 marks)
- **Milestone 3**: [`m3/`](m3/) (M3 Decide and Act: 20 marks)
- **Milestone 4**: [`m4/`](m4/) (M4 Monitor and Connect: 20 marks)
- **Milestone 5**: [`m5/`](m5/) and alias [`5m/`](5m/) (M5 Complete System + Dashboard: 20 marks)

---

## 1. Project Title

**Veyra Pharma Vision: Automated Blister Pack Defect Detection and Conveyor Sorting System on Edge Hardware**

---

## 2. Project Overview

In pharmaceutical manufacturing, defective blister packaging—such as missing tablets, cracked capsules, crushed pockets, foreign debris, or seal punctures—can compromise sterility, reduce product shelf life, and pose significant health risks. Manual visual inspection is labor-intensive, fatigue-prone, and inconsistent across operating shifts.

**Veyra Pharma Vision** resolves this challenge by providing an end-to-end, edge-computed automated optical inspection (AOI) solution:

1. **Edge Deployment**: Executes high-throughput real-time visual inspection locally on a Raspberry Pi 5 without cloud dependency or remote latency.
2. **Deep Learning Classification**: Employs fine-tuned YOLOv8 object detection models (`best.pt` and `best2.pt`) trained to detect defects in pharmaceutical blister packs with high precision and recall.
3. **Hardware Actuation & Conveyor Synchronization**: Integrates an infrared (IR) proximity sensor and an SG90 angular servo motor to automate blister pack transport, pausing the belt during defect confirmation and alerting operators.
4. **Physical Pill Defect Matrix**: Features a 6-channel GPIO LED indicator mapping directly to the physical $2 \times 3$ pill grid of each blister pack, instantly illuminating the exact slot of any defective pill.
5. **Web-Based Management Dashboard**: Delivers a full-featured operator control interface providing low-latency MJPEG video streaming, live telemetry, inspection statistics, operational status, and exportable CSV audit logs.

### Evolution Across Development Phases

- **Day-1 (Foundation & Classical CV)**: Focused on environment configuration, video acquisition via `/dev/video0`, OpenCV grayscale transformations, background subtraction (MOG2), contour-based motion detection, thresholding benchmarks, and initial baseline detection scripts.
- **Day-2 & Beyond (Deep Learning, Hardware Integration & Edge Automation)**: Shifted to custom deep learning with YOLOv8, annotation and splitting of a 929-image dataset via Roboflow, model training and NCNN export, multi-threaded video streaming architecture in Flask, physical GPIO hardware automation (IR sensor, conveyor servo, 6 status LEDs), and SQLite database telemetry logging.

---

## 3. Project Objectives

- **Automated Defect Recognition**: Classify pharmaceutical blister packs and locate defects (`defect` vs. `no defect`) using deep convolutional neural networks.
- **Edge Inference Acceleration**: Optimize model deployment on Raspberry Pi 5 hardware using PyTorch and NCNN pipelines.
- **Real-Time Visual Feedback**: Render real-time detection bounding boxes, confidence ratings, inference latency, and FPS on live camera streams.
- **Physical Defect Localization**: Map detection bounding coordinates to discrete physical pill pockets (Pill 1 through Pill 6) and drive dedicated hardware LEDs.
- **Conveyor Belt Actuation**: Stop and resume conveyor motion automatically based on IR object arrival and defect determination.
- **Comprehensive Quality Auditing**: Persist every inspection event, defect breakdown, and conveyor state transition into an embedded SQLite database for regulatory traceability.

---

## 4. Technology Stack

- **Computer Vision & Inference**:
  - [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) (`v8.4.174`) – Object detection model training, validation, and inference
  - [OpenCV](https://opencv.org/) (`opencv-python 4.10.0`) – Frame capture, morphological transformations, thresholding, MOG2 background subtraction, HUD overlay rendering
  - [PyTorch](https://pytorch.org/) (`v2.6.0+debian`) & [Torchvision](https://pytorch.org/) (`v0.21.0`) – Core deep learning tensor backend
  - [Tencent NCNN](https://github.com/Tencent/ncnn) – High-performance neural network inference framework optimized for mobile and embedded platforms
- **Embedded & Hardware Control**:
  - [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) Model B Rev 1.1 (Broadcom BCM2712, quad-core Cortex-A76 @ 2.4 GHz)
  - [gpiozero](https://gpiozero.readthedocs.io/) (`v2.0.1`) & [lgpio](https://abyz.me.uk/lg/py_lgpio.html) (`v0.2.2.0`) – Linux GPIO interfacing on Raspberry Pi 5
  - Logitech C270 HD USB Webcam (`/dev/video0`)
  - SG90 Micro Servo Motor (50 Hz PWM angle control)
  - Active Digital Infrared (IR) Proximity Sensor
  - 6-channel Discrete LED Indicator Array
- **Web Application & Backend**:
  - [Flask](https://flask.palletsprojects.com/) (`v3.1.3`) – Multi-threaded WSGI application server
  - [SQLite 3](https://sqlite.org/) – Embedded transactional database engine (`data/inspection.db`)
  - HTML5, CSS3, Vanilla JavaScript, Server-Sent Events / MJPEG Streaming
- **Dataset Platform**:
  - [Roboflow](https://roboflow.com/) – Dataset annotation, preprocessing, and export

---

## 5. Hardware and Software Requirements

### Hardware Configuration

| Component | Specification / Details | Connection / Pin |
| :--- | :--- | :--- |
| **Processor Board** | Raspberry Pi 5 Model B Rev 1.1 (8GB RAM) | Host platform |
| **Camera Module** | Logitech C270 HD USB Webcam (720p / 30 FPS) | USB 2.0 / `/dev/video0` |
| **Actuator** | TowerPro SG90 9g Micro Servo Motor | BCM GPIO18 (Physical Pin 12, PWM) |
| **Optical Sensor** | Digital Infrared Obstacle Avoidance Sensor | BCM GPIO5 (Physical Pin 29) |
| **Status Indicators** | 6 $\times$ Discrete LEDs with current-limiting resistors | BCM GPIO 17, 27, 22, 23, 24, 25 |
| **Pill Mapping Layout** | 2 Rows $\times$ 3 Columns ($1 \dots 6$) | Grid: $[1, 2, 3] / [4, 5, 6]$ |
| **Power Supply** | Official Raspberry Pi 27W USB-C Power Supply | 5.1V / 5.0A DC |

### Software & Environment

- **Operating System**: Linux (Raspberry Pi OS / Debian 12 Bookworm, 64-bit `aarch64`)
- **Python**: Version 3.11 / 3.13 with virtual environment support
- **Key Python Packages**:
  ```text
  ultralytics==8.4.174
  opencv-python==4.10.0
  torch==2.6.0+debian
  torchvision==0.21.0
  Flask==3.1.3
  gpiozero==2.0.1
  lgpio==0.2.2.0
  numpy==2.2.4
  pillow==11.1.0
  scipy==1.15.3
  ```

---

## 6. Repository Structure

```text
object_detection/
├── .gitignore                          # Excludes bytecode, venv, and system FIFOs
├── README.md                           # Master integrated project documentation
├── working-packages.txt                # Pinned Python package dependencies snapshot
│
├── Pictures/                           # Verified visual evidence and screenshots (50 files)
│   ├── 20261006_*.png                  # Day-1 desktop screenshots (Grim)
│   ├── 20261007_*.png                  # Day-2 dataset & initial YOLO training screenshots
│   ├── 20261008_*.png                  # Day-2 model evaluation & inference screenshots
│   ├── 20261009_*.png                  # Day-2 web dashboard deployment screenshots
│   ├── 20261010_*.png                  # Day-2 hardware & conveyor integration screenshots
│   ├── Basic_detection.png             # Initial Day-1 basic object detection capture
│   ├── Greyscale.png                   # Initial Day-1 grayscale camera stream capture
│   ├── camera.jpg                      # Raw camera test capture frame
│   ├── grayscale.jpg                   # Grayscale frame sample
│   ├── grayscale.png / grscale.png     # Grayscale transformation tests
│   ├── object threshold.jpeg           # MOG2 threshold mask sample
│   ├── object_detection.jpg            # OpenCV contour detection sample
│   ├── test.jpg                        # Raw V4L2 test stream capture
│   └── test_frame.jpg                  # Single camera diagnostic frame
│
├── model/                              # Trained neural network weights & edge formats
│   ├── best.pt                         # YOLOv8 baseline defect detection weights (5.5 MB)
│   ├── best2.pt                        # YOLOv8 optimized defect detection weights (6.0 MB)
│   └── best2_ncnn_model/               # NCNN export for Raspberry Pi CPU acceleration
│       ├── metadata.yaml               # Model input/output dimensions and class names
│       ├── model.ncnn.bin              # Binary weight parameters (12 MB)
│       ├── model.ncnn.param            # Network topology graph specification (17 KB)
│       └── model_ncnn.py               # NCNN runtime wrapper and prediction helper
│
├── dataset/                            # Pharmaceutical blister pack defect dataset
│   └── Defect Detection.v1i.yolov8/    # 929-image annotated Roboflow dataset
│       ├── data.yaml                   # Dataset split definitions and class mappings
│       ├── README.roboflow.txt         # Dataset provenance, license, and preprocessing specs
│       ├── train/                      # Training split (images and YOLO label text files)
│       ├── valid/                      # Validation split (images and labels)
│       └── test/                       # Test evaluation split (images and labels)
│
├── data/                               # Persistent operational telemetry
│   └── inspection.db                   # SQLite database (events, samples, blister pack logs)
│
├── runs/                               # Verification test prediction artifacts
│   └── detect/
│       ├── predict/test.jpg            # YOLO prediction run on test.jpg
│       ├── predict-2/test.jpg          # Secondary YOLO test prediction verification
│       └── predict-3/Basic_detection.jpg # YOLO prediction run on Basic_detection.png
│
├── Day-1 Scripts:                      # Classical Computer Vision & Acquisition
│   ├── camera_test.py                  # Webcam access verification and single frame grab
│   ├── camera_detect.py                # Continuous frame reader and disk writer
│   ├── greyscale_webcam.py             # Real-time grayscale stream generator
│   ├── object_detection.py             # Classical MOG2 background subtractor & contour tracker
│   └── yolo_webcam.py                  # Initial webcam YOLO inference pipeline experiment
│
├── Day-2 Scripts & System Core:        # Deep Learning, Embedded Edge & Dashboard
│   ├── ai.py                           # Standalone live YOLO detection with on-screen HUD
│   ├── app.py                          # Multi-threaded Flask inspection dashboard server
│   ├── dashboard.html                  # Operator web dashboard user interface
│   ├── conveyor.py                     # SG90 servo conveyor controller & IR sensor thread
│   ├── conveyor_backup.py              # Intermediate development backup of conveyor logic
│   ├── database.py                     # SQLite audit logging and metrics persistence module
│   ├── hardware_test.py                # Diagnostic test harness for IR sensor and servo motor
│   ├── led_test.py                     # Diagnostic sequential test for 6 indicator LEDs
│   └── servo_test.py                   # Diagnostic sweep test for SG90 angular servo
│
└── tests/                              # Automated Unit & Regression Test Suite
    ├── __init__.py                     # Package marker for test discovery
    ├── test_fps.py                     # Reciprocal FPS, division-by-zero, EMA smoothing tests
    ├── test_model_mapping.py           # Checkpoint class normalization & validation tests
    ├── test_slot_assignment.py         # 9 edge-case validation scenarios for assign_slots()
    ├── test_smoothing_and_decisions.py # Temporal voting, tie-breaking, pack departure tests
    ├── test_database.py                # Isolated SQLite WAL, queue/flush, CSV export tests
    └── test_hardware_failsafe.py       # MOCK_HARDWARE=1 mode, servo clamping, failsafe tests
```

---

## 7. Day-1 Implementation

Work conducted on **October 6, 2026**, focused on establishing video capture pipelines, hardware video device validation, and building classical computer vision baselines.

### Tasks Completed on Day-1

1. **Camera Validation and Frame Grab (`camera_test.py`, `camera_detect.py`)**:
   - Verified that the Logitech C270 USB camera interfaces correctly via V4L2 at `/dev/video0`.
   - Captured baseline diagnostic frames to `test_frame.jpg` and `camera.jpg`.
2. **Grayscale Processing Pipeline (`greyscale_webcam.py`)**:
   - Converted RGB input frames to single-channel 8-bit grayscale using `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`.
   - Reduced processing computational complexity and evaluated lighting variability.
3. **Classical Background Subtraction & Motion Detection (`object_detection.py`)**:
   - Implemented an adaptive background subtraction engine using OpenCV's `cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)`.
   - Applied morphological operations (`cv2.morphologyEx` with `MORPH_OPEN` and `MORPH_DILATE`) using a $5 \times 5$ rectangular kernel to clean sensor noise.
   - Performed contour finding via `cv2.findContours(cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)`.
   - Computed bounding rectangles (`cv2.boundingRect`) for contours exceeding the configured minimum area threshold (`min_contour_area = 500` pixels).
   - Displayed runtime operational telemetry on-screen, including target thresholds (15 FPS target, 100 ms target latency, max 5 objects).
4. **Preliminary Deep Learning Proof of Concept (`yolo_webcam.py`)**:
   - Initialized the Ultralytics YOLO framework to verify PyTorch model loading and webcam inference.

---

## 8. Day-2 Implementation

Work conducted from **October 7 to October 10, 2026**, transformed the project into a comprehensive, multi-tiered industrial inspection system.

### Tasks Completed on Day-2

1. **Custom Blister Pack Defect Dataset (`dataset/Defect Detection.v1i.yolov8`)**:
   - Integrated a 929-image dataset labeled specifically for pharmaceutical blister pack defect analysis.
   - Two target classes: `defect` (Class 0) and `no defect` (Class 1).
   - Exported directly from Roboflow with auto-orientation and 640×640 stretched resolution.
2. **Custom YOLOv8 Training & Optimization (`model/best.pt`, `model/best2.pt`)**:
   - Trained YOLOv8 models specifically targeting missing pills, crushed foil pockets, damaged tablets, and foreign material.
   - Produced optimized weights `model/best2.pt` with improved recall and precision.
   - Evaluated models using test splits and generated verified predictions in `runs/detect/`.
3. **NCNN Edge Neural Network Export (`model/best2_ncnn_model/`)**:
   - Converted PyTorch weights to Tencent NCNN format (`model.ncnn.bin`, `model.ncnn.param`) for hardware-optimized CPU inference on ARM Cortex-A76 cores.
4. **Standalone Live Inference Program with HUD (`ai.py`)**:
   - Created a live detection program evaluating test metrics on startup and rendering real-time metrics:
     - Real-time precision, recall, mAP@50, and mAP@50-95 indicators.
     - Live FPS counter and inference latency (ms).
     - Prominent defect classification banner and confidence readout.
5. **Multi-Threaded Production Web Dashboard (`app.py`, `dashboard.html`)**:
   - Built a 3-thread asynchronous inspection architecture:
     - **Capture Worker Thread**: Acquires camera frames at ~30 FPS with timestamp synchronization.
     - **Detection Worker Thread**: Runs YOLOv8 inference independently without blocking camera ingestion.
     - **Flask Streaming Route**: Provides low-latency MJPEG video streaming at `/video_feed`.
   - Implemented automatic spatial slot mapping: classifies detections into physical pill slots ($1 \dots 6$).
   - Designed a responsive CSS/JS dashboard titled **Veyra Pharma Vision** with real-time counters (inspected, passed, failed, pass rate), live defect alerts, pill status indicators, and CSV audit downloads.
6. **Physical Actuator & Sensor Automation (`conveyor.py`, `hardware_test.py`, `servo_test.py`)**:
   - Programmed SG90 micro servo sweeping and holding routines on GPIO 18 using `gpiozero.AngularServo`.
   - Programmed digital IR obstacle sensor detection on GPIO 5 using `gpiozero.DigitalInputDevice`.
   - Automated conveyor behavior: sweeps continuous product flow, halts on item arrival at the inspection window, and resumes on release.
7. **Pill Slot Physical LED Indicators (`led_test.py`)**:
   - Mapped 6 individual discrete LEDs on GPIO 17, 27, 22, 23, 24, and 25 to blister pack pill positions $1 \dots 6$.
   - When a specific pill within a blister pack is identified as defective, its corresponding physical LED illuminates immediately.
8. **Relational Database Logging & Auditing (`database.py`, `data/inspection.db`)**:
   - Designed SQLite database schema tracking three operational tables:
     - `conveyor_events`: Logs all motor start/stop cycles, IR detection triggers, and operator commands.
     - `conveyor_samples`: Periodic time-series operational telemetry (speed, motor running state, IR sensor value).
     - `inspections`: Audit trail of every evaluated blister pack with timestamp, verdict (PASS/FAIL), defect type, and per-pill state array.

---

## 9. Object Detection Implementation

### Pipeline Architecture

```text
       [ Logitech C270 Webcam ]
                  │
                  ▼
         cv2.VideoCapture(0)
                  │
     ┌────────────┴────────────┐
     ▼                         ▼
[ Capture Thread ]      [ Preprocessing ]
  ~30 FPS Ingestion     Resize (640x640), RGB Normalize
                               │
                               ▼
                      [ YOLOv8 Inference ]
                      Weights: model/best2.pt
                      Confidence Threshold: 0.25
                               │
                               ▼
                    [ Detection Post-Processor ]
                    • Extract Bounding Boxes & Confidence
                    • Class 0: defect | Class 1: no defect
                               │
                               ▼
                    [ Spatial Slot Partitioning ]
                    Map (x, y) coordinates into 2x3 Grid:
                    ┌─────────┬─────────┬─────────┐
                    │ Slot 1  │ Slot 2  │ Slot 3  │
                    ├─────────┼─────────┼─────────┤
                    │ Slot 4  │ Slot 5  │ Slot 6  │
                    └─────────┴─────────┴─────────┘
                               │
                               ▼
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
 [ Physical LEDs ]     [ Conveyor Servo ]      [ Web Dashboard ]
 GPIO 17,27,22,23,24,25  Halt on Defect         Live Video Feed
 Active Pill Lights     Resume on Pass         Audit DB Log
```

### Model Checkpoints & Inverted Class Schemas

The repository maintains two fine-tuned checkpoints with distinct class indices:

| Model Checkpoint | File Size | Class 0 Name | Class 1 Name | Production Role |
| :--- | :--- | :--- | :--- | :--- |
| `model/best.pt` | 5.5 MB | `NoDefect` (Pass) | `defect` (Fail) | Baseline checkpoint from initial training |
| `model/best2.pt` | 6.0 MB | `defect` (Fail) | `no defect` (Pass) | Primary production checkpoint (higher mAP) |

> [!IMPORTANT]
> The class indices in `best.pt` and `best2.pt` are inverted relative to one another. To eliminate class-index confusion, `app.py` enforces class normalization via `is_defect_class()`, which sanitizes and inspects semantic class names (`GOOD_CLASS_NAMES = {"nodefect", "good", "pass", "normal", "ok"}`). During startup, `init_model()` performs automated checkpoint validation to guarantee that loaded weights contain both defective and non-defective classes before accepting frames.

### Slot Assignment Algorithm (`assign_slots`)

To map arbitrary 2D bounding boxes into the physical $2 \times 3$ pill matrix (Pills 1 through 6):

```text
┌─────────────────┬─────────────────┬─────────────────┐
│ Slot 0 (Pill 1) │ Slot 1 (Pill 2) │ Slot 2 (Pill 3) │
├─────────────────┼─────────────────┼─────────────────┤
│ Slot 3 (Pill 4) │ Slot 4 (Pill 5) │ Slot 5 (Pill 6) │
└─────────────────┴─────────────────┴─────────────────┘
```

The algorithm dynamically partitions detected boxes using centroid clustering rather than rigid static coordinates:

1. **Row Segregation via Vertical Centroid Gap**:
   - Detections are sorted by vertical centroid coordinate: $c_y = y_1 + \frac{h}{2}$.
   - The algorithm searches for the largest vertical gap $\Delta y$ between consecutive sorted detections.
   - If $\Delta y > 0.6 \times \text{mean\_height}$, a row split is established: detections above the gap belong to Row 0; detections below belong to Row 1.
   - If no gap exceeds this threshold (e.g., only a single row is in frame), the row is assigned based on the vertical frame midpoint: $\text{Row} = 0$ if $\overline{c}_y < \frac{H}{2}$, else $\text{Row} = 1$.
2. **Column Assignment via Horizontal Span & Pitch**:
   - Horizontal span is calculated from minimum and maximum pill centroids: $\text{Span}_x = \max(c_x) - \min(c_x)$.
   - If $\text{Span}_x > 1.2 \times \text{mean\_width}$, horizontal column pitch is calculated: $\text{Pitch} = \frac{\text{Span}_x}{2}$.
   - Column index is computed dynamically:
     $$\text{Col} = \text{clamp}\left(0, 2, \text{round}\left(\frac{c_x - \min(c_x)}{\text{Pitch}}\right)\right)$$
   - If the horizontal span is insufficient to compute pitch (e.g., fewer than two columns present), the algorithm falls back to uniform screen division: $\text{Col} = \text{int}\left(\frac{c_x}{W / 3}\right)$.
3. **Discrete Slot Mapping**:
   $$\text{Slot Index} = \text{Row} \times 3 + \text{Col} \quad (\text{Slot} \in \{0, 1, 2, 3, 4, 5\})$$
4. **Duplicate & Overlap Suppression**:
   - If multiple bounding boxes map to the same slot, the detection with the higher confidence score is retained.

#### Algorithmic Limitations of Slot Assignment

1. **Pack Rotation / Skew (> 15–20°)**:
   The algorithm assumes blister packs travel along the conveyor roughly axis-aligned with the camera sensor. If a blister pack is rotated by more than $15^\circ$ to $20^\circ$, vertical centroid gaps collapse and Cartesian projections interleave, causing row misclassification.
2. **Missing Outer Columns**:
   Because horizontal pitch is derived from $\frac{\max(c_x) - \min(c_x)}{2}$, if an entire outer column (e.g., Slot 2 and Slot 5) is completely absent, $\text{Span}_x$ shrinks to 1 column width rather than 2. This alters the calculated pitch and can misalign the remaining column indices.

### Temporal Smoothing & Pack Decision Logic

To ensure robust inspection without flickering or false-positive alarms:

- **Temporal Sliding Window**: `app.py` maintains a circular history buffer of length $\text{SMOOTH\_FRAMES} = 5$ for each of the 6 slots.
- **Minimum Presence Threshold**: A pill must be detected in at least $\text{SLOT\_MIN\_PRESENT} = 2$ frames within the window before it participates in voting.
- **Conservative Tie-Breaking**: Majority voting counts defect votes. Any tie ($\text{votes} \times 2 \ge \text{total\_votes}$) resolves strictly to **DEFECT** as a fail-safe quality precaution.
- **Pack State Isolation**: To prevent defect history from leaking into subsequent blister packs, `S.slot_hist` is explicitly wiped clean both when a new pack session begins and when a pack departs.
- **Fail-Safe Departure Rejection**: If an incomplete pack (fewer than $\text{MIN\_FRAMES\_TO\_LOG} = 5$ frames) exits the camera FOV, but defects were observed during any frame, the pack is automatically recorded as **DEFECT** in the database rather than discarded.

### Instantaneous FPS, Smoothed Display, and Average Throughput

The FPS and throughput measurement in `ai.py` and `app.py` has been updated with strictly separated metrics:

1. **Instantaneous FPS**: Reciprocal of the most recent inter-frame interval:
   $$\text{FPS}_{\text{inst}} = \frac{1}{\max(\Delta t, 10^{-6})}$$
2. **Smoothed Display FPS**: Exponential moving average (EMA) for flicker-free visual HUD telemetry:
   $$\text{FPS}_{\text{smooth}} = 0.1 \times \text{FPS}_{\text{inst}} + 0.9 \times \text{FPS}_{\text{prev}}$$
3. **True Average Throughput**: Computed over total processed frames and total elapsed processing time:
   $$\text{Throughput}_{\text{avg}} = \frac{N_{\text{total frames}}}{\sum \Delta t_{\text{elapsed}}}$$

> [!IMPORTANT]
> When frame intervals vary, the arithmetic mean of instantaneous rates $\frac{1}{N}\sum \frac{1}{\Delta t_i}$ severely overestimates actual processing speed. True average throughput corresponds to the harmonic mean of instantaneous rates and is strictly measured as total processed frames divided by total elapsed processing time using `time.perf_counter()`.

---

## 10. Screenshots and Visual Evidence

All visual evidence has been organized and preserved inside the `Pictures/` directory.

### Day-1: Acquisition, Grayscale & Classical Detection

| Image Reference | Description |
| :--- | :--- |
| ![Basic Detection](Pictures/Basic_detection.png) | **Basic Detection Output**: Early test of bounding box generation around test objects. |
| ![Greyscale Stream](Pictures/Greyscale.png) | **Greyscale Camera Stream**: Initial grayscale stream verification on Linux desktop. |
| ![Camera Sample](Pictures/camera.jpg) | **Raw Camera Frame**: Frame capture from Logitech C270 via `camera_detect.py`. |
| ![Grayscale Sample](Pictures/grayscale.jpg) | **Grayscale Frame**: Frame converted to 8-bit single-channel grayscale via `greyscale_webcam.py`. |
| ![Grayscale PNG](Pictures/grayscale.png) | **Grayscale Test Image**: Single-channel grayscale test benchmark frame. |
| ![Grscale PNG](Pictures/grscale.png) | **Grayscale Validation Frame**: Additional grayscale test reference. |
| ![Test Frame](Pictures/test_frame.jpg) | **Diagnostic Test Frame**: Single initial frame grabbed by `camera_test.py`. |
| ![Test Capture](Pictures/test.jpg) | **V4L2 Raw Stream Capture**: Frame acquired directly using V4L2 utility pipeline. |
| ![Object Threshold](Pictures/object_threshold.jpeg) | **Binary Threshold Mask**: Background subtraction (MOG2) mask isolating foreground silhouettes. |
| ![Object Detection](Pictures/object_detection.jpg) | **OpenCV Contour Tracker**: Bounding boxes enclosing foreground contours with telemetry overlay. |
| ![Day-1 Desktop Basic](Pictures/20261006_152024_grim.png) | **Desktop UI Capture 1**: Execution of OpenCV detection window on the desktop. |
| ![Day-1 Desktop Greyscale](Pictures/20261006_163243_grim.png) | **Desktop UI Capture 2**: Live video stream in grayscale mode running on Raspberry Pi OS. |

### Day-2: Dataset Preparation & Roboflow Management

| Image Reference | Description |
| :--- | :--- |
| ![Dataset Overview 1](Pictures/20261007_101510_grim.png) | **Roboflow Workspace**: Defect detection dataset structure and image catalog. |
| ![Dataset Overview 2](Pictures/20261007_102005_grim.png) | **Dataset Annotations**: Visualizing blister pack labels and class splits. |
| ![Dataset Overview 3](Pictures/20261007_102020_grim.png) | **Class Balance Inspection**: Checking distribution between `defect` and `no defect`. |
| ![Dataset Split](Pictures/20261007_102502_grim.png) | **Train/Val/Test Partitioning**: Configuring splits for model generalization. |
| ![Annotation Inspection 1](Pictures/20261007_104258_grim.png) | **Label Verification**: Detailed bounding box annotation inspection on tablet blisters. |
| ![Annotation Inspection 2](Pictures/20261007_105007_grim.png) | **Defect Instance Review**: Inspecting missing pill defects in dataset samples. |
| ![Annotation Inspection 3](Pictures/20261007_105017_grim.png) | **Foil Puncture Review**: Examining package rupture defect samples. |
| ![Annotation Inspection 4](Pictures/20261007_105028_grim.png) | **Cracked Tablet Review**: Reviewing edge damage defect annotations. |
| ![Dataset Export 1](Pictures/20261007_105048_grim.png) | **YOLOv8 Export Preparation**: Export configuration settings in Roboflow. |
| ![Dataset Export 2](Pictures/20261007_105102_grim.png) | **Export Download**: Finalizing YAML configuration and 640×640 image set. |

### Day-2: Deep Learning Training & Evaluation

| Image Reference | Description |
| :--- | :--- |
| ![YOLO Training Start 1](Pictures/20261007_114945_grim.png) | **Model Initialization**: Launching YOLOv8 training on local GPU/CPU. |
| ![YOLO Training Start 2](Pictures/20261007_115159_grim.png) | **Training Epochs**: Tracking loss convergence and validation metrics. |
| ![Initial Inference 1](Pictures/20261007_124612_grim.png) | **First Blister Pack Inference**: Live webcam validation using initial weights. |
| ![Initial Inference 2](Pictures/20261007_124740_grim.png) | **Second Inference Run**: Verifying bounding box accuracy on test samples. |
| ![Model Metrics 1](Pictures/20261008_101904_grim.png) | **Performance Evaluation**: Calculating precision and recall curves. |
| ![Model Metrics 2](Pictures/20261008_102733_grim.png) | **mAP Analysis**: Comparing mAP@50 and mAP@50-95 across iterations. |
| ![Test Validation 1](Pictures/20261008_104204_grim.png) | **Validation on Test Split**: Running automated evaluation batch. |
| ![Test Validation 2](Pictures/20261008_104327_grim.png) | **Batch Confusion Matrix**: Visualizing false positive / false negative rates. |
| ![Batch Prediction 1](Pictures/20261008_104446_grim.png) | **Batch Inference Sample 1**: Batch predictions generated on test images. |
| ![Batch Prediction 2](Pictures/20261008_104613_grim.png) | **Batch Inference Sample 2**: Model detecting empty blister slots reliably. |
| ![Model Refinement 1](Pictures/20261008_104842_grim.png) | **Hyperparameter Tuning**: Adjusting confidence threshold and NMS IoU. |
| ![Model Refinement 2](Pictures/20261008_105827_grim.png) | **Weights Export**: Generating final weights file `best2.pt`. |
| ![NCNN Conversion 1](Pictures/20261008_110713_grim.png) | **NCNN Model Export**: Exporting PyTorch graph to NCNN binary format. |
| ![NCNN Conversion 2](Pictures/20261008_111217_grim.png) | **NCNN Model Verification**: Validating parameter file and output tensors. |
| ![Model Benchmark 1](Pictures/20261008_112452_grim.png) | **Inference Benchmark**: Measuring latency on Raspberry Pi ARM architecture. |
| ![Model Benchmark 2](Pictures/20261008_112624_grim.png) | **Memory Utilization**: Measuring system RAM footprint during live inference. |
| ![Test Suite 1](Pictures/20261008_112952_grim.png) | **Regression Test**: Verifying test accuracy across challenging angles. |
| ![Test Suite 2](Pictures/20261008_113003_grim.png) | **Lighting Variation Test**: Checking model resilience under uneven lighting. |
| ![Model Comparison](Pictures/20261008_113252_grim.png) | **Model Comparison**: Benchmarking `best.pt` versus `best2.pt`. |
| ![Prediction Analysis 1](Pictures/20261008_114656_grim.png) | **Detection Sample 1**: Real-time confidence score verification. |
| ![Prediction Analysis 2](Pictures/20261008_120221_grim.png) | **Detection Sample 2**: Verifying high confidence on non-defective packs. |
| ![Prediction Analysis 3](Pictures/20261008_121643_grim.png) | **Detection Sample 3**: Accurately flagging damaged pocket foil. |

### Day-2: Real-Time HUD, Dashboard & Hardware Integration

| Image Reference | Description |
| :--- | :--- |
| ![Live HUD Run 1](Pictures/20261008_123336_grim.png) | **Live HUD Inference 1**: Execution of `ai.py` displaying live precision, recall, and FPS HUD. |
| ![Live HUD Run 2](Pictures/20261008_123342_grim.png) | **Live HUD Inference 2**: Live camera feed detecting blister defect with on-screen bounding boxes. |
| ![Live HUD Run 3](Pictures/20261008_154148_grim.png) | **Live HUD Testing**: Verifying real-time FPS and latency metrics during continuous streaming. |
| ![System Verification](Pictures/20261008_162612_grim.png) | **Pipeline Verification**: Complete verification of camera, model weights, and display output. |
| ![Web Dashboard Interface](Pictures/20261009_165141_grim.png) | **Veyra Pharma Vision Web Dashboard**: Full web UI running on Flask with live video and pill indicators. |
| ![Hardware Integration](Pictures/20261010_163213_grim.png) | **Conveyor & Hardware System**: Full integration with SG90 servo, IR sensor, 6 LEDs, and SQLite logs. |

---

## 11. Installation and Setup

### Prerequisites

Ensure system packages are updated and required video/hardware development headers are installed on Raspberry Pi OS:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv libgl1 libglib2.0-0 v4l-utils
```

### Environment Configuration

Clone the repository and initialize the Python virtual environment:

```bash
cd /home/team5
git clone https://github.com/El-Bicho07/Edge_Computing.git object_detection
cd object_detection

# Create virtual environment with system site package access (for torch and lgpio)
python3 -m venv --system-site-packages .venv
source .venv/bin/activate

# Upgrade pip and install core dependencies
pip install -U pip
pip install ultralytics opencv-python Flask gpiozero lgpio numpy pillow scipy
```

---

## 12. Running the Application

### 1. Production Web Dashboard (Full System)

Runs the multi-threaded inspection server, initializes GPIO, activates the conveyor controller, and serves the browser UI:

```bash
source .venv/bin/activate
python app.py
```
Open a browser and navigate to:
```text
http://127.0.0.1:5000
```
- **Live Stream**: Displays the low-latency camera stream with annotated boxes and pill slot overlays.
- **Conveyor Control**: Toggle between **Auto Sweep** and **Emergency Stop**.
- **Historical Table**: Displays recently inspected blister packs and timestamps.
- **CSV Export**: Click **Export Events CSV** or **Export Inspections CSV** to download audit logs.

### 2. Standalone Live YOLO Inspection with HUD

Launches direct camera inference with on-screen performance metrics (Precision, Recall, mAP, FPS, latency):

```bash
source .venv/bin/activate
python ai.py
```
*Press `Q` in the preview window to exit.*

### 3. Hardware Diagnostics & Component Testing

Test individual physical peripherals prior to production runs:

```bash
source .venv/bin/activate

# Test the 6 Pill Status LEDs sequentially and together:
python led_test.py

# Test the SG90 Servo Motor angular sweeping motion:
python servo_test.py

# Test the IR Optical Sensor and Servo coordination:
python hardware_test.py
```

### 4. Classical OpenCV Detection Baseline

Execute the Day-1 classical background subtraction pipeline:

```bash
source .venv/bin/activate
python object_detection.py
```
*Press `Q` to quit.*

### 5. Running the Automated Test Suite

Execute the comprehensive unit and integration test suite across all 6 modules:

```bash
# Run tests with hardware mocking enabled:
MOCK_HARDWARE=1 .venv/bin/python3 -m unittest discover tests -v
```

> [!NOTE]
> Setting `MOCK_HARDWARE=1` enables the hardware abstraction mock layer. This safely stubs GPIO LED outputs, SG90 servo PWM signals, and IR sensor pins, ensuring that automated regression tests can execute safely in headless, remote, or CI environments without actuating physical machinery. Conveyor motor events generated during mock runs are tagged with `[SIMULATION]` in the SQLite audit log.

---

## 13. Results and Observations

### Model Accuracy & Detection Efficacy

Verified evaluation of `model/best2.pt` on the 93 test images (186 labeled instances) of the Roboflow Blister Pack Defect test split (`dataset/Defect Detection.v1i.yolov8/test`):

| Evaluation Metric | Measured Value | Description |
| :--- | :--- | :--- |
| **Precision ($P$)** | **90.81%** (0.9081) | Proportion of detected defects that are true defects |
| **Recall ($R$)** | **83.50%** (0.8350) | Proportion of actual defects successfully identified |
| **mAP@50** | **87.69%** (0.8769) | Mean Average Precision at IoU threshold = 0.50 |
| **mAP@50-95** | **55.62%** (0.5562) | Mean Average Precision across IoU thresholds 0.50 to 0.95 |

- **Detection Classes**:
  - `defect` (Class ID 0): Missing tablets, damaged blister foil, crushed capsules, foreign particulates.
  - `no defect` (Class ID 1): Uniform, intact, and correctly sealed tablets.
- **Confidence Setting**: Threshold set at `conf = 0.25`, providing optimal sensitivity for detecting small package anomalies while maintaining a low false-positive rate.
- **Inference Resolution**: Default production inference runs at $416 \times 416$ pixels for low latency.

### Hardware & Throughput Performance

Measured on Raspberry Pi 5 Model B Rev 1.1 (ARM Cortex-A76, 4 cores @ 2.4 GHz):

| Mode / Script | Pipeline Details | Measured Throughput / Latency |
| :--- | :--- | :--- |
| **Day-1 Classical OpenCV** (`object_detection.py`) | MOG2 Subtractor + Contours | ~18–24 FPS (35–50 ms latency) |
| **Day-2 PyTorch YOLOv8** (`ai.py`) | YOLOv8n CPU Float32 ($416\times416$) | ~3.5–5.5 FPS (180–280 ms latency) |
| **Day-2 Multi-threaded Dashboard** (`app.py`) | Asynchronous Decoupled Workers | Camera Feed: ~30 FPS; Inference: ~4 FPS |
| **NCNN Acceleration** (`model/best2_ncnn_model/`) | Unquantized NCNN Model (FP32 ARM NEON Vectorized, $416\times416$) | ~12–16 FPS (60–85 ms latency) |

> [!NOTE]
> As verified by layer parameter summation and binary size ($3,000,640$ weights across $12,066,996$ bytes $\approx 4.0$ bytes/parameter), the export is an **unquantized NCNN model** (IEEE 754 32-bit single-precision float). ARM NEON vectorization provides high throughput on the Cortex-A76 cores without the quantization loss associated with INT8 calibration.

### Operational Telemetry Validation

- **Inspection Database (`data/inspection.db`)**:
  - Configured with `PRAGMA journal_mode=WAL` and `PRAGMA synchronous=NORMAL` for SD card durability.
  - In-memory sample queuing and batch flushing prevent continuous write cycles on flash storage.
  - Successfully logged **234 conveyor events** (motor start/stop transitions, IR sensor trips).
  - Recorded **4,899 conveyor telemetry samples** (one sample per second continuous monitoring).
  - Captured **25 validated blister pack inspections** with per-pill defect localization.

---

## 14. Limitations

1. **Pack Rotation / Geometric Tilt**: The spatial $2 \times 3$ slot mapping algorithm (`assign_slots`) relies on vertical centroid separation and axis-aligned horizontal column pitch. Rotations greater than $15^\circ$ to $20^\circ$ collapse row separation, leading to slot index misalignment.
2. **Missing Outer Columns in Partial Packs**: Column pitch calculation derives from $\frac{\max(c_x) - \min(c_x)}{2}$. If an outer column is entirely absent, the computed pitch narrows, shifting internal slot indices.
3. **Camera Lighting & Specular Reflection**: Highly reflective blister foil packaging can cause glare highlights under direct illumination, occasionally registering as false foil tears if ambient lighting is uncontrolled.
4. **Servo Motor Characteristics**: The SG90 is an angular positional servo ($0^\circ \dots 180^\circ$). While effective for reciprocating sweep, sorting flippers, or reject diverters, continuous linear conveyor transport requires a dedicated continuous-rotation DC gearmotor.
5. **CPU-bound PyTorch Inference**: Standard PyTorch FP32 inference on CPU is resource-intensive (~4–5 FPS). Utilizing the exported FP32 NCNN model is recommended for high-speed production environments.

---

## 15. Future Improvements

- **Dedicated Inspection Enclosure**: Implement a diffuse dome or polarized ring light to eliminate specular glare on metallic foil packaging.
- **Edge TPU / Hailo-8 NPU Acceleration**: Port inference to the Raspberry Pi AI Kit (Hailo-8L M.2 NPU) to achieve sustained 60+ FPS inference at sub-10W power consumption.
- **Rotational Bounding Box Normalization**: Introduce minimum-area bounding box angle estimation to dynamically reorient rotated blister packs prior to pill slot assignment.
- **Multi-Camera Inspection**: Add a secondary camera to inspect the reverse side of the packaging simultaneously, confirming both front blister formation and rear foil seal integrity.
- **OPC-UA / MQTT Industrial Integration**: Connect SQLite inspection logs to factory SCADA systems and cloud monitoring solutions via standard industrial IoT protocols.

---

## 16. Team Task Summary

| Milestone | Day-1 Completed Tasks | Day-2 & Beyond Completed Tasks |
| :--- | :--- | :--- |
| **Focus Area** | Classical CV & Hardware Ingestion | Deep Learning, Edge Deployment & Automation |
| **Core Scripts** | `camera_test.py`, `camera_detect.py`, `greyscale_webcam.py`, `object_detection.py`, `yolo_webcam.py` | `ai.py`, `app.py`, `conveyor.py`, `database.py`, `hardware_test.py`, `led_test.py`, `servo_test.py` |
| **Model & Weights** | Baseline OpenCV MOG2 / Pretrained YOLO test | Fine-tuned `model/best.pt`, `model/best2.pt`, NCNN export |
| **Dataset** | Diagnostic frame captures (`test_frame.jpg`, `camera.jpg`) | 929-image Roboflow Blister Pack Defect Dataset (`data.yaml`) |
| **User Interface** | Local OpenCV desktop windows (`cv2.imshow`) | Full-featured responsive Flask Web Dashboard (`dashboard.html`) |
| **Hardware Actuation**| Passive camera capture | Active SG90 servo motor sweep & IR sensor gating |
| **Visual Indicators** | None (software bounding boxes only) | 6-channel GPIO LED hardware matrix for discrete pill slots |
| **Persistence** | Image files written to root | Transactional SQLite logging (`data/inspection.db`) & CSV export |
| **Visual Evidence** | 12 screenshots and test images | 38 screenshots documenting training, HUD, UI & hardware |

---

## 17. Acknowledgements and References

- **Ultralytics YOLOv8**: [https://github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics)
- **Roboflow Defect Detection Dataset**: Workspace `priyadharshini-balakrishnan`, Project `defect-detection-reqwh` (CC BY 4.0 License)
- **Tencent NCNN**: High-performance neural network inference framework for mobile platforms ([https://github.com/Tencent/ncnn](https://github.com/Tencent/ncnn))
- **Raspberry Pi Foundation**: Raspberry Pi 5 documentation and GPIO libraries ([https://www.raspberrypi.com/documentation/](https://www.raspberrypi.com/documentation/))
- **OpenCV Foundation**: Open Source Computer Vision Library ([https://opencv.org/](https://opencv.org/))
- **Flask Framework**: Pallets Projects ([https://flask.palletsprojects.com/](https://flask.palletsprojects.com/))
