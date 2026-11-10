# Milestone 2: M2 Optimize (Max Marks: 20)

This directory contains the complete source code, quantization engines, benchmark harnesses, individual student contributions, visual proof photos, architectural diagrams, and trade-off analyses for **Milestone 2: Optimize**.

---

## 🏆 Evaluator Link Matrix (M2 Optimize)

for M2

| Export to ONNX | Link | Convert and run live | Link | Accuracy check | Link | Fair benchmark | Link | CPU vs accelerator + stack | Link | Own target and trade-off | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ONNX Conversion** | [`export_onnx.py`](export_onnx.py)<br>[`verify_onnx.py`](verify_onnx.py)<br>[`onnx_export_report.md`](onnx_export_report.md) | **TFLite INT8 Edge Inference** | [`convert_tflite_int8.py`](convert_tflite_int8.py)<br>[`run_quantized_live.py`](run_quantized_live.py)<br>[`quantized_conversion_report.md`](quantized_conversion_report.md)<br>[`photo_ak.jpg`](photo_ak.jpg)<br>[`photo_sri.jpg`](photo_sri.jpg)<br>[`photo_b.jpg`](photo_b.jpg) | **mAP Before vs After** | [`eval_accuracy_comparison.py`](eval_accuracy_comparison.py)<br>[`accuracy_drop_report.md`](accuracy_drop_report.md) | **Fair Benchmark (20+100 runs)** | [`fair_benchmark.py`](fair_benchmark.py)<br>[`benchmark_results.json`](benchmark_results.json)<br>[`fair_benchmark_report.md`](fair_benchmark_report.md) | **Hardware & Architecture** | [`cpu_vs_accelerator_table.md`](cpu_vs_accelerator_table.md)<br>[`software_stack_diagram.md`](software_stack_diagram.md) | **Targets & Trade-Offs** | [`targets_and_tradeoffs.md`](targets_and_tradeoffs.md) |

---

## 👥 Individual Student Task Verification Matrix

Each team member has executed individual ONNX conversions, quantization runs, accuracy verifications, and standardized benchmarks on edge hardware. Dedicated student subfolders contain complete individual proofs:

| Order | Student Name | Photo ID & Alias | Export to ONNX (3M) | Convert & run live (4M) | Accuracy check (4M) | Fair benchmark (4M) | CPU vs accel + stack (2M) | Own target & trade-off (3M) | Status | Dedicated Subfolder |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Akshaya M** | `photo ak`<br>(Akshay) | [ONNX Report & Commit](akshaya_m/onnx_export_report.md) | [Live INT8 Runner](akshaya_m/quantized_conversion_report.md)<br>[Own Photo Proof](akshaya_m/photo_ak.jpg) | [Accuracy Drop](akshaya_m/accuracy_drop_report.md)<br>mAP: -0.77% | [Fair Benchmark](akshaya_m/fair_benchmark_report.md)<br>[Results JSON](akshaya_m/benchmark_results.json) | [Hardware Table](akshaya_m/cpu_vs_accelerator_table.md)<br>[Stack Diagram](akshaya_m/software_stack_diagram.md) | [Pre-Training Target](akshaya_m/targets_and_tradeoffs.md)<br>Trade-off Analysis | **Submitted (Max: 20M)** | [`akshaya_m/`](akshaya_m/) |
| **2** | **Sri Janani S** | `photo sri`<br>(Sri Janani S) | [ONNX Report & Commit](sri_jananii_s/onnx_export_report.md) | [Live INT8 Runner](sri_jananii_s/quantized_conversion_report.md)<br>[Own Photo Proof](sri_jananii_s/photo_sri.jpg) | [Accuracy Drop](sri_jananii_s/accuracy_drop_report.md)<br>mAP: -0.77% | [Fair Benchmark](sri_jananii_s/fair_benchmark_report.md)<br>[Results JSON](sri_jananii_s/benchmark_results.json) | [Hardware Table](sri_jananii_s/cpu_vs_accelerator_table.md)<br>[Stack Diagram](sri_jananii_s/software_stack_diagram.md) | [Pre-Training Target](sri_jananii_s/targets_and_tradeoffs.md)<br>Trade-off Analysis | **Submitted (Max: 20M)** | [`sri_jananii_s/`](sri_jananii_s/) |
| **3** | **Bhuvanashree K** | `photo b`<br>(Vamsi) | [ONNX Report & Commit](bhuvanashree_k/onnx_export_report.md) | [Live INT8 Runner](bhuvanashree_k/quantized_conversion_report.md)<br>[Own Photo Proof](bhuvanashree_k/photo_b.jpg) | [Accuracy Drop](bhuvanashree_k/accuracy_drop_report.md)<br>mAP: -0.77% | [Fair Benchmark](bhuvanashree_k/fair_benchmark_report.md)<br>[Results JSON](bhuvanashree_k/benchmark_results.json) | [Hardware Table](bhuvanashree_k/cpu_vs_accelerator_table.md)<br>[Stack Diagram](bhuvanashree_k/software_stack_diagram.md) | [Pre-Training Target](bhuvanashree_k/targets_and_tradeoffs.md)<br>Trade-off Analysis | **Submitted (Max: 20M)** | [`bhuvanashree_k/`](bhuvanashree_k/) |

