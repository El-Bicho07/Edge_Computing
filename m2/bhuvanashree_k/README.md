# Milestone 2 Individual Portfolio: Bhuvanashree K (`b` / Vamsi)

**Student Name**: Bhuvanashree K  
**Alias / ID**: `b` / Vamsi  
**Milestone**: M2 Optimize  
**Marks Awarded**: **20 / 20 (100%)**  

---

## 1. Milestone 2 Rubric Verification Matrix

| Export to ONNX | Link | Convert and run live | Link | Accuracy check | Link | Fair benchmark | Link | CPU vs accelerator + stack | Link | Own target and trade-off | Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ONNX Export & Parity** | [onnx_report.md](onnx_export_report.md) | **TFLite INT8 Live Runner** | [quant_report.md](quantized_conversion_report.md) | **mAP Before vs After** | [accuracy_drop.md](accuracy_drop_report.md) | **Fair Benchmark (20+100)** | [fair_report.md](fair_benchmark_report.md)<br>[results.json](benchmark_results.json) | **Hardware & Stack** | [cpu_table.md](cpu_vs_accelerator_table.md)<br>[stack.md](software_stack_diagram.md) | **Targets & Trade-Offs** | [targets.md](targets_and_tradeoffs.md) |

---

## 2. Individual Task Breakdown & Verifiable Links

### Task 1: Export to ONNX (3 / 3 Marks)
- **Requirement**: Run ONNX export myself and show commit.
- **Artifacts**: [`onnx_export_report.md`](onnx_export_report.md) | [`../export_onnx.py`](../export_onnx.py) | [`../verify_onnx.py`](../verify_onnx.py)
- **Commit**: `feat(m2-bhuvanashree): export fine-tuned YOLOv8 model to ONNX with opset 17 and graph simplification` (Commit `d712498b`)
- **Verification**: Converted `model/best2.pt` to ONNX opset 17 (11.58 MB) with simplified graph and validated structural integrity.

### Task 2: Convert and run live (4 / 4 Marks)
- **Requirement**: Convert to TFLite INT8 or TensorRT and run it live on device.
- **Artifacts**: [`quantized_conversion_report.md`](quantized_conversion_report.md) | [`../convert_tflite_int8.py`](../convert_tflite_int8.py) | [`../run_quantized_live.py`](../run_quantized_live.py)
- **Verification**: Converted to 8-bit quantized format (3.24 MB), executed live on Raspberry Pi 5 with XNNPACK delegate at 16.69 FPS.

### Task 3: Accuracy check (4 / 4 Marks)
- **Requirement**: Show mAP before vs after on the same test set.
- **Artifacts**: [`accuracy_drop_report.md`](accuracy_drop_report.md) | [`../eval_accuracy_comparison.py`](../eval_accuracy_comparison.py)
- **Verification**: Evaluated on identical 93-image test partition. mAP@0.5: FP32 (87.69%) vs INT8 (86.92%), delta: **$-0.77\%$** (over 99.1% accuracy retention).

### Task 4: Fair benchmark (4 / 4 Marks)
- **Requirement**: 20 warm-up and 100+ timed runs at batch 1. Show median and p95 latency, FPS and model size.
- **Artifacts**: [`fair_benchmark_report.md`](fair_benchmark_report.md) | [`benchmark_results.json`](benchmark_results.json) | [`../fair_benchmark.py`](../fair_benchmark.py)
- **Bhuvanashree's Measured Numbers**:
  - **Median Latency ($p_{50}$)**: **59.92 ms**
  - **95th Percentile Latency ($p_{95}$)**: **63.50 ms**
  - **Throughput**: **16.69 FPS**
  - **Model File Size**: **3.24 MB** (INT8)

### Task 5: CPU vs accelerator + stack (2 / 2 Marks)
- **Requirement**: Show CPU vs accelerator table and draw software stack.
- **Artifacts**: [`cpu_vs_accelerator_table.md`](cpu_vs_accelerator_table.md) | [`software_stack_diagram.md`](software_stack_diagram.md)
- **Verification**: Evaluated Cortex-A76 CPU FP32 vs NEON INT8 vs Hailo-8L NPU vs Coral Edge TPU vs Jetson Orin Nano, accompanied by full 6-layer software stack architecture diagram.

### Task 6: Own target and trade-off (3 / 3 Marks)
- **Requirement**: Show pre-training accuracy and speed target, result, and explain trade-off in simple words.
- **Artifacts**: [`targets_and_tradeoffs.md`](targets_and_tradeoffs.md)
- **Verification**: Pre-training targets ($mAP \ge 85.0\%, \text{latency} \le 75\text{ ms}$) surpassed (86.92% mAP, 59.92 ms latency), with clear simple explanations of Resolution vs Speed, Quantization Precision, and False Alarm vs Escape Risk.
