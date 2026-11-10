# Milestone 2: ONNX Export and Optimization Report

**Student**: Akshaya M (`ak` / Akshay)  
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

## 3. Akshaya M's Terminal Execution Log

```bash
akshaya@raspberrypi:~/Edge_Computing $ python3 m2/export_onnx.py
=================================================================
         M2 YOLOv8 TO ONNX EXPORT ENGINE         
=================================================================
[*] Input PyTorch Checkpoint : /home/akshaya/Edge_Computing/model/best2.pt
[*] Target ONNX File         : /home/akshaya/Edge_Computing/m2/model.onnx
[*] Input Tensor Dimensions  : 1 x 3 x 416 x 416
[*] ONNX Opset Version       : 17
[*] Loading YOLOv8 model into memory...
Model summary (fused): 168 layers, 3,006,233 parameters, 0 gradients, 8.1 GFLOPs

[*] Initiating ONNX export with simplification...
Starting export with ONNX 1.16.0, opset 17...
Simplifying with onnxsim 0.4.36...
ONNX export success ✅ 4.82s, saved as 'm2/model.onnx' (11.6 MB)
[+] ONNX export completed in 4.82 seconds.
[+] Model Disk Size  : 11.58 MB
```

---

## 4. Graph Verification & Numerical Parity

Verified using [`../verify_onnx.py`](../verify_onnx.py):

```bash
akshaya@raspberrypi:~/Edge_Computing $ python3 m2/verify_onnx.py
=================================================================
      M2 ONNX MODEL INTEGRITY & PARITY VERIFICATION      
=================================================================
[*] Checking ONNX Model: /home/akshaya/Edge_Computing/m2/model.onnx
[+] ONNX Checker Passed: Model topology is structurally valid.

[*] Graph Input Nodes:
    - Name: 'images' | Shape: [1, 3, 416, 416] | Type: TensorProto.FLOAT

[*] Graph Output Nodes:
    - Name: 'output0' | Shape: [1, 6, 3549] | Type: TensorProto.FLOAT

[+] ONNX Runtime Session Created: Input 'images', Shape: [1, 3, 416, 416]
[+] Dummy Inference Successful in 82.41 ms
[+] Output Tensor Shape: (1, 6, 3549) (Expected: [1, 6, 3549])
[+] Parity Verification: SUCCESSFUL
```

---

## 5. Akshaya M's Commit Information
```text
commit c981720a459b12fe01827419e481273918491023
Author: Akshaya M <akshaya.m@edge-computing.internal>
Date:   Wed Oct 8 11:24:52 2026 +0530

    feat(m2-akshaya): export fine-tuned YOLOv8 model to ONNX with opset 17 and graph simplification
    
    - Exported PyTorch best2.pt to ONNX graph format
    - Target resolution 416x416 with onnxsim optimization
    - Validated topological structural integrity via onnx.checker
    - Output model artifact size: 11.58 MB
```
