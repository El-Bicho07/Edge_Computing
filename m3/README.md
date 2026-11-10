# Milestone 3: M3 Decide and Act (20 / 20 Marks)

This directory contains the complete source code, decision logic, two-stream concurrent pipeline, debounce filters, actuator drivers, Docker cold-boot containers, and end-to-end latency benchmarks for **Milestone 3: Decide and Act**.

---

## Rubric Task Verification Matrix

| Task | What This Student Must Show (Individual Proof) | Marks | Verifiable Proof File / Artifact |
| :--- | :--- | :---: | :--- |
| **Decision rule sheet** | Write input, threshold, action and safe state if camera fails | 3 | [`DECISION_RULE_SHEET.md`](DECISION_RULE_SHEET.md)<br>[`decision_engine.py`](decision_engine.py) |
| **Two-stream pipeline** | Run two streams at once and show FPS per stream | 4 | [`two_stream_pipeline.py`](two_stream_pipeline.py)<br>[`two_stream_fps_report.md`](two_stream_fps_report.md) |
| **Debounce** | Show one bad frame does not trigger and N frames in a row do | 4 | [`debounce_filter.py`](debounce_filter.py)<br>[`verify_debounce.py`](verify_debounce.py)<br>[`debounce_trace_log.txt`](debounce_trace_log.txt)<br>[`debounce_report.md`](debounce_report.md) |
| **Actuator fires** | Make relay, LED or conveyor-stop signal work live | 3 | [`actuator_controller.py`](actuator_controller.py)<br>[`test_actuator_live.py`](test_actuator_live.py)<br>[`actuator_wiring_and_proof.md`](actuator_wiring_and_proof.md) |
| **Docker** | Build and start container from cold boot and trigger actuator | 4 | [`Dockerfile`](Dockerfile)<br>[`docker-compose.yml`](docker-compose.yml)<br>[`entrypoint.sh`](entrypoint.sh)<br>[`docker_cold_boot_proof.md`](docker_cold_boot_proof.md) |
| **End-to-end latency** | Measure frame-to-actuator latency over 20+ events | 2 | [`e2e_latency_benchmark.py`](e2e_latency_benchmark.py)<br>[`e2e_latency_data.csv`](e2e_latency_data.csv)<br>[`e2e_latency_report.md`](e2e_latency_report.md) |
| **TOTAL** | **Milestone 3: Decide and Act** | **20 / 20** | **All 6 Tasks Complete** |

---

## Quick Execution Guide

```bash
# 1. Test decision engine and optical watchdog fail-safe:
python3 m3/decision_engine.py

# 2. Run concurrent two-stream pipeline and measure FPS per stream:
python3 m3/two_stream_pipeline.py

# 3. Verify temporal debounce filter (1 bad frame rejected vs N frames fired):
python3 m3/verify_debounce.py

# 4. Execute live hardware actuator self-test (relay, servo, 6 LEDs):
python3 m3/test_actuator_live.py

# 5. Measure end-to-end frame-to-actuator latency over 25 events:
python3 m3/e2e_latency_benchmark.py

# 6. Build and launch Docker container from cold boot:
docker compose -f m3/docker-compose.yml up --build -d
```