---

## 📸 Quantized Edge Inference Visual Evidence (Live HUD Runs on Edge Device)

The edge-deployed TFLite INT8 inference pipeline (`run_quantized_live.py`) was executed live on Raspberry Pi 5 with real-time HUD overlays (FPS counter, bounding boxes, component classes, and confidence mapping). Contributed live inference frames across the team in exact order:

| Order | Contributing Student | Physical Object & Labelled Features | Quantized Edge HUD Live Ingestion Proof |
| :---: | :--- | :--- | :---: |
| **1** | **Akshaya M**<br>(Akshay) | **`base`**, **`internal_component`**, **`assembly`**, **`assembled_enclosure`** multi-stage enclosure detection sequence with live FPS and bounding box HUD telemetry | ![Akshaya M Live Quantized Inference](photo_ak.jpg) |
| **2** | **Sri Janani S**<br>(Sri Janani S) | **`enclosure_system`**, **`enclosure_body`**, **`internal_alignment`**, **`magnet_attachment`**, **`assembly`** 9-frame edge inspection sequence (arrow indicator removed) | ![Sri Janani S Live Quantized Inference](photo_sri.jpg) |
| **3** | **Bhuvanashree K**<br>(Vamsi) | **`assembled_enclosure`** 9-frame real-time edge tracking and assembly QA sequence | ![Bhuvanashree K Live Quantized Inference](photo_b.jpg) |

---

## 📊 Summary of Milestone 2 Technical Results

### 1. Standardized Fair Benchmark Across Students (Batch 1, 20 Warm-up + 100 Timed Runs)

Tested on Raspberry Pi 5 (ARM Cortex-A76 quad-core @ 2.4 GHz, 8GB RAM):

| Order | Student Name | Runtime Engine | Median Latency ($p_{50}$) | 95th Percentile ($p_{95}$) | Throughput (FPS) | Model File Size | Status vs 15 FPS Target |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | **Akshaya M** | TFLite INT8 (NEON) | **60.82 ms** | **64.21 ms** | **16.44 FPS** | **3.24 MB** | **PASSED (+1.44 FPS)** |
| **2** | **Sri Janani S** | TFLite INT8 (NEON) | **60.24 ms** | **63.85 ms** | **16.61 FPS** | **3.24 MB** | **PASSED (+1.61 FPS)** |
| **3** | **Bhuvanashree K** | TFLite INT8 (NEON) | **59.92 ms** | **63.50 ms** | **16.69 FPS** | **3.24 MB** | **PASSED (+1.69 FPS)** |
| — | *Baseline* | *PyTorch FP32* | *208.42 ms* | *224.81 ms* | *4.80 FPS* | *6.00 MB* | *Too Slow for Live Line* |
| — | *Intermediate* | *ONNX Runtime FP32* | *82.38 ms* | *89.44 ms* | *12.14 FPS* | *11.58 MB* | *Close but sub-target* |

### 2. Accuracy Retention Before vs. After Quantization (Same 93-Image Test Set)

| Metric | Baseline (PyTorch FP32) | Quantized (TFLite INT8) | Net Change ($\Delta$) | Accuracy Retention |
| :--- | :---: | :---: | :---: | :---: |
| **mAP@0.5** | **87.69%** | **86.92%** | **$-0.77\%$** | **99.12% Retention** |
| **Precision ($P$)** | **90.81%** | **89.95%** | **$-0.86\%$** | **99.05% Retention** |
| **Recall ($R$)** | **83.50%** | **83.10%** | **$-0.40\%$** | **99.52% Retention** |
| **Latency ($p_{50}$)** | **208.4 ms** | **60.5 ms** | **$-70.9\%$** | **$3.44\times$ Speedup** |

### 3. CPU vs. Hardware Accelerator Comparative Evaluation

| Platform / Accelerator | Architecture | Model Format | Latency ($p_{50}$) | FPS | Power (TDP) | Efficiency | Unit Cost |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Raspberry Pi 5 CPU (FP32)** | Quad Cortex-A76 @ 2.4 GHz | PyTorch FP32 | 208.4 ms | 4.8 FPS | ~8.5 W | 0.56 FPS/W | $80 |
| **Raspberry Pi 5 CPU (NEON)** | Quad Cortex-A76 NEON | TFLite INT8 | **60.5 ms** | **16.5 FPS** | ~6.8 W | **2.43 FPS/W** | **$80** |
| **Raspberry Pi AI Kit (Hailo-8L)** | Neural Co-processor (13 TOPS)| Hailo HEF INT8 | 14.2 ms | 70.4 FPS | ~8.2 W | 8.58 FPS/W | $150 |
| **Google Coral Edge TPU** | Edge TPU ASIC (4 TOPS) | Edge TPU TFLite | 28.6 ms | 35.0 FPS | ~7.2 W | 4.86 FPS/W | $140 |
| **NVIDIA Jetson Orin Nano** | 1024-core Ampere GPU (40 TOPS)| TensorRT INT8 | 8.6 ms | 116.2 FPS | ~15.0 W | 7.74 FPS/W | $499 |

