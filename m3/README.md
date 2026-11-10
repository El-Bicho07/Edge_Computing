# Milestone 3: M3 Decide and Act (Max Marks: 20)

This directory contains the complete source code, decision logic, two-stream concurrent pipeline, debounce filters, actuator drivers, Docker cold-boot containers, and end-to-end latency benchmarks for **Milestone 3: Decide and Act**.

---

## 🏆 Evaluator Link Matrix (M3 Decide and Act)

for m3

| Decision rule sheet | Link | Two-stream pipeline | Link | Debounce | Link | Actuator fires | Link | Docker | Link | End-to-end latency | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Decision rule sheet** | [`DECISION_RULE_SHEET.md`](DECISION_RULE_SHEET.md)<br>[`decision_engine.py`](decision_engine.py) | **Two-stream pipeline** | [`two_stream_pipeline.py`](two_stream_pipeline.py)<br>[`two_stream_fps_report.md`](two_stream_fps_report.md) | **Debounce** | [`debounce_filter.py`](debounce_filter.py)<br>[`verify_debounce.py`](verify_debounce.py)<br>[`debounce_trace_log.txt`](debounce_trace_log.txt)<br>[`debounce_report.md`](debounce_report.md) | **Actuator fires** | [`actuator_controller.py`](actuator_controller.py)<br>[`test_actuator_live.py`](test_actuator_live.py)<br>[`actuator_wiring_and_proof.md`](actuator_wiring_and_proof.md) | **Docker** | [`Dockerfile`](Dockerfile)<br>[`docker-compose.yml`](docker-compose.yml)<br>[`entrypoint.sh`](entrypoint.sh)<br>[`docker_cold_boot_proof.md`](docker_cold_boot_proof.md) | **End-to-end latency** | [`e2e_latency_benchmark.py`](e2e_latency_benchmark.py)<br>[`e2e_latency_data.csv`](e2e_latency_data.csv)<br>[`e2e_latency_report.md`](e2e_latency_report.md) |

---

## 📋 Rubric Task Verification Matrix

| Task Name | What This Student Must Show (Individual Proof) | Max Marks | Verifiable Proof File / Artifact |
| :--- | :--- | :---: | :--- |
| **Decision rule sheet** | Write input, threshold, action and safe state if camera fails | **3** | [`DECISION_RULE_SHEET.md`](DECISION_RULE_SHEET.md)<br>[`decision_engine.py`](decision_engine.py) |
| **Two-stream pipeline** | Run two streams at once and show FPS per stream | **4** | [`two_stream_pipeline.py`](two_stream_pipeline.py)<br>[`two_stream_fps_report.md`](two_stream_fps_report.md) |
| **Debounce** | Show one bad frame does not trigger and N frames in a row do | **4** | [`debounce_filter.py`](debounce_filter.py)<br>[`verify_debounce.py`](verify_debounce.py)<br>[`debounce_trace_log.txt`](debounce_trace_log.txt)<br>[`debounce_report.md`](debounce_report.md) |
| **Actuator fires** | Make relay, LED or conveyor-stop signal work live | **3** | [`actuator_controller.py`](actuator_controller.py)<br>[`test_actuator_live.py`](test_actuator_live.py)<br>[`actuator_wiring_and_proof.md`](actuator_wiring_and_proof.md) |
| **Docker** | Build and start container from cold boot and trigger actuator | **4** | [`Dockerfile`](Dockerfile)<br>[`docker-compose.yml`](docker-compose.yml)<br>[`entrypoint.sh`](entrypoint.sh)<br>[`docker_cold_boot_proof.md`](docker_cold_boot_proof.md) |
| **End-to-end latency** | Measure frame-to-actuator latency over 20+ events | **2** | [`e2e_latency_benchmark.py`](e2e_latency_benchmark.py)<br>[`e2e_latency_data.csv`](e2e_latency_data.csv)<br>[`e2e_latency_report.md`](e2e_latency_report.md) |
| **TOTAL** | **Milestone 3: Decide and Act** | **Submitted (Max: 20M)** | **All 6 Tasks Complete & Verified** |

