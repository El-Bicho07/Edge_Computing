# Milestone 2: ONNX Export and Optimization Report

**Student**: Theeran (Dheeran)  
**Milestone**: M2 Optimize  
**Task**: Export to ONNX  
**Rubric Weight**: 3 Marks  

---

## 1. Requirement Summary
> *"I run the ONNX export myself and show my commit"*

---

## 2. Export Methodology & Pipeline
The custom YOLOv8 defect detection weights ([`../../model/best2.pt`](../../model/best2.pt)) were converted from PyTorch computational graph format (`.pt`) to Open Neural Network Exchange format ([`../export_onnx.py`](../export_onnx.py)).

### Export Technical Parameters:
- **Source Checkpoint**: `model/best2.pt` (PyTorch FP32, 6.00 MB, 3,006,233 parameters)
- **Target Format**: ONNX (Open Neural Network Exchange)
- **Opset Version**: 17 (Supports modern optimized convolutional operators and activations)
- **Input Tensor Dimensions**: $1 \times 3 \times 416 \times 416$ (Batch size = 1, RGB channels, 416 px resolution)
- **Output Tensor Dimensions**: $1 \times 6 \times 3549$ ($[x, y, w, h, \text{score}_{\text{defect}}, \text{score}_{\text{nodefect}}]$ across 3,549 spatial anchors)
- **Graph Optimization**: `onnx-simplifier` applied to fold redundant constant operations, fuse batch normalization into convolution layers, and prune dead branches.

---

## 3. Theeran's Terminal Execution Log

```bash
theeran@raspberrypi:~/Edge_Computing $ python3 m2/export_onnx.py
=================================================================
         M2 YOLOv8 TO ONNX EXPORT ENGINE         
=================================================================
[*] Input PyTorch Checkpoint : /home/theeran/Edge_Computing/model/best2.pt
[*] Target ONNX File         : /home/theeran/Edge_Computing/m2/model.onnx
[*] Input Tensor Dimensions  : 1 x 3 x 416 x 416
[*] ONNX Opset Version       : 17
[*] Loading YOLOv8 model into memory...
Model summary (fused): 168 layers, 3,006,233 parameters, 0 gradients, 8.1 GFLOPs

[*] Initiating ONNX export with simplification...
Starting export with ONNX 1.16.0, opset 17...
Simplifying with onnxsim 0.4.36...
ONNX export success ✅ 4.79s, saved as 'm2/model.onnx' (11.6 MB)
[+] ONNX export completed in 4.79 seconds.
[+] Model Disk Size  : 11.58 MB
```

---

## 4. Graph Verification & Numerical Parity

Verified using [`../verify_onnx.py`](../verify_onnx.py):

```bash
theeran@raspberrypi:~/Edge_Computing $ python3 m2/verify_onnx.py
=================================================================
      M2 ONNX MODEL INTEGRITY & PARITY VERIFICATION      
=================================================================
[*] Loading ONNX model from: m2/model.onnx
[+] ONNX graph topology successfully validated with onnx.checker.check_model()
[*] Executing ONNX Runtime with synthetic batch=1 input tensor...
[+] Inference completed in 81.70 ms (Throughput: 12.24 FPS)
[*] Computing output difference with PyTorch reference model...
[+] Maximum absolute numerical difference (L-infinity): 4.12e-06 (< 1e-4 threshold)
[+] Numerical parity verified across all 3,549 output anchors.
```

---

## 5. Student Commit Evidence

```text
commit b738192a0149bc2891ecde71029481bcae812901
Author: Theeran <theeran@edge-computing.internal>
Date:   Wed Oct 8 11:15:22 2026 +0530

    feat(m2-theeran): export fine-tuned YOLOv8 model to ONNX with opset 17 and graph simplification
    
    - Target opset 17 with onnxsim constant folding and operator fusion
    - Verified L-inf numerical tolerance (4.12e-06) against PyTorch FP32
    - Output model size: 11.58 MB
```
