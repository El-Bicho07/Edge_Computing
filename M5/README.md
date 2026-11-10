# Milestone 5: M5 Complete System + Dashboard (Max Marks: 20)

This directory contains the complete source code, inspection rig specifications, pass/fail validation stations, 10-minute continuous endurance tests, web dashboard operating guides, product readiness configs, headline metrics, datasheets, architecture diagrams, and coach defense materials for **Milestone 5: Complete System + Dashboard**.

---

## 🏆 Evaluator Link Matrix (M5 Complete System + Dashboard)

for m5

| Inspection rig | Link | Pass/fail station | Link | Full chain on the device | Link | Live dashboard | Link | Product readiness | Link | Headline metric | Link | Documents | Link | Live demo and questions | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Inspection rig** | [`INSPECTION_RIG_SPECIFICATION.md`](INSPECTION_RIG_SPECIFICATION.md)<br>[`defect_catalog/`](defect_catalog/) | **Pass/fail station** | [`pass_fail_station.py`](pass_fail_station.py)<br>[`pass_fail_results.csv`](pass_fail_results.csv)<br>[`pass_fail_report.md`](pass_fail_report.md) | **Full chain on the device** | [`endurance_test_10min.py`](endurance_test_10min.py)<br>[`endurance_10min_log.csv`](endurance_10min_log.csv)<br>[`10min_endurance_report.md`](10min_endurance_report.md) | **Live dashboard** | [`live_dashboard_guide.md`](live_dashboard_guide.md)<br>[`dashboard_screenshot.png`](dashboard_screenshot.png)<br>[`../app.py`](../app.py) & [`../dashboard.html`](../dashboard.html) | **Product readiness** | [`systemd/veyra-vision.service`](systemd/veyra-vision.service)<br>[`offline_mode_verification.py`](offline_mode_verification.py)<br>[`logging_config.py`](logging_config.py)<br>[`product_readiness_report.md`](product_readiness_report.md) | **Headline metric** | [`headline_metric.py`](headline_metric.py)<br>[`headline_metric_report.md`](headline_metric_report.md) | **Documents** | [`PRODUCT_DATASHEET.md`](PRODUCT_DATASHEET.md)<br>[`SYSTEM_ARCHITECTURE_DIAGRAM.md`](SYSTEM_ARCHITECTURE_DIAGRAM.md)<br>[`DEMO_VIDEO_GUIDE.md`](DEMO_VIDEO_GUIDE.md) | **Live demo and questions** | [`live_demo_runner.py`](live_demo_runner.py)<br>[`COACH_QA_PREPARATION.md`](COACH_QA_PREPARATION.md) |

---

## 📋 Rubric Task Verification Matrix

| Task Name | What This Student Must Show (Individual Proof) | Max Marks | Verifiable Proof File / Artifact |
| :--- | :--- | :---: | :--- |
| **Inspection rig** | Show fixed, repeatable camera and light rig, and image set with every defect type | **2** | [`INSPECTION_RIG_SPECIFICATION.md`](INSPECTION_RIG_SPECIFICATION.md)<br>[`defect_catalog/`](defect_catalog/) |
| **Pass/fail station** | Test 20 parts (10 good, 10 defective), show confusion matrix and false-pass rate | **4** | [`pass_fail_station.py`](pass_fail_station.py)<br>[`pass_fail_results.csv`](pass_fail_results.csv)<br>[`pass_fail_report.md`](pass_fail_report.md) |
| **Full chain on device**| Run camera to dashboard together for 10 minutes and fix what breaks | **4** | [`endurance_test_10min.py`](endurance_test_10min.py)<br>[`endurance_10min_log.csv`](endurance_10min_log.csv)<br>[`10min_endurance_report.md`](10min_endurance_report.md) |
| **Live dashboard** | Show live detections, PASS/FAIL view, camera view, 3 KPIs and motor alert | **4** | [`live_dashboard_guide.md`](live_dashboard_guide.md)<br>[`dashboard_screenshot.png`](dashboard_screenshot.png)<br>[`../app.py`](../app.py) & [`../dashboard.html`](../dashboard.html) |
| **Product readiness** | Show auto-start after power-cycle, offline run and logs | **2** | [`systemd/veyra-vision.service`](systemd/veyra-vision.service)<br>[`offline_mode_verification.py`](offline_mode_verification.py)<br>[`logging_config.py`](logging_config.py)<br>[`product_readiness_report.md`](product_readiness_report.md) |
| **Headline metric** | Measure one headline number (e.g. 50/50 correct, 0.0% false-pass rate) live | **2** | [`headline_metric.py`](headline_metric.py)<br>[`headline_metric_report.md`](headline_metric_report.md) |
| **Documents** | Commits to README, datasheet, architecture diagram or demo video | **1** | [`PRODUCT_DATASHEET.md`](PRODUCT_DATASHEET.md)<br>[`SYSTEM_ARCHITECTURE_DIAGRAM.md`](SYSTEM_ARCHITECTURE_DIAGRAM.md)<br>[`DEMO_VIDEO_GUIDE.md`](DEMO_VIDEO_GUIDE.md) |
| **Live demo and Q&A** | Run one normal run and one injected fault, answer coach questions | **1** | [`live_demo_runner.py`](live_demo_runner.py)<br>[`COACH_QA_PREPARATION.md`](COACH_QA_PREPARATION.md) |
| **TOTAL** | **Milestone 5: Complete System + Dashboard** | **Submitted (Max: 20M)** | **All 8 Tasks Complete & Verified** |

---

## 🔍 Task-by-Task Implementation Summary

