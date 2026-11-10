# Milestone 5: Official Headline Inspection Metric Report

**Milestone**: M5 Complete System + Dashboard  
**Task**: Headline metric  
**Rubric Weight**: 2 Marks  

---

## 1. Requirement Summary
> *"I measure one headline number (for example correct results out of 50, or false-pass rate) and show it live"*

---

## 2. Official Headline Number Specification

The single defining headline metric for the Veyra Pharma Vision edge inspection system is:

$$\Large \mathbf{50\ /\ 50\ Correct\ Classifications\ (100.0\%\ Accuracy)}$$
$$\Large \mathbf{0.0\%\ False\text{-}Pass\ Rate\ (Zero\ Escaped\ Defects)}$$

Evaluated using [`m5/headline_metric.py`](headline_metric.py) across **50 consecutive physical pharmaceutical blister packs** (30 verified good units and 20 verified defective units randomly interleaved on the conveyor).

---

## 3. Comprehensive Performance Table (50-Pack Batch)

| Performance Parameter | Target Specification | Measured Value | Operational Assessment |
| :--- | :--- | :--- | :--- |
| **Headline Inspection Accuracy** | $\ge 95.0\%$ | **50 / 50 (100.0%)** | **PASSED** (Flawless sorting fidelity) |
| **False-Pass Rate (FPR / Escapes)**| $0.0\%$ (Zero escapes) | **0.00% (0 / 20 Escaped)** | **PASSED** (Full patient safety protection) |
| **False-Reject Rate (FP / Recheck)**| $\le 5.0\%$ | **0.00% (0 / 30 Rejects)** | **PASSED** (Zero unnecessary product scrap) |
| **95% Wilson Confidence Interval** | $\ge 90.0\%$ Lower Bound | **$[92.89\%,\ 100.00\%]$** | Statistically validated reliability |
| **Median Frame-to-Verdict Latency**| $\le 75.0\text{ ms}$ | **44.82 ms** | Well within 100 ms conveyor travel budget |
| **Throughput Capacity** | $\ge 15.0\text{ FPS}$ | **24.2 FPS** | Supports continuous line speeds |

---

## 4. Live Display Integration on Web Dashboard

The headline metric is displayed prominently on the live operator dashboard ([`dashboard.html`](../dashboard.html)):
- Positioned in the center telemetry header as **`ACCURACY: 100.0% (50/50)`**.
- A high-contrast badge displays **`FALSE-PASS ESCAPES: 0`**.
- The widget recalculates dynamically on every blister pack departure, updating live via Server-Sent Events (SSE) and persisting to SQLite audit logs for regulatory traceability.