### 4. Simple Explanation of Key Engineering Trade-Offs
1. **Resolution vs. Speed (416 vs. 640 Pixels)**: Downscaling to $416\times416$ cuts calculations by $57.7\%$, halving latency from 145 ms to 60.5 ms while losing only $1.2\%$ mAP on non-critical micro-fissures.
2. **Quantization Precision vs. Memory (FP32 vs. INT8)**: Converting 32-bit floats to 8-bit integers slashes memory bandwidth by $4\times$, fits weights into the Cortex-A76 L3 cache, and boosts throughput $3.44\times$ ($4.8 \to 16.5\text{ FPS}$) with only $0.77\%$ mAP drop.
3. **False Alarm vs. Escaped Defect Risk**: Operating threshold was locked to $\tau = 0.25$ with a strict tie-breaking reject rule. While slightly elevating false alarm re-checks to $8.0\%$, it guarantees a **0.0% False-Pass Rate** (zero defective units escape into the supply chain).

---

## 📁 Milestone 2 Directory Structure

```text
m2/
├── README.md                                 # Master Milestone 2 Matrix & Documentation
├── photo_ak.jpg                              # Order 1: Akshaya M Quantized Edge HUD Ingestion Proof
├── photo_sri.jpg                             # Order 2: Sri Janani S Quantized Edge HUD Ingestion Proof (Arrow Removed)
├── photo_b.jpg                               # Order 3: Bhuvanashree K Quantized Edge HUD Ingestion Proof
├── export_onnx.py                            # Task 1 YOLOv8 to ONNX Export Engine
├── verify_onnx.py                            # Task 1 Topology & Parity Checker
├── onnx_export_report.md                     # Task 1 ONNX Export & Commit Report
├── convert_tflite_int8.py                    # Task 2 Post-Training INT8 Quantizer
├── run_quantized_live.py                     # Task 2 Real-Time Edge Runner with HUD
├── quantized_conversion_report.md            # Task 2 Quantized Edge Deployment Report
├── eval_accuracy_comparison.py               # Task 3 Before vs After mAP Evaluator
├── accuracy_drop_report.md                   # Task 3 Quantization Accuracy Drop Audit
├── fair_benchmark.py                         # Task 4 Standardized Fair Benchmark Engine
├── benchmark_results.json                    # Task 4 Machine-Readable Telemetry Data
├── fair_benchmark_report.md                  # Task 4 20-Warmup + 100-Timed Run Report
├── cpu_vs_accelerator_table.md               # Task 5 Hardware Accelerator Comparison
├── software_stack_diagram.md                 # Task 5 6-Layer Architecture Stack
├── targets_and_tradeoffs.md                  # Task 6 Pre-Training Targets vs Results
├── akshaya_m/                                # Order 1: Akshaya M Dedicated Subfolder
│   ├── README.md                             # Individual Task Matrix
│   ├── photo_ak.jpg                          # Own Live Ingestion Evidence
│   ├── onnx_export_report.md                 # Own Commit Proof
│   ├── fair_benchmark_report.md              # Own Benchmark Numbers
│   ├── benchmark_results.json                # Own JSON Telemetry
│   └── ...                                   # Individual Task Artifacts
├── sri_jananii_s/                            # Order 2: Sri Janani S Dedicated Subfolder
│   ├── README.md                             # Individual Task Matrix
│   ├── photo_sri.jpg                         # Own Live Ingestion Evidence (Arrow Removed)
│   ├── onnx_export_report.md                 # Own Commit Proof
│   ├── fair_benchmark_report.md              # Own Benchmark Numbers
│   ├── benchmark_results.json                # Own JSON Telemetry
│   └── ...                                   # Individual Task Artifacts
└── bhuvanashree_k/                           # Order 3: Bhuvanashree K Dedicated Subfolder
    ├── README.md                             # Individual Task Matrix
    ├── photo_b.jpg                           # Own Live Ingestion Evidence
    ├── onnx_export_report.md                 # Own Commit Proof
    ├── fair_benchmark_report.md              # Own Benchmark Numbers
    ├── benchmark_results.json                # Own JSON Telemetry
    └── ...                                   # Individual Task Artifacts
```

---

## 🚀 Quick Execution Commands

```bash
# 1. Export YOLOv8 to ONNX format:
python3 m2/export_onnx.py

# 2. Verify ONNX topological validity:
python3 m2/verify_onnx.py

# 3. Convert to TFLite INT8 with representative calibration:
python3 m2/convert_tflite_int8.py

# 4. Run live quantized edge inference with on-screen HUD:
python3 m2/run_quantized_live.py --model m2/model_int8.tflite --source 0

# 5. Evaluate accuracy before vs. after quantization:
python3 m2/eval_accuracy_comparison.py

# 6. Execute fair standardized benchmark (20 warm-up + 100 timed runs @ batch 1):
python3 m2/fair_benchmark.py --warmup 20 --runs 100 --batch 1
```
