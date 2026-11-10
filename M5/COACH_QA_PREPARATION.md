# Milestone 5: Coach & Examiner Oral Defense Technical Guide

**Milestone**: M5 Complete System + Dashboard  
**Task**: Live demo and questions  
**Rubric Weight**: Part of 1 Marks  

---

## 1. Overview
During the Milestone 5 evaluation, technical coaches and examiners grill students on architectural choices, trade-offs, edge failure modes, and hardware constraints. This guide provides 15 comprehensive technical questions and bulletproof engineering answers.

---

## 2. 15 Technical Defense Questions & Bulletproof Answers

### Q1: Why did you choose YOLOv8n over two-stage detectors like Faster R-CNN or lightweight models like MobileNet-SSD?
**Answer**: Faster R-CNN relies on a separate Region Proposal Network (RPN), resulting in 150M+ parameters and latency exceeding 600 ms on ARM CPUs—far too slow for our 100 ms conveyor travel budget. MobileNet-SSD v2 is fast (~40 ms) but uses static default anchors that struggle with variable-aspect foil tears and micro-cracks. YOLOv8 utilizes an anchor-free split decoupled head and C2f cross-stage partial bottleneck modules, achieving an optimal sweet spot on Raspberry Pi 5: **87.69% mAP@0.5 at only 3.0M parameters and 60.5 ms INT8 latency**.

---

### Q2: Why did you deploy on-device edge computing instead of streaming camera frames to AWS or Azure?
**Answer**: Cloud streaming introduces three fatal engineering flaws:
1. **Unpredictable Latency**: Network round-trip time (RTT) + TLS handshake introduces 120–350 ms of jitter, breaching our 100 ms mechanical conveyor stop window.
2. **Bandwidth Costs & Outages**: Streaming dual 30 FPS video generates ~18 GB/hour. Any factory Wi-Fi drop halts production.
3. **Data Sovereignty & Privacy**: Pharmaceutical inspection images containing proprietary batch lot codes and tablet formulations must remain on-premises to satisfy FDA and GDPR air-gap regulations.

---

### Q3: How did you ensure you didn't have data leakage in your 70/20/10 dataset split?
**Answer**: Naive random splitting can leak sequential frames of the same physical blister pack across train and test partitions. We enforced two safeguards:
1. **Temporal & Pack Session Isolation**: Images were grouped strictly by physical blister pack serial ID and batch run. All frames of Pack $A$ reside exclusively in Train, while Pack $B$ resides exclusively in Test.
2. **Cryptographic SHA-256 Hash Verification**: We computed SHA-256 binary digests for all 929 image files. As proven by `m1/verify_dataset_split.py`, the set intersection between train, validation, and test hash sets is strictly empty ($\emptyset$), mathematically proving 0.00% leakage.

---

### Q4: When you quantized to INT8, why didn't accuracy drop significantly?
**Answer**: Naive INT8 min-max clipping typically causes 5% to 15% mAP degradation. We preserved 99.1% of our accuracy ($\Delta\text{mAP} = -0.77\%$) by:
1. Calibrating against **100 actual representative blister pack images** covering high-glare foil, empty cavities, and cracked tablets.
2. Using **Kullback-Leibler (KL) divergence minimization** to calculate optimal clipping thresholds $[\alpha_{\min}, \alpha_{\max}]$, discarding outliers while preserving dynamic range in dense activation clusters.
3. Enforcing **per-channel weight quantization** so large weights in one filter don't saturate small gradients in adjacent channels.

---

### Q5: What is your False-Pass Rate, and why is it more important than overall accuracy?
**Answer**: In pharmaceutical packaging, **Accuracy is a deceptive metric**: if 98 out of 100 packs are normal, a dummy model that accepts everything gets 98% accuracy but lets every single defective pack reach consumers. The critical safety metric is the **False-Pass Rate (FPR)**:
$$\text{FPR} = \frac{\text{False Passes (FN)}}{\text{Total Actual Defects}} = \frac{0}{10} = \mathbf{0.0\%}$$
A false reject (stopping a good pack) only costs a 10-second manual re-check, whereas a false pass (shipping a missing pill or punctured seal to an immunocompromised patient) triggers FDA recalls and catastrophic liability.

---

### Q6: How does your spatial slot assignment algorithm work, and what are its geometric failure limits?
**Answer**: We partition detected bounding boxes into a $2 \times 3$ matrix (Pills 1–6) using dynamic centroid clustering (`assign_slots` in `app.py`). It calculates the largest vertical centroid gap to divide Row 0 from Row 1, and derives horizontal column pitch from $\frac{\max(c_x) - \min(c_x)}{2}$.
**Geometric Limits**: If a blister pack enters rotated by more than $15^\circ$ to $20^\circ$, vertical centroid projections overlap, causing row misclassification. To resolve this, we implemented minimum-area bounding box angle estimation (`cv2.minAreaRect`) to digitally re-align the pack prior to slot assignment.

---

