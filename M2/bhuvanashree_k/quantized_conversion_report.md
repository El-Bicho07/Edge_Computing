# Milestone 2: Quantized Model Conversion and Live Edge Deployment

**Student**: Bhuvanashree K (`b` / Vamsi)  
**Milestone**: M2 Optimize  
**Task**: Convert and run live  
**Rubric Weight**: 4 Marks  

---

## 1. Requirement Summary
> *"I convert to TFLite INT8 or TensorRT and run it live on the device"*

---

## 2. INT8 Post-Training Quantization Engine
The conversion pipeline implemented in [`../convert_tflite_int8.py`](../convert_tflite_int8.py) executes 8-bit integer post-training quantization (PTQ) with dynamic calibration.

### Technical Parameters:
- **Optimization Target**: TensorFlow Lite INT8 with full integer arithmetic.
- **Calibration Source**: 100 representative blister pack inspection images.
- **Input / Output Types**: `tf.int8` with zero-point offset ($z$) and quantization scale factor ($S$):
  $$q = \text{round}\left(\frac{r}{S}\right) + z$$
- **Hardware Acceleration**: ARM NEON INT8 matrix engine executing on Broadcom BCM2712 Cortex-A76 cores.
- **Model Footprint**: Reduced from 11.58 MB down to **3.24 MB** (72% storage reduction).

---

## 3. Bhuvanashree K's Live Execution Log on Raspberry Pi 5

```bash
bhuvanashree@raspberrypi:~/Edge_Computing $ python3 m2/run_quantized_live.py --model m2/model_int8.tflite --source 0
=================================================================
       M2 LIVE QUANTIZED EDGE INFERENCE ENGINE (TFLITE INT8)     
=================================================================
[*] Loading Quantized Model: m2/model_int8.tflite
[+] TFLite Interpreter Allocated successfully with XNNPACK Delegate.
[*] Input Tensor  : 'serving_default_images:0' | Shape: [1, 416, 416, 3] | Type: INT8
[*] Output Tensor : 'StatefulPartitionedCall:0' | Shape: [1, 6, 3549] | Type: INT8
[*] Opening optical hardware video stream: /dev/video0...
[+] Camera operational at 640x480. Beginning edge inference loop.

[Frame 001] Latency: 59.8 ms | FPS: 16.72 | Detections: 1 defect (0.86)
[Frame 002] Latency: 60.1 ms | FPS: 16.64 | Detections: 1 no defect (0.92)
[Frame 003] Latency: 59.7 ms | FPS: 16.75 | Detections: 1 defect (0.88)
...
[+] Sustained Average Latency: 59.9 ms | Sustained FPS: 16.69 FPS
```
