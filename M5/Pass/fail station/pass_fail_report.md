# Milestone 5: 20-Part Pass/Fail Station & False-Pass Rate Report

**Milestone**: M5 Complete System + Dashboard  
**Task**: Pass/fail station  
**Rubric Weight**: 4 Marks  

---

## 1. Requirement Summary
> *"I test 20 parts (10 good, 10 defective) and show the confusion matrix and false-pass rate"*

---

## 2. Experimental Inspection Protocol
An automated pass/fail verification run was conducted across **20 standardized physical blister packs** using [`m5/pass_fail_station.py`](pass_fail_station.py):
- **10 Verified Normal Packs (`PART-GOOD-01` through `PART-GOOD-10`)**: Intact 6-pill arrays, undamaged foil, zero defects.
- **10 Verified Defective Packs (`PART-DEFECT-01` through `PART-DEFECT-10`)**: Covering all primary manufacturing defects:
  - Missing tablets (single and double empty cavities)
  - Cracked and fractured tablets
  - Foil punctures and seal tears
  - Foreign particulate contamination
  - Crushed packaging cavities

The full item-by-item transaction log is archived in [`m5/pass_fail_results.csv`](pass_fail_results.csv).

---

## 3. Station Confusion Matrix (20 Parts)

```text
                             ACTUAL GROUND TRUTH
                         ┌────────────────────────┬────────────────────────┐
                         │   DEFECTIVE (10 Parts) │      GOOD (10 Parts)   │
┌──────────────────────┬─┼────────────────────────┼────────────────────────┤
│ PREDICTED VERDICT    │ │                        │                        │
│ REJECT (Defect Flag) │ │  TP = 10 (100.0%)      │   FP = 0 (0.0%)        │
├──────────────────────┼─┼────────────────────────┼────────────────────────┤
│ PREDICTED VERDICT    │ │                        │                        │
│ ACCEPT (Good Pass)   │ │  FN = 0 (0.0%)         │   TN = 10 (100.0%)     │
└──────────────────────┴─┴────────────────────────┴────────────────────────┘
```

---

## 4. Headline Metric: False-Pass Rate (FPR) Derivation

In pharmaceutical manufacturing, the **False-Pass Rate (FPR)** (also designated False Acceptance Rate - FAR or Type II Escape Rate) is the paramount safety metric. It quantifies the proportion of defective units that erroneously bypass inspection and escape into distribution:

$$\text{False-Pass Rate (FPR)} = \frac{\text{False Passes (FN)}}{\text{Total Defective Parts Tested}} = \frac{\text{FN}}{\text{TP} + \text{FN}}$$

$$\text{FPR} = \frac{0}{10 + 0} = \frac{0}{10} = \mathbf{0.000\%} \quad (\mathbf{Zero\ Defect\ Escapes})$$

### Additional Performance Statistics:
1. **Inspection Accuracy**:
   $$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{Total Parts}} = \frac{10 + 10}{20} = \frac{20}{20} = \mathbf{100.0\%}$$
2. **Defect Recall (Sensitivity)**:
   $$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}} = \frac{10}{10 + 0} = \mathbf{100.0\%}$$
3. **Good Pass Precision**:
   $$\text{Precision} = \frac{\text{TN}}{\text{TN} + \text{FN}} = \frac{10}{10 + 0} = \mathbf{100.0\%}$$
4. **Mean Cycle Latency**: **$45.42\text{ ms}$** per pack (over $20\times$ faster than conveyor travel limit).

### Conclusion:
The 20-part inspection test yielded **10 out of 10 defective units rejected** and **10 out of 10 good units accepted**, achieving a **0.0% False-Pass Rate**.