### Q7: Why do you need temporal debouncing? Why not actuate on the very first defect detection?
**Answer**: Curved aluminum foil packaging generates transient specular glare spikes as it moves under directional light. In a single frame, a bright glint can mimic a foil tear for 33 ms. If we actuated immediately, we would suffer an 8% false-reject rate. Our temporal debounce filter requires **$N=3$ consecutive frames** to confirm a defect before firing the diverter gate. Since the pack sits under the camera for ~200 ms (6 frames), 3 consecutive frames take only 90 ms—safely inside our 100 ms travel budget while rejecting 100% of single-frame noise spikes.

---

### Q8: What happens if the camera disconnects, freezes, or drops frames?
**Answer**: The system contains a dedicated **Optical Heartbeat Watchdog** (`WatchdogThread`). If no valid frame is ingested within **$500\text{ ms}$**, the system engages a deterministic **Fail-Safe Mode**:
1. It immediately de-energizes the conveyor motor relay (`GPIO 14`, Normally-Open logic), stopping belt motion in $< 12\text{ ms}$.
2. The SG90 reject diverter falls back to the closed reject chute position via gravitational return.
3. Amber alarm strobe illuminates and a critical alert is broadcast via MQTT and Modbus.
4. The system locks out automatic restart until a technician physically acknowledges the fault.

---

### Q9: Why did you couple an MPU6050 vibration sensor with optical vision?
**Answer**: Optical inspection is strictly reactive: it detects defects after they have already been manufactured. The MPU6050 vibration sensor provides **proactive condition monitoring**: it detects drive motor bearing degradation, belt slip, and mechanical unbalance (such as 85 Hz harmonics) hours or days *before* mechanical failure ruins thousands of blister packs.

---

### Q10: How did you train the vibration anomaly model without having months of recorded failure data?
**Answer**: We used an **unsupervised One-Class Statistical Anomaly Envelope** trained **strictly and exclusively on baseline normal data** (`normal_run_1..3.csv`). We extracted a 5D feature space (RMS acceleration, standard deviation, peak-to-peak shock, gyro velocity, FFT spectral energy) and calibrated an alert threshold at the **3.5-sigma upper tail ($\tau = 4.285$)**. Normal runs hover at $0.7 \dots 1.2$, while mechanical fault injection surges past $89.0$, giving instant alerts with zero false alarms.

---

### Q11: How do you prevent thread lockups when Flask, YOLO, and SQLite run simultaneously?
**Answer**: In our 10-minute endurance test, default SQLite rollback journaling crashed with `database is locked`. We solved this by enabling **Write-Ahead Logging (WAL)**:
`PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;`
WAL mode separates reads from writes so Flask dashboard queries never block the 16 Hz YOLO detection worker. Additionally, routine conveyor telemetry is queued in-memory and flushed in atomic 50-row batch transactions every 5 seconds.

---

### Q12: Why did your SG90 servo motor jitter during early runs, and how did you fix it?
**Answer**: Linux is a general-purpose operating system without hard real-time kernel guarantees. Under 60% CPU load, software-timed PWM on GPIO pins suffers from microsecond timer jitter, causing the servo to twitch and draw 800 mA stall current. We fixed this by migrating to **Hardware PWM on GPIO 18** and implementing **PWM pulse detachment**: after commanding $0^\circ$ or $90^\circ$, we wait 350 ms for the arm to reach mechanical position, then shut off the PWM signal entirely (`servo.detach()`). Gear friction holds the gate in place with zero current draw and zero jitter.

---

### Q13: What security measures did you implement for factory network integration?
**Answer**: Following IEC 62443, we applied two core mitigations:
1. **Network Level (Level 3)**: Closed plaintext MQTT port 1883. Implemented **Mutual TLS 1.3 on port 8883** with 256-bit AES-GCM encryption and x509 CA certificate verification, setting `allow_anonymous false` with PBKDF2 password hashes.
2. **Device Level (Level 2)**: Containerized the application in Docker with minimal non-root capabilities and mapped only necessary hardware nodes (`/dev/video0`, `/dev/gpiomem`).

---

### Q14: How does your OTA update system prevent "bricking" the edge inspection station?
**Answer**: We implemented an **A/B staging partition update strategy** in `m4/ota_manager.py`. When version 2 is downloaded:
1. The active stable version (v1) is backed up.
2. The new package is installed to an isolated shadow staging slot.
3. The system executes a **pre-flight self-test**: tests camera frame grab, runs forward tensor pass, and checks GPIO state.
4. If *any* pre-flight test fails, the manager **aborts immediately and rolls back to v1** in $< 300\text{ ms}$ with zero downtime.

---

### Q15: What is your total End-to-End latency, and how does it compare to your physical conveyor travel time?
**Answer**: Our median End-to-End Latency ($T_{\text{E2E}}$) across 25 measured events is **$59.93\text{ ms}$** (Capture: 13.9 ms, Preprocessing: 4.1 ms, Quantized Inference: 40.1 ms, Decision: 1.5 ms, GPIO pin latching: 0.5 ms), with a 95th percentile of **$64.54\text{ ms}$**.
Our conveyor travels at $120\text{ mm/s}$, and the optical station to reject diverter distance is $120\text{ mm}$, providing a physical travel window of $1,000\text{ ms}$. Our $65\text{ ms}$ response time leaves a massive safety margin of over $930\text{ ms}$, guaranteeing that the reject diverter gate is fully open long before the defective pack reaches it.
