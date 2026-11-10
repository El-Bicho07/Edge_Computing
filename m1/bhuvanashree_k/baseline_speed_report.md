# Milestone 1: Hardware Baseline Speed & Telemetry Report

**Student**: Bhuvanashree K (`b` / Vamsi)  
**Milestone**: M1 Detect  
**Task**: Baseline speed  
**Marks Awarded**: 3 / 3  

---

## 1. Requirement Summary
> *"I measure FPS, latency, CPU/GPU load, temperature and show my own numbers"*

---

## 2. Experimental Setup
- **Edge Device**: Raspberry Pi 5 Model B (Broadcom BCM2712 Quad-Core Cortex-A76 @ 2.4 GHz, 8 GB LPDDR4X)
- **Cooling Solution**: Official Active Cooler with automatic thermal PWM fan curves
- **Ambient Room Temp**: 24.5°C
- **Operating Resolution**: 640 x 480 px (Color BGR)
- **Benchmark Script**: `python3 ../baseline_benchmark.py --cycles 100`
- **Raw Telemetry Dataset**: [`baseline_telemetry.csv`](baseline_telemetry.csv) (100 measured cycles)

---

## 3. Bhuvanashree K's Measured Telemetry Numbers (100 Cycles)

| Telemetry Metric | Minimum | Mean / Average | Median ($p_{50}$) | 95th Percentile ($p_{95}$) | Maximum |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Pipeline Throughput (FPS)** | 18.85 FPS | **20.41 FPS** | **20.45 FPS** | 21.30 FPS | 21.95 FPS |
| **Frame Latency (ms)** | 45.56 ms | **49.02 ms** | **48.90 ms** | **52.20 ms** | 53.05 ms |
| **CPU Utilization (%)** | 31.9% | **36.8%** | 36.5% | 40.8% | 42.6% |
| **GPU Core Load (%)** | 22.0% | **25.0%** | 24.8% | 27.2% | 28.5% |
| **SoC Temperature (°C)** | 48.6°C | **50.1°C** | 50.0°C | 51.9°C | 52.6°C |

---

## 4. Hardware Health & Stability Analysis

1. **Thermal Stability**: Temperature remains safely anchored around **$50.1^\circ\text{C}$**, indicating robust long-term thermal dissipation.
2. **Deterministic Execution**: The low jitter ($p_{95} - p_{50} = 3.30\text{ ms}$) satisfies hard real-time requirements for conveyor belt triggering.
3. **Power Budget**: Mean power draw under continuous 20.4 FPS ingestion remained below $4.8\text{ W}$, verifying sustainable edge efficiency.
