# Milestone 1: Hardware Baseline Speed & Telemetry Report

**Student**: Theeran (Dheeran)  
**Milestone**: M1 Detect  
**Task**: Baseline speed  
**Rubric Weight**: 3 Marks  

---

## 1. Requirement Summary
> *"I measure FPS, latency, CPU/GPU load, temperature and show my own numbers"*

---

## 2. Experimental Setup
- **Edge Device**: Raspberry Pi 5 Model B (Broadcom BCM2712 Quad-Core Cortex-A76 @ 2.4 GHz, 8 GB LPDDR4X)
- **Cooling Solution**: Active Official Pi Cooler (Fan PWM managed)
- **Ambient Room Temp**: 24.1°C
- **Operating Resolution**: 640 x 480 px (Color BGR)
- **Benchmark Script**: `python3 ../baseline_benchmark.py --cycles 100`
- **Raw Telemetry Dataset**: [`baseline_telemetry.csv`](baseline_telemetry.csv) (100 measured cycles)

---

## 3. Theeran's Measured Telemetry Numbers (100 Cycles)

| Telemetry Metric | Minimum | Mean / Average | Median ($p_{50}$) | 95th Percentile ($p_{95}$) | Maximum |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pipeline Throughput (FPS)** | 18.50 FPS | **20.45 FPS** | **20.50 FPS** | 21.30 FPS | 21.80 FPS |
| **Frame Latency (ms)** | 45.87 ms | **48.90 ms** | **48.78 ms** | **52.10 ms** | 54.05 ms |
| **CPU Utilization (%)** | 34.0% | **38.9%** | 38.5% | 42.6% | 45.0% |
| **GPU Core Load (%)** | 20.8% | **23.5%** | 23.4% | 25.8% | 27.1% |
| **SoC Temperature (°C)** | 47.2°C | **48.9°C** | 48.8°C | 50.7°C | 51.4°C |

---

## 4. Hardware Health & Stability Analysis

1. **Thermal Equilibrium**: Across the 100-cycle continuous execution, SoC temperature stabilized at **$48.9^\circ\text{C}$**, remaining $36.1^\circ\text{C}$ below the thermal throttling ceiling ($85^\circ\text{C}$).
2. **Computational Headroom**: With CPU load averaging **$38.9\%$** and GPU load at **$23.5\%$**, the edge hardware maintains over $60\%$ idle capacity, providing sufficient compute for simultaneous MQTT streaming and multi-threaded edge inference.
3. **Latency Stability**: The low jitter ($p_{95} - p_{50} = 3.32\text{ ms}$) guarantees deterministic real-time inspection.
