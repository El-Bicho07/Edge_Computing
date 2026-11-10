# Milestone 2: Fair Standardized Benchmark Report

**Student**: Sri Jananii S (`sri` / Sri Janani S)  
**Milestone**: M2 Optimize  
**Task**: Fair benchmark  
**Rubric Weight**: 4 Marks  

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

## 3. Sri Jananii S's Measured Benchmark Results

| Runtime Engine | Warm-Up Runs | Timed Runs | Batch Size | Median Latency ($p_{50}$) | 95th Percentile ($p_{95}$) | Throughput (FPS) | Binary Model Size |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PyTorch FP32 (Baseline)** | 20 | 100 | 1 | **208.42 ms** | 224.81 ms | **4.80 FPS** | 6.00 MB |
| **ONNX Runtime FP32** | 20 | 100 | 1 | **82.38 ms** | 89.44 ms | **12.14 FPS** | 11.58 MB |
| **TFLite INT8 (Quantized)** | 20 | 100 | 1 | **60.24 ms** | **63.85 ms** | **16.61 FPS** | **3.24 MB** |

---

## 4. Key Takeaways
1. **Latency Reduction**: Median inference latency dropped from **208.42 ms to 60.24 ms** (71.1% reduction).
2. **Deterministic Response**: The 95th percentile tail latency ($p_{95} = 63.85\text{ ms}$) sits safely below the 100 ms conveyor deadline.
3. **Model Footprint**: Binary footprint compressed from 11.58 MB down to **3.24 MB**, ensuring sustained 16.61 FPS without thermal throttling.
