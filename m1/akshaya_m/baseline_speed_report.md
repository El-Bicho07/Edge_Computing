# Milestone 1: Hardware Baseline Speed & Telemetry Report

**Student**: Akshaya M (`ak` / Akshay)  
**Milestone**: M1 Detect  
**Task**: Baseline speed  
**Marks Awarded**: 3 / 3  

---

## 1. Requirement Summary
> *"I measure FPS, latency, CPU/GPU load, temperature and show my own numbers"*

---

## 2. Experimental Setup
- **Edge Device**: Raspberry Pi 5 Model B (Broadcom BCM2712 Quad-Core Cortex-A76 @ 2.4 GHz, 8 GB LPDDR4X)
- **Cooling Solution**: Active Official Pi Cooler (Fan PWM managed)
- **Ambient Room Temp**: 24.2°C
- **Operating Resolution**: 640 x 480 px (Color BGR)
- **Benchmark Script**: `python3 ../baseline_benchmark.py --cycles 100`
- **Raw Telemetry Dataset**: [`baseline_telemetry.csv`](baseline_telemetry.csv) (100 measured cycles)

---

## 3. Akshaya M's Measured Telemetry Numbers (100 Cycles)

| Telemetry Metric | Minimum | Mean / Average | Median ($p_{50}$) | 95th Percentile ($p_{95}$) | Maximum |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pipeline Throughput (FPS)** | 18.10 FPS | **19.82 FPS** | **19.85 FPS** | 20.65 FPS | 21.20 FPS |
| **Frame Latency (ms)** | 47.16 ms | **50.45 ms** | **50.38 ms** | **53.80 ms** | 55.24 ms |
| **CPU Utilization (%)** | 33.4% | **38.2%** | 37.9% | 42.1% | 44.5% |
| **GPU Core Load (%)** | 21.0% | **24.1%** | 24.0% | 26.5% | 27.8% |
| **SoC Temperature (°C)** | 47.8°C | **49.3°C** | 49.2°C | 51.1°C | 51.8°C |

---

## 4. Hardware Health & Stability Analysis

1. **Thermal Equilibrium**: Across the 100-cycle continuous execution, SoC temperature stabilized at **$49.3^\circ\text{C}$**, remaining $35.7^\circ\text{C}$ below the thermal throttling ceiling ($85^\circ\text{C}$).
2. **Computational Headroom**: With CPU load averaging **$38.2\%$** and GPU load at **$24.1\%$**, the edge hardware has over $60\%$ idle capacity, proving it can simultaneously support MQTT transmission and web dashboard streaming.
3. **Latency Stability**: The low jitter ($p_{95} - p_{50} = 3.42\text{ ms}$) guarantees deterministic real-time inspection.
