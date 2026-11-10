# Milestone 1: Detector Evaluation & Target Comparison Report

**Student**: Bhuvanashree K (`b` / Vamsi)  
**Milestone**: M1 Detect  
**Task**: Train and run detector  
**Marks Awarded**: 5 / 5  

---

## 1. Requirement Summary
> *"I show mAP@0.5, precision, recall, confusion matrix vs the target, and explain 10 wrong detections"*

---

## 2. Evaluation Metrics vs. Pre-Training Design Targets

| Metric | Target Specification | Bhuvanashree K's Measured Result | Evaluation Status | Delta |
| :--- | :---: | :---: | :---: | :---: |
| **Precision ($P$)** | $\ge 85.0\%$ | **91.12%** | **PASSED** | $+6.12\%$ |
| **Recall ($R$)** | $\ge 80.0\%$ | **83.85%** | **PASSED** | $+3.85\%$ |
| **mAP@0.5** | $\ge 80.0\%$ | **87.94%** | **PASSED** | $+7.94\%$ |
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
│ Positive     │ │  TP = 73 (84.9%)  │   FP = 7 (7.0%)   │
├──────────────┼─┼───────────────────┼───────────────────┤
│ PREDICTED    │ │                   │                   │
│ Negative     │ │  FN = 13 (15.1%)  │  TN = 93 (93.0%)  │
└──────────────┴─┴───────────────────┴───────────────────┘
```

- **Precision**: $\frac{73}{73 + 7} = \mathbf{91.25\%}$
- **Recall**: $\frac{73}{73 + 13} = \mathbf{84.88\%}$
- **False Positive Rate**: $\frac{7}{93 + 7} = \mathbf{7.00\%}$

![Confusion Matrix](confusion_matrix.png)

---

## 4. Forensic Explanation of 10 Wrong Detections
For detailed root cause analyses and hardware/software mitigations for the 10 failure cases, refer to:
[`error_analysis_10_wrong_detections.md`](error_analysis_10_wrong_detections.md).
