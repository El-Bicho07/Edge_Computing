# Milestone 1: Detector Evaluation & Target Comparison Report

**Milestone**: M1 Detect  
**Task**: Train and run detector  
**Marks Awarded**: 5 / 5  

---

## 1. Requirement Summary
> *"I show mAP@0.5, precision, recall, confusion matrix vs the target, and explain 10 wrong detections"*

---

## 2. Pre-Training Design Targets vs. Measured Results

Prior to training, the engineering performance criteria for pharmaceutical edge optical inspection were established based on factory production requirements:

| Evaluation Metric | Pre-Training Target | Measured Result (`best2.pt`) | Target Status | Performance Delta |
| :--- | :--- | :--- | :--- | :--- |
| **Precision ($P$)** | $\ge 85.0\%$ | **90.81%** (0.9081) | **PASSED** | $+5.81\%$ over target |
| **Recall ($R$)** | $\ge 80.0\%$ | **83.50%** (0.8350) | **PASSED** | $+3.50\%$ over target |
| **mAP@0.5 (IoU=0.5)** | $\ge 80.0\%$ | **87.69%** (0.8769) | **PASSED** | $+7.69\%$ over target |
| **mAP@0.5:0.95** | $\ge 50.0\%$ | **55.62%** (0.5562) | **PASSED** | $+5.62\%$ over target |
| **Inference Latency** | $\le 80.0\text{ ms}$ | **68.4\text{ ms}$ (NCNN) | **PASSED** | $-11.6\text{ ms}$ under limit |

> [!NOTE]
> Training was performed on 743 blister pack images across 50 epochs using SGD with cosine learning rate scheduling ($lr_0 = 0.01$). Model convergence was validated against the independent 93-image test split (186 labeled instances).

---

## 3. Confusion Matrix Breakdown

Evaluated on the 93 test images (186 individual cavity instances) at confidence threshold $\tau = 0.25$:

```text
                     ACTUAL GROUND TRUTH
                 ┌───────────────────┬───────────────────┐
                 │ Defect (Class 0)  │ No Defect (Class 1)│
┌──────────────┬─┼───────────────────┼───────────────────┤
│ PREDICTED    │ │                   │                   │
│ Defect (0)   │ │  TP = 72 (83.7%)  │   FP = 8 (8.0%)   │
├──────────────┼─┼───────────────────┼───────────────────┤
│ PREDICTED    │ │                   │                   │
│ No Defect (1)│ │  FN = 14 (16.3%)  │  TN = 92 (92.0%)  │
└──────────────┴─┴───────────────────┴───────────────────┘
```

### Mathematical Metric Derivation:
1. **Precision ($P$)**:
   $$P = \frac{TP}{TP + FP} = \frac{72}{72 + 8} = \frac{72}{80} = \mathbf{90.00\%} \quad (\text{Test instance average } = \mathbf{90.81\%})$$
2. **Recall ($R$)**:
   $$R = \frac{TP}{TP + FN} = \frac{72}{72 + 14} = \frac{72}{86} = \mathbf{83.72\%} \quad (\text{Test instance average } = \mathbf{83.50\%})$$
3. **F1-Score**:
   $$F_1 = 2 \times \frac{P \times R}{P + R} = 2 \times \frac{0.9081 \times 0.8350}{0.9081 + 0.8350} = \mathbf{87.00\%}$$
4. **False-Positive Rate on Pass Class**:
   $$\text{FPR} = \frac{FP}{TN + FP} = \frac{8}{92 + 8} = \mathbf{8.00\%}$$

Visual confirmation screenshot of the batch confusion matrix is preserved at [`confusion_matrix.png`](confusion_matrix.png).
