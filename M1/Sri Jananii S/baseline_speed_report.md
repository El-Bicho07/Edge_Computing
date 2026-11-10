# Milestone 1: Hardware Baseline Speed & Telemetry Report

**Student**: Sri Jananii S (`sri` / Sri Jananii S)  
**Milestone**: M1 Detect  
**Task**: Baseline speed  
**Rubric Weight**: 3 Marks  

---

## 1. Requirement Summary
> *"I measure FPS, latency, CPU/GPU load, temperature and show my own numbers"*

---

## 2. Experimental Setup
- **Edge Device**: Raspberry Pi 5 Model B (Broadcom BCM2712 Quad-Core Cortex-A76 @ 2.4 GHz, 8 GB LPDDR4X)
- **Cooling Solution**: Official Active Cooler with automatic thermal PWM fan curves
- **Ambient Room Temp**: 24.0°C
- **Operating Resolution**: 640 x 480 px (Color BGR)
- **Benchmark Script**: `python3 ../baseline_benchmark.py --cycles 100`
- **Raw Telemetry Dataset**: [`baseline_telemetry.csv`](baseline_telemetry.csv) (100 measured cycles)

---

## 3. Sri Jananii S's Measured Telemetry Numbers (100 Cycles)

| Telemetry Metric | Minimum | Mean / Average | Median ($p_{50}$) | 95th Percentile ($p_{95}$) | Maximum |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pipeline Throughput (FPS)** | 19.45 FPS | **21.08 FPS** | **21.12 FPS** | 22.05 FPS | 22.60 FPS |
| **Frame Latency (ms)** | 44.25 ms | **47.44 ms** | **47.35 ms** | **50.50 ms** | 51.41 ms |
| **CPU Utilization (%)** | 34.8% | **39.5%** | 39.2% | 43.4% | 45.1% |
| **GPU Core Load (%)** | 21.2% | **23.8%** | 23.6% | 25.8% | 26.9% |
| **SoC Temperature (°C)** | 47.2°C | **48.6°C** | 48.5°C | 50.4°C | 51.0°C |

---

## 4. Hardware Health & Stability Analysis

1. **High Ingestion Throughput**: Average throughput achieved **$21.08\text{ FPS}$**, comfortably exceeding the line inspection minimum ($15\text{ FPS}$).
2. **Thermal Resilience**: Temperature never breached $51.0^\circ\text{C}$, confirming sufficient airflow and thermal headroom.
3. **Execution Predictability**: Standard deviation in latency remained under $1.5\text{ ms}$, ensuring synchronous operation with the SG90 servo conveyor trigger.
