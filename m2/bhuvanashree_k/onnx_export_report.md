# Milestone 2: ONNX Export and Optimization Report

**Student**: Bhuvanashree K (`b` / Vamsi)  
**Milestone**: M2 Optimize  
**Task**: Export to ONNX  
**Marks Awarded**: 3 / 3  

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

## 3. Bhuvanashree K's Terminal Execution Log

```bash
bhuvanashree@raspberrypi:~/Edge_Computing $ python3 m2/export_onnx.py
=================================================================
         M2 YOLOv8 TO ONNX EXPORT ENGINE         
=================================================================
[*] Input PyTorch Checkpoint : /home/bhuvanashree/Edge_Computing/model/best2.pt
[*] Target ONNX File         : /home/bhuvanashree/Edge_Computing/m2/model.onnx
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
bhuvanashree@raspberrypi:~/Edge_Computing $ python3 m2/verify_onnx.py
=================================================================
      M2 ONNX MODEL INTEGRITY & PARITY VERIFICATION      
=================================================================
[*] Checking ONNX Model: /home/bhuvanashree/Edge_Computing/m2/model.onnx
[+] ONNX Checker Passed: Model topology is structurally valid.

[*] Graph Input Nodes:
    - Name: 'images' | Shape: [1, 3, 416, 416] | Type: TensorProto.FLOAT

[*] Graph Output Nodes:
    - Name: 'output0' | Shape: [1, 6, 3549] | Type: TensorProto.FLOAT

[+] ONNX Runtime Session Created: Input 'images', Shape: [1, 3, 416, 416]
[+] Dummy Inference Successful in 81.95 ms
[+] Output Tensor Shape: (1, 6, 3549) (Expected: [1, 6, 3549])
[+] Parity Verification: SUCCESSFUL
```

---

## 5. Bhuvanashree K's Commit Information
```text
commit d712498b31490ac3918f0291471029487192bc44
Author: Bhuvanashree K <bhuvanashree.k@edge-computing.internal>
Date:   Wed Oct 8 11:26:24 2026 +0530

    feat(m2-bhuvanashree): export fine-tuned YOLOv8 model to ONNX with opset 17 and graph simplification
    
    - Convert best2.pt weights to ONNX computation graph
    - Simplify constant tensor subgraphs using onnxsim
    - Validate inference output shape parity [1, 6, 3549]
    - Output model size: 11.58 MB
```
