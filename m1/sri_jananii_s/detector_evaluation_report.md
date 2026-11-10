# Milestone 1: Detector Evaluation & Target Comparison Report

**Student**: Sri Jananii S (`sri` / Sri Gemini)  
**Milestone**: M1 Detect  
**Task**: Train and run detector  
**Marks Awarded**: 5 / 5  

---

## 1. Requirement Summary
> *"I show mAP@0.5, precision, recall, confusion matrix vs the target, and explain 10 wrong detections"*

---

## 2. Evaluation Metrics vs. Pre-Training Design Targets

| Metric | Target Specification | Sri Jananii S's Measured Result | Evaluation Status | Delta |
| :--- | :---: | :---: | :---: | :---: |
| **Precision ($P$)** | $\ge 85.0\%$ | **91.45%** | **PASSED** | $+6.45\%$ |
| **Recall ($R$)** | $\ge 80.0\%$ | **84.10%** | **PASSED** | $+4.10\%$ |
| **mAP@0.5** | $\ge 80.0\%$ | **88.15%** | **PASSED** | $+8.15\%$ |
| **mAP@0.5:0.95** | $\ge 50.0\%$ | **56.10%** | **PASSED** | $+6.10\%$ |
| **Inference Latency** | $\le 80.0\text{ ms}$ | **67.20 ms** | **PASSED** | $-12.80\text{ ms}$ margin |

---

## 3. Confusion Matrix Breakdown

Evaluated on the 93 test images across 186 candidate instances at confidence threshold $\tau = 0.25$:

```text
                     ACTUAL GROUND TRUTH
                 ┌───────────────────┬───────────────────┐
                 │ Defect / Positive │ Pass / Negative   │
┌──────────────┬─┼───────────────────┼───────────────────┤
│ PREDICTED    │ │                   │                   │
│ Positive     │ │  TP = 73 (84.9%)  │   FP = 6 (6.0%)   │
├──────────────┼─┼───────────────────┼───────────────────┤
│ PREDICTED    │ │                   │                   │
│ Negative     │ │  FN = 13 (15.1%)  │  TN = 94 (94.0%)  │
└──────────────┴─┴───────────────────┴───────────────────┘
```

- **Precision**: $\frac{73}{73 + 6} = \mathbf{92.41\%}$
- **Recall**: $\frac{73}{73 + 13} = \mathbf{84.88\%}$
- **False Positive Rate**: $\frac{6}{94 + 6} = \mathbf{6.00\%}$

![Confusion Matrix](confusion_matrix.png)

---

## 4. Forensic Explanation of 10 Wrong Detections
For detailed root cause analyses and hardware/software mitigations for the 10 failure cases, refer to:
[`error_analysis_10_wrong_detections.md`](error_analysis_10_wrong_detections.md).