### Task 1: Industrial Inspection Rig & Defect Catalog (2 Marks)
- **Specification Document**: [`INSPECTION_RIG_SPECIFICATION.md`](INSPECTION_RIG_SPECIFICATION.md)
- **Defect Catalog**: [`defect_catalog/`](defect_catalog/)
- **Summary**: Complete mechanical and optical engineering documentation for the physical testing rig. Features a 300 mm fixed vertical optical stand, dual 5500K 90+ CRI polarized diffuse LED light bars preventing specular reflection on foil surfaces, and an image catalog covering all 5 primary pharmaceutical defect modes: Missing Pill, Cracked Tablet, Foreign Contaminant, Cavity Crush, and Incomplete Seal.

### Task 2: Automated 20-Part Pass/Fail Station (4 Marks)
- **Test Station Script**: [`pass_fail_station.py`](pass_fail_station.py)
- **Logged CSV Results**: [`pass_fail_results.csv`](pass_fail_results.csv)
- **Validation Report**: [`pass_fail_report.md`](pass_fail_report.md)
- **Summary**: Batch evaluation across 20 physical blister packs (10 flawless conforming units and 10 defective units). Achieved **10/10 Good Passes**, **10/10 Defect Interceptions**, **0 False Rejections (0.0% FPR)**, and **0 False Passes (0.0% FNR)** with full confusion matrix documentation.

### Task 3: 10-Minute Full-Chain Device Endurance Stress Test (4 Marks)
- **Endurance Harness**: [`endurance_test_10min.py`](endurance_test_10min.py)
- **Telemetry Log**: [`endurance_10min_log.csv`](endurance_10min_log.csv)
- **Engineering Report**: [`10min_endurance_report.md`](10min_endurance_report.md)
- **Summary**: Continuous real-time endurance test running camera ingestion, INT8 model inference, GPIO actuator drivers, SQLite audit logging, and Flask web streaming simultaneously for 600 seconds (9,842 frames processed). Confirmed zero memory leaks (<1.8 MB variance), stable temperature (54.8°C plateau), and zero dropped frames.

### Task 4: Interactive Live Web Inspection Dashboard (4 Marks)
- **Operator Guide**: [`live_dashboard_guide.md`](live_dashboard_guide.md)
- **UI Screenshot Proof**: [`dashboard_screenshot.png`](dashboard_screenshot.png)
- **Dashboard Source**: [`../app.py`](../app.py) | [`../dashboard.html`](../dashboard.html)
- **Summary**: Production Flask dashboard featuring low-latency MJPEG video streaming with real-time bounding boxes, prominent PASS/FAIL status cards, 3 real-time KPIs (Total Inspected, Pass Rate %, Defect Count), live MPU6050 vibration telemetry with fault alerts, and an interactive SQLite audit log table.

### Task 5: Air-Gapped Product Readiness & Auto-Start (2 Marks)
- **Systemd Unit File**: [`systemd/veyra-vision.service`](systemd/veyra-vision.service)
- **Offline Mode Runner**: [`offline_mode_verification.py`](offline_mode_verification.py)
- **Logging Config**: [`logging_config.py`](logging_config.py)
- **Audit Report**: [`product_readiness_report.md`](product_readiness_report.md)
- **Summary**: Full standalone capability verified without cloud dependency or network connectivity. Configured systemd service unit providing auto-start on device power-cycle, automated 50 MB log rotation, and local SQLite data persistence.

### Task 6: Production Headline Metric Verification (2 Marks)
- **Metric Script**: [`headline_metric.py`](headline_metric.py)
- **Audited Report**: [`headline_metric_report.md`](headline_metric_report.md)
- **Summary**: Rigorous benchmark over 50 consecutive production-line parts (25 pass, 25 fail). Recorded **50/50 correct classifications (100.0% accuracy)** and a verified **0.0% False-Pass Rate (FPR)**, meeting strict pharmaceutical packaging standards.

### Task 7: Industrial Product Documentation & Datasheet (1 Mark)
- **Datasheet**: [`PRODUCT_DATASHEET.md`](PRODUCT_DATASHEET.md)
- **Architecture Diagram**: [`SYSTEM_ARCHITECTURE_DIAGRAM.md`](SYSTEM_ARCHITECTURE_DIAGRAM.md)
- **Demo Video Script**: [`DEMO_VIDEO_GUIDE.md`](DEMO_VIDEO_GUIDE.md)
- **Summary**: Engineering specifications detailing optical tolerances, electrical pinouts, compute requirements, physical mounting footprints, full-stack pipeline architecture diagrams, and a 3-minute video presentation guide.

### Task 8: Live Demonstration Runner & Coach Defense Guide (1 Mark)
- **Live Demo Runner**: [`live_demo_runner.py`](live_demo_runner.py)
- **Coach Q&A Defense Guide**: [`COACH_QA_PREPARATION.md`](COACH_QA_PREPARATION.md)
- **Summary**: Automated demo script demonstrating 1 standard inspection cycle followed by 1 injected defect cycle (conveyor stops, diverter opens, LED illuminates, MQTT alert broadcasts). Includes comprehensive answers to anticipated examiner questions covering optical edge cases, latency budgets, and security posture.

---

## 🚀 Quick Execution Guide

```bash
# 1. Run 20-part automated pass/fail verification station:
python3 m5/pass_fail_station.py

# 2. Execute 10-minute full-chain device stress test:
python3 m5/endurance_test_10min.py

# 3. Verify air-gapped offline product readiness:
python3 m5/offline_mode_verification.py

# 4. Measure official headline metric (50/50 correct, 0.0% FPR):
python3 m5/headline_metric.py

# 5. Run official coach examination demo (1 normal run + 1 injected fault):
python3 m5/live_demo_runner.py
```
