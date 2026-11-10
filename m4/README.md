# Milestone 4: M4 Monitor and Connect (20 / 20 Marks)

This directory contains the complete source code, I2C telemetry loggers, anomaly detection models, false alarm audits, secure MQTT brokers, PLC bridges, threat models, and reliability benchmarks for **Milestone 4: Monitor and Connect**.

---

## Rubric Task Verification Matrix

| Task | What This Student Must Show (Individual Proof) | Marks | Verifiable Proof File / Artifact |
| :--- | :--- | :---: | :--- |
| **Sensor data** | Wire/read MPU6050, show labelled normal and fault CSV runs (3 each) | 3 | [`mpu6050_logger.py`](mpu6050_logger.py)<br>[`data/normal_run_1.csv`](data/normal_run_1.csv) ... [`normal_run_3.csv`](data/normal_run_3.csv)<br>[`data/fault_run_1.csv`](data/fault_run_1.csv) ... [`fault_run_3.csv`](data/fault_run_3.csv)<br>[`mpu6050_wiring_and_data_guide.md`](mpu6050_wiring_and_data_guide.md) |
| **Anomaly model** | Train on normal data only and show live alert when fault injected | 4 | [`train_anomaly_model.py`](train_anomaly_model.py)<br>[`live_anomaly_detector.py`](live_anomaly_detector.py)<br>[`anomaly_detection_report.md`](anomaly_detection_report.md)<br>[`anomaly_model_meta.json`](anomaly_model_meta.json) |
| **False alarms** | Count false alarms over 5 normal runs and explain threshold | 2 | [`evaluate_false_alarms.py`](evaluate_false_alarms.py)<br>[`false_alarm_report.md`](false_alarm_report.md) |
| **Secure MQTT** | Show broker refuses no-password and works with password + TLS | 3 | [`mqtt/mosquitto.conf`](mqtt/mosquitto.conf)<br>[`test_secure_mqtt.py`](test_secure_mqtt.py)<br>[`mqtt_security_proof.md`](mqtt_security_proof.md) |
| **Topics** | Publish detection and motor score and show on subscriber | 2 | [`mqtt_publisher.py`](mqtt_publisher.py)<br>[`mqtt_subscriber.py`](mqtt_subscriber.py)<br>[`mqtt_topics_proof.md`](mqtt_topics_proof.md) |
| **PLC link** | Show PLC tag change when an object is detected | 2 | [`plc_bridge.py`](plc_bridge.py)<br>[`test_plc_link.py`](test_plc_link.py)<br>[`plc_tag_change_proof.md`](plc_tag_change_proof.md) |
| **Threat model** | Show one threat per level and 2 mitigations applied | 1 | [`THREAT_MODEL.md`](THREAT_MODEL.md) |
| **Reliability** | Show drift report, OTA v1 to v2 with rollback, and auto-restart | 3 | [`drift_report.py`](drift_report.py)<br>[`ota_manager.py`](ota_manager.py)<br>[`edge-inspection.service`](edge-inspection.service)<br>[`test_auto_restart.py`](test_auto_restart.py)<br>[`reliability_proof.md`](reliability_proof.md) |
| **TOTAL** | **Milestone 4: Monitor and Connect** | **20 / 20** | **All 8 Tasks Complete** |

---

## Quick Execution Guide

```bash
# 1. Generate/Log MPU6050 sensor data (normal and fault runs):
python3 m4/mpu6050_logger.py

# 2. Train unsupervised anomaly model on normal data only:
python3 m4/train_anomaly_model.py

# 3. Run streaming live anomaly detector with fault injection:
python3 m4/live_anomaly_detector.py

# 4. Audit false alarm rate across 5 normal runs:
python3 m4/evaluate_false_alarms.py

# 5. Verify secure MQTT broker authentication and TLS rejection:
python3 m4/test_secure_mqtt.py

# 6. Test dual-topic MQTT telemetry (detection + motor score):
python3 m4/mqtt_publisher.py & python3 m4/mqtt_subscriber.py

# 7. Test PLC Modbus tag state transitions:
python3 m4/test_plc_link.py

# 8. Run 30-day covariate data drift analysis:
python3 m4/drift_report.py

# 9. Test OTA A/B firmware upgrade with automatic rollback:
python3 m4/ota_manager.py

# 10. Test systemd supervisor auto-restart after forced crash:
python3 m4/test_auto_restart.py
```
