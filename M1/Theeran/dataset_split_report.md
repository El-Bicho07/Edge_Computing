# Milestone 1: Dataset Split & Zero Data Leakage Report

**Student**: Theeran (Dheeran)  
**Milestone**: M1 Detect  
**Task**: Correct split  
**Rubric Weight**: 2 Marks  

---

## 1. Requirement Summary
> *"I explain and show the 70/20/10 split with no leakage"*

---

## 2. 70 / 20 / 10 Partitioning Rationale

In edge computing model deployment, the standard **70% Training / 20% Validation / 10% Testing** partitioning strategy represents the optimal balance for edge-constrained datasets:
- **70% Training (650 images)**: Maximizes gradient variety for weight optimization without overfitting to background textures.
- **20% Validation (186 images)**: Provides an adequately large distribution for tuning early-stopping patience, confidence thresholds ($\tau$), and NMS IoU overlap thresholds.
- **10% Testing (93 images)**: Kept completely blind and frozen for final generalization auditing.

---

## 3. Theeran's Partition Audit Numbers

| Partition Name | Theoretical Ratio | Actual Image Count | Empirical Percentage | Cryptographic SHA-256 Collision Count |
| :--- | :---: | :---: | :---: | :---: |
| **Train Set** | 70.0% | **650** | **69.97%** | 0 duplicates |
| **Validation Set** | 20.0% | **186** | **20.02%** | 0 duplicates |
| **Test Set** | 10.0% | **93** | **10.01%** | 0 duplicates |
| **Total Images** | **100.0%** | **929** | **100.00%** | **Zero Cross-Split Duplicates (0.00%)** |

---

## 4. Cryptographic Proof of Zero Data Leakage

All image payloads were hashed using cryptographic SHA-256 digests via [`../verify_dataset_split.py`](../verify_dataset_split.py):

$$\text{Train} \cap \text{Validation} = \emptyset \quad (\text{Intersection} = 0)$$
$$\text{Train} \cap \text{Test} = \emptyset \quad (\text{Intersection} = 0)$$
$$\text{Validation} \cap \text{Test} = \emptyset \quad (\text{Intersection} = 0)$$

$$\text{Confirmed Data Leakage} = \mathbf{0.000\%}$$

This mathematical disjointness guarantees that the reported test mAP reflects true out-of-sample edge generalization.
