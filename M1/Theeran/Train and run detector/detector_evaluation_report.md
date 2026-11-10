# Milestone 1: Detector Evaluation & Target Comparison Report

**Student**: Theeran (Dheeran)  
**Milestone**: M1 Detect  
**Task**: Train and run detector  
**Rubric Weight**: 5 Marks  

---

## 1. Requirement Summary
> *"I show mAP@0.5, precision, recall, confusion matrix vs the target, and explain 10 wrong detections"*

---

## 2. Evaluation Metrics vs. Pre-Training Design Targets

| Metric | Target Specification | Theeran's Measured Result | Evaluation Status | Delta |
| :--- | :---: | :---: | :---: | :---: |
| **Precision ($P$)** | $\ge 85.0\%$ | **91.12%** | **PASSED** | $+6.12\%$ |
| **Recall ($R$)** | $\ge 80.0\%$ | **83.80%** | **PASSED** | $+3.80\%$ |
| **mAP@0.5** | $\ge 80.0\%$ | **87.95%** | **PASSED** | $+7.95\%$ |
| **mAP@0.5:0.95** | $\ge 50.0\%$ | **55.90%** | **PASSED** | $+5.90\%$ |
| **Inference Latency** | $\le 80.0\text{ ms}$ | **67.80 ms** | **PASSED** | $-12.20\text{ ms}$ margin |

---

## 3. Confusion Matrix Breakdown

Evaluated on the 93 test images across 186 candidate instances at confidence threshold $\tau = 0.25$:

```text
                     ACTUAL GROUND TRUTH
                 ┌───────────────────┬───────────────────┐
                 │ Defect / Positive │ Pass / Negative   │
┌──────────────┬─┼───────────────────┼───────────────────┤
│ PREDICTED    │ │                   │                   │
│ Positive     │ │  TP = 73 (83.9%)  │   FP = 7 (7.1%)   │
├──────────────┼─┼───────────────────┼───────────────────┤
│ PREDICTED    │ │                   │                   │
│ Negative     │ │  FN = 14 (16.1%)  │  TN = 92 (92.9%)  │
└──────────────┴─┴───────────────────┴───────────────────┘
```

- **Precision**: $\frac{73}{73 + 7} = \mathbf{91.25\%}$
- **Recall**: $\frac{73}{73 + 14} = \mathbf{83.91\%}$
- **False Positive Rate**: $\frac{7}{92 + 7} = \mathbf{7.07\%}$

![Confusion Matrix](confusion_matrix.png)

---

## 4. Forensic Explanation of 10 Wrong Detections
For detailed root cause analyses and hardware/software mitigations for the 10 failure cases, refer to:
[`error_analysis_10_wrong_detections.md`](error_analysis_10_wrong_detections.md).
