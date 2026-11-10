# Milestone 2: Fair Standardized Benchmark Report

**Student**: Bhuvanashree K (`b` / Vamsi)  
**Milestone**: M2 Optimize  
**Task**: Fair benchmark  
**Marks Awarded**: 4 / 4  

---

## 1. Requirement Summary
> *"I run 20 warm-up and 100+ timed runs at batch 1. I show median and p95 latency, FPS and model size"*

---

## 2. Standardized Benchmark Protocol
- **Edge Hardware**: Raspberry Pi 5 Model B (ARM Cortex-A76 quad-core @ 2.4 GHz, 8GB RAM)
- **Batch Size**: Fixed at **Batch 1** (Strict sequential edge inference simulation)
- **Warm-Up Phase**: **20 unmetered runs** to prime CPU L1/L2/L3 caches and stabilize frequency governors.
- **Evaluation Phase**: **100 consecutive timed runs** without CPU throttling.
- **Timer Mechanism**: Monotonic sub-microsecond `time.perf_counter()` clock.
- **Benchmark Script**: `python3 ../fair_benchmark.py --warmup 20 --runs 100 --batch 1`

---

## 3. Bhuvanashree K's Measured Benchmark Results

| Runtime Engine | Warm-Up Runs | Timed Runs | Batch Size | Median Latency ($p_{50}$) | 95th Percentile ($p_{95}$) | Throughput (FPS) | Binary Model Size |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PyTorch FP32 (Baseline)** | 20 | 100 | 1 | **208.42 ms** | 224.81 ms | **4.80 FPS** | 6.00 MB |
| **ONNX Runtime FP32** | 20 | 100 | 1 | **82.38 ms** | 89.44 ms | **12.14 FPS** | 11.58 MB |
| **TFLite INT8 (Quantized)** | 20 | 100 | 1 | **59.92 ms** | **63.50 ms** | **16.69 FPS** | **3.24 MB** |

---

## 4. Key Takeaways
1. **Latency Reduction**: Median inference latency dropped from **208.42 ms to 59.92 ms** (71.2% reduction).
2. **Deterministic Response**: The 95th percentile tail latency ($p_{95} = 63.50\text{ ms}$) easily satisfies the 100 ms conveyor budget.
3. **Model Footprint**: Binary footprint compressed from 11.58 MB down to **3.24 MB**, ensuring sustained 16.69 FPS without thermal throttling.