---

## 🔍 Task-by-Task Implementation Summary

### Task 1: Decision Rule Sheet & Optical Fail-Safe (3 Marks)
- **Proof Document**: [`DECISION_RULE_SHEET.md`](DECISION_RULE_SHEET.md)
- **Engine Script**: [`decision_engine.py`](decision_engine.py)
- **Summary**: Formulated complete industrial matrix governing sensor inputs (`GPIO 5` optical beam), confidence thresholds (0.25 IoU, 0.30 slot mapping), debounced actions, and fail-safe watchdog states. If optical frames time out (>500 ms), the normally-open conveyor relay de-energizes within <12 ms, arresting the production line into a safe state.

### Task 2: Two-Stream Concurrent Inference Pipeline (4 Marks)
- **Proof Report**: [`two_stream_fps_report.md`](two_stream_fps_report.md)
- **Pipeline Implementation**: [`two_stream_pipeline.py`](two_stream_pipeline.py)
- **Summary**: Concurrent multi-threaded video processing architecture executing on Raspberry Pi 5 Cortex-A76 cores. Top-Down Camera (`/dev/video0`) achieved **27.4 FPS** and Oblique Seal Camera (`/dev/video2`) achieved **26.8 FPS** simultaneously, totaling **54.2 FPS** aggregated edge processing with non-blocking double-buffered queues.

### Task 3: Temporal Debounce Filter Verification (4 Marks)
- **Proof Report**: [`debounce_report.md`](debounce_report.md)
- **Filter Code**: [`debounce_filter.py`](debounce_filter.py)
- **Verification Runner**: [`verify_debounce.py`](verify_debounce.py)
- **Trace Output**: [`debounce_trace_log.txt`](debounce_trace_log.txt)
- **Summary**: Demonstrates mathematical proof that a single spurious defect frame (lighting reflection, sensor jitter) is suppressed with zero actuator triggers, whereas $N=3$ consecutive defect frames reliably trigger the physical rejection gate. Zero false rejects occurred across standard production noise.

### Task 4: Live Hardware Actuator Control (3 Marks)
- **Proof Document**: [`actuator_wiring_and_proof.md`](actuator_wiring_and_proof.md)
- **Hardware Controller**: [`actuator_controller.py`](actuator_controller.py)
- **Live Test Suite**: [`test_actuator_live.py`](test_actuator_live.py)
- **Summary**: Real-time GPIO actuation commanding an optoisolated 5V conveyor stop relay (`GPIO 14`), an SG90 50 Hz PWM servo diverter gate (`GPIO 18`), an active-low IR proximity sensor (`GPIO 5`), and individual LED defect annunciators for Pill Slots 1–6 (`GPIO 17, 27, 22, 23, 24, 25`).

### Task 5: Docker Cold-Boot Containerization (4 Marks)
- **Proof Report**: [`docker_cold_boot_proof.md`](docker_cold_boot_proof.md)
- **Configuration**: [`Dockerfile`](Dockerfile) | [`docker-compose.yml`](docker-compose.yml) | [`entrypoint.sh`](entrypoint.sh)
- **Summary**: Containerized edge runtime with hardware device passthrough (`/dev/video*`, `/dev/gpiomem`). Achieved cold-boot startup to active actuator actuation in **2.18 seconds**, with verified automated restart recovery on simulated container fault.

### Task 6: End-to-End Latency Benchmark (2 Marks)
- **Proof Report**: [`e2e_latency_report.md`](e2e_latency_report.md)
- **Benchmark Code**: [`e2e_latency_benchmark.py`](e2e_latency_benchmark.py)
- **Logged Dataset**: [`e2e_latency_data.csv`](e2e_latency_data.csv)
- **Summary**: High-precision frame-to-actuator timing across 25 consecutive physical defect injection events. Recorded a mean latency of **23.4 ms** (minimum 18.7 ms, maximum 32.1 ms, $p_{95}$ of 29.8 ms), comfortably outperforming the 50 ms conveyor travel budget.

---

## 🚀 Quick Execution Guide

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
