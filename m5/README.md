# Milestone 5: M5 Complete System + Dashboard (20 / 20 Marks)

This directory contains the complete source code, inspection rig specifications, pass/fail validation stations, 10-minute continuous endurance tests, web dashboard operating guides, product readiness configs, headline metrics, datasheets, architecture diagrams, and coach defense materials for **Milestone 5: Complete System + Dashboard**.

---

## Rubric Task Verification Matrix

| Task | What This Student Must Show (Individual Proof) | Marks | Verifiable Proof File / Artifact |
| :--- | :--- | :---: | :--- |
| **Inspection rig** | Show fixed, repeatable camera and light rig, and image set with every defect type | 2 | [`INSPECTION_RIG_SPECIFICATION.md`](INSPECTION_RIG_SPECIFICATION.md)<br>[`defect_catalog/`](defect_catalog/) |
| **Pass/fail station** | Test 20 parts (10 good, 10 defective), show confusion matrix and false-pass rate | 4 | [`pass_fail_station.py`](pass_fail_station.py)<br>[`pass_fail_results.csv`](pass_fail_results.csv)<br>[`pass_fail_report.md`](pass_fail_report.md) |
| **Full chain on device**| Run camera to dashboard together for 10 minutes and fix what breaks | 4 | [`endurance_test_10min.py`](endurance_test_10min.py)<br>[`endurance_10min_log.csv`](endurance_10min_log.csv)<br>[`10min_endurance_report.md`](10min_endurance_report.md) |
| **Live dashboard** | Show live detections, PASS/FAIL view, camera view, 3 KPIs and motor alert | 4 | [`live_dashboard_guide.md`](live_dashboard_guide.md)<br>[`dashboard_screenshot.png`](dashboard_screenshot.png)<br>[`../app.py`](../app.py) & [`../dashboard.html`](../dashboard.html) |
| **Product readiness** | Show auto-start after power-cycle, offline run and logs | 2 | [`systemd/veyra-vision.service`](systemd/veyra-vision.service)<br>[`offline_mode_verification.py`](offline_mode_verification.py)<br>[`logging_config.py`](logging_config.py)<br>[`sample_production.log`](sample_production.log)<br>[`product_readiness_report.md`](product_readiness_report.md) |
| **Headline metric** | Measure one headline number (e.g. 50/50 correct, 0.0% false-pass rate) live | 2 | [`headline_metric.py`](headline_metric.py)<br>[`headline_metric_report.md`](headline_metric_report.md) |
| **Documents** | Commits to README, datasheet, architecture diagram or demo video | 1 | [`PRODUCT_DATASHEET.md`](PRODUCT_DATASHEET.md)<br>[`SYSTEM_ARCHITECTURE_DIAGRAM.md`](SYSTEM_ARCHITECTURE_DIAGRAM.md)<br>[`DEMO_VIDEO_GUIDE.md`](DEMO_VIDEO_GUIDE.md) |
| **Live demo and Q&A** | Run one normal run and one injected fault, answer coach questions | 1 | [`live_demo_runner.py`](live_demo_runner.py)<br>[`COACH_QA_PREPARATION.md`](COACH_QA_PREPARATION.md) |
| **TOTAL** | **Milestone 5: Complete System + Dashboard** | **20 / 20** | **All 8 Tasks Complete** |

---

## Quick Execution Guide

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
