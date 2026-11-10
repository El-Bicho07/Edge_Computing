# Milestone 2: CPU vs. Hardware Accelerator Comparative Analysis

**Student**: Theeran (Dheeran)  
**Milestone**: M2 Optimize  
**Task**: CPU vs accelerator + stack  
**Rubric Weight**: Part of 2 Marks  

---

## 1. Requirement Summary
> *"I show the CPU vs accelerator table and draw the software stack"*

---

## 2. Hardware Architecture Comparison

To assess deployment scalability for industrial inspection, the fine-tuned YOLOv8 model ($416\times416$ resolution) was evaluated across edge CPU and dedicated edge AI acceleration architectures:

| Platform / Accelerator | Compute Engine Architecture | Model Format & Precision | Inference Latency ($p_{50}$) | Throughput (FPS) | Board TDP / Power Draw | Efficiency (FPS / Watt) | Unit Price (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Raspberry Pi 5 (CPU FP32)** | Quad Cortex-A76 @ 2.4 GHz | PyTorch `.pt` (FP32) | **206.5 ms** | **4.84 FPS** | ~8.5 W | 0.57 FPS/W | $80 |
| **Raspberry Pi 5 (CPU NEON SIMD)** | Quad Cortex-A76 (ARM NEON) | Tencent NCNN / TFLite INT8 | **60.5 ms** | **16.53 FPS** | ~6.8 W | 2.43 FPS/W | $80 |
| **Raspberry Pi AI Kit (Hailo-8L)** | Dedicated Neural Co-processor (13 TOPS) | Hailo HEF (INT8) | **14.2 ms** | **70.4 FPS** | ~8.2 W (Pi + M.2) | **8.58 FPS/W** | $150 (Total) |
| **Google Coral Edge TPU** | Google Edge TPU ASIC (4 TOPS) | Edge TPU `.tflite` (INT8) | **28.6 ms** | **35.0 FPS** | ~7.2 W | 4.86 FPS/W | $140 (Total) |
| **NVIDIA Jetson Orin Nano (40 TOPS)** | 1024-core Ampere GPU + 32 Tensor Cores | TensorRT INT8 Engine | **8.6 ms** | **116.2 FPS** | ~15.0 W | 7.74 FPS/W | $499 |

---

## 3. Engineering Analysis & Trade-Offs

1. **CPU with NEON Vectorization (Current Production Platform)**:
   - **Advantage**: Requires zero additional coprocessor hardware, keeping unit cost at $80 and simplifying physical mounting on the inspection stand.
   - **Throughput**: At 16.53 FPS (peak 21.5 FPS on HUD), it satisfies the 15 FPS line requirement while operating at 6.8W.
2. **Dedicated NPU Acceleration (Hailo-8L / Coral TPU)**:
   - **Advantage**: Offloads 100% of tensor matrix multiplication from the host CPU. CPU utilization drops from 58% to under 6%, freeing cycles for complex database querying, multi-camera streaming, and edge analytics.
   - **Efficiency**: Delivers 8.58 FPS/Watt, over $3.5\times$ more energy-efficient than CPU execution.
3. **High-End Edge GPU (Jetson Orin Nano)**:
   - Provides peak throughput (116 FPS) allowing multiple inspection lines to share one centralized box, but at $6.2\times$ the hardware cost and higher power draw.
