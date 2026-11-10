# Milestone 2: Accuracy Evaluation Before vs. After Quantization

**Student**: Theeran (Dheeran)  
**Milestone**: M2 Optimize  
**Task**: Accuracy check  
**Rubric Weight**: 4 Marks  

---

## 1. Requirement Summary
> *"I show mAP before vs after on the same test set"*

---

## 2. Experimental Methodology
To evaluate the impact of edge quantization on defect detection fidelity, both the original unquantized PyTorch float32 model (`model/best2.pt`) and the quantized INT8 engine (`m2/model_int8.tflite`) were evaluated against the identical frozen test partition:
- **Test Partition**: `dataset/Defect Detection.v1i.yolov8/test/`
- **Total Test Images**: 93 images (186 labeled candidate components)
- **Evaluation Resolution**: $416 \times 416$ pixels
- **Confidence Threshold**: $\tau = 0.25$
- **NMS IoU Threshold**: $\text{IoU} = 0.45$
- **Evaluation Script**: [`../eval_accuracy_comparison.py`](eval_accuracy_comparison.py)

---

## 3. Comparative Accuracy Table (Before vs. After)

| Evaluation Metric | Baseline Model (FP32 PyTorch) | Quantized Model (INT8 TFLite) | Net Delta ($\Delta$) | Retention Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Precision ($P$)** | **90.81%** (0.9081) | **89.95%** (0.8995) | **$-0.86\%$** | **99.05%** |
| **Recall ($R$)** | **83.50%** (0.8350) | **83.10%** (0.8310) | **$-0.40\%$** | **99.52%** |
| **mAP@0.5** | **87.69%** (0.8769) | **86.92%** (0.8692) | **$-0.77\%$** | **99.12%** |
| **mAP@0.5:0.95** | **55.62%** (0.5562) | **54.88%** (0.5488) | **$-0.74\%$** | **98.67%** |
| **F1-Score** | **87.00%** (0.8700) | **86.38%** (0.8638) | **$-0.62\%$** | **99.29%** |
| **Binary Model Size**| **6.00 MB** | **3.24 MB** | **$-46.0\%$** | Memory Bandwidth Halved |
| **Raspberry Pi 5 Latency** | **206.5 ms** (~4.8 FPS) | **60.5 ms** (~16.5 FPS) | **$-70.7\%$** | **3.41$\times$ Throughput Gain** |

---

## 4. Technical Analysis of Minimal Quantization Loss

In many naive INT8 quantization pipelines, models suffer from 5% to 15% mAP degradation due to dynamic range truncation. Here, the net mAP drop was restricted to **0.77%** ($< 1\%$) through three engineering techniques:

1. **Representative Calibration Dataset**: Rather than using Gaussian random noise, 100 actual industrial images covering high-glare surfaces, empty cavities, and dark components were supplied to the calibrator, ensuring optimal clipping thresholds $[\alpha_{\min}, \alpha_{\max}]$.
2. **Kullback-Leibler (KL) Divergence Minimization**: Used relative entropy to minimize information loss between the floating-point activation distributions and quantized integer bins.
3. **Per-Channel Weight Quantization**: Applied separate scale factors $S_c$ for each convolutional filter channel rather than a single per-tensor scalar, preventing large weights in one filter from saturating fine detail in adjacent filters.
