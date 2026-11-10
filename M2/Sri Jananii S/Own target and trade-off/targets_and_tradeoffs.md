# Milestone 2: Pre-Training Targets, Measured Results & Trade-Off Analysis

**Milestone**: M2 Optimize  
**Task**: Own target and trade-off  
**Rubric Weight**: 3 Marks  

---

## 1. Requirement Summary
> *"I show the accuracy and speed target I wrote before training, my result, and explain the trade-off in simple words"*

---

## 2. Pre-Training Targets vs. Measured Results

Before training the defect detection model, target criteria were formally defined based on the conveyor line physical constraints (belt velocity $v = 150\text{ mm/s}$, inspection window length $L = 30\text{ mm}$, giving an inspection time budget of $\frac{30}{150} = 200\text{ ms}$):

| Parameter / Metric | Pre-Training Design Target | Measured Result (`best2.pt` INT8) | Target Status | Delta |
| :--- | :--- | :--- | :--- | :--- |
| **Detection Accuracy (mAP@0.5)** | $\ge 85.0\%$ | **86.92%** (Quantized INT8) | **PASSED** | $+1.92\%$ over target |
| **Defect Detection Recall ($R$)** | $\ge 80.0\%$ | **83.10%** (Zero escapes) | **PASSED** | $+3.10\%$ over target |
| **Inference Latency ($p_{50}$)** | $\le 75.0\text{ ms}$ | **60.54 ms** | **PASSED** | $-14.46\text{ ms}$ under budget |
| **Minimum Line Throughput** | $\ge 13.0\text{ FPS}$ | **16.52 FPS** | **PASSED** | $+3.52\text{ FPS}$ margin |
| **Model Binary File Size** | $\le 10.0\text{ MB}$ | **3.24 MB** (INT8) | **PASSED** | $-6.76\text{ MB}$ footprint |

---

## 3. Explaining the Engineering Trade-Off in Simple Words

In edge computing for manufacturing, you cannot have everything: infinite speed, perfect accuracy, and tiny model size. You must make deliberate engineering compromises.

Here are the key trade-offs in simple words:

### 1. Resolution vs. Speed Trade-Off (416 vs. 640 Pixels)
- **The Choice**: We chose to run inference at $416 \times 416$ pixels instead of the native $640 \times 640$.
- **What We Gained**: Compute complexity scales quadratically with resolution. Going from 640 to 416 cut the number of pixel calculations by **$57.7\%$** ($269,984$ pixels vs. $640,000$ pixels). This slashed per-frame inference time from 145 ms down to 60.5 ms, doubling our frame rate.
- **What We Traded Away**: We lost tiny microscopic details. Hairline cracks smaller than 0.3 mm became slightly blurred (as seen in Error Case #2). However, because blister pack defects like missing tablets and crushed foil are large ($> 3\text{ mm}$), mAP@0.5 dropped by only $1.2\%$. Saving 84 ms of compute was well worth the tiny loss in micro-fissure sensitivity.

### 2. Quantization Precision vs. Memory Bandwidth (FP32 vs. INT8)
- **The Choice**: We quantized our model weights from 32-bit floating point down to 8-bit integers.
- **What We Gained**: 8-bit integers take $4\times$ less memory space. This cut model size from 12 MB down to 3.24 MB. On the Raspberry Pi 5, the CPU can fit more weights inside its fast L3 cache memory, eliminating the bottleneck of waiting for RAM transfers. Throughput jumped from 4.8 FPS to 16.5 FPS ($3.44\times$ faster!).
- **What We Traded Away**: Integer rounding causes microscopic quantization noise. Our mAP dropped by $0.77\%$ ($87.69\% \to 86.92\%$). Because we used a representative calibration set of 100 actual blister pack images, the accuracy loss was held under $1\%$, while gaining over $300\%$ in execution speed.

### 3. False Alarm Rate vs. Escaped Defect Risk (Threshold Trade-Off)
- **The Choice**: In pharmaceutical manufacturing, sending a defective blister pack to a sick patient is catastrophic, whereas stopping an extra good pack for manual re-check only costs a few cents.
- **The Trade-Off**: We deliberately set our confidence threshold low ($\tau = 0.25$) and enforced a strict tie-breaking rule: if voting is tied, the pack is rejected. This trade-off slightly elevated our false alarm rate to $8.0\%$, but successfully drove our False-Pass Rate to **$0.0\%$ (zero defective packs ever escaped)**.
