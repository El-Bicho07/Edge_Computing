# Milestone 1: Hardware & Camera Specification Sheet

## 1. System Overview
The edge vision system is deployed on an industrial Raspberry Pi 5 single-board computer coupled with a fixed-focus Logitech C270 HD optical imaging unit to perform automated quality inspection on pharmaceutical blister packs.

---

## 2. Camera Module Specifications

| Specification | Technical Detail | Operational Note |
| :--- | :--- | :--- |
| **Model** | Logitech C270 HD Webcam | Commercial USB Optical Sensor |
| **Interface** | USB 2.0 (High Speed, 480 Mbps) | Bus-powered directly from Pi 5 USB 3.0 port |
| **Linux V4L2 Device Node** | `/dev/video0` (Stream), `/dev/video1` (Metadata) | Native UVC Video Driver (`uvcvideo`) |
| **Sensor Type** | 1/4" Color CMOS Optical Sensor | Anti-reflective coated glass lens |
| **Native Resolution** | 1280 $\times$ 720 pixels (720p HD) | Native 16:9 widescreen aspect ratio |
| **Inspection Resolution** | 640 $\times$ 480 (VGA) / 416 $\times$ 416 (Inference) | Scaled via OpenCV hardware acceleration |
| **Pixel Format / Chroma** | YUYV 4:2:2 / MJPEG | Captured as YUYV, converted to BGR via OpenCV |
| **Max Frame Rate** | 30 FPS @ 720p, 30 FPS @ 640x480 | Monitored with zero dropped frames on RPi 5 |
| **Field of View (FOV)** | 60° (Diagonal) / ~52° (Horizontal) | Covers full 120 mm $\times$ 60 mm conveyor FOV |
| **Focal Length** | 4.0 mm (Fixed Focus) | Factory calibrated hyperfocal distance: 180 mm |
| **Aperture** | $f/2.0$ | Fixed aperture for consistent depth-of-field |
| **Exposure Control** | Automatic / Manual via V4L2-ctl | Locked to `exposure_absolute=156` to avoid motion blur |
| **White Balance** | Locked at 4500K daylight | Eliminates color shifts across shifts |
| **Power Consumption** | 5V DC @ ~120 mA (0.6 W) | Low thermal footprint |

---

## 3. Edge Compute Host Platform Specifications

| Component | Technical Detail | Role in Pipeline |
| :--- | :--- | :--- |
| **Board Model** | Raspberry Pi 5 Model B Rev 1.1 | Edge compute host |
| **Processor (SoC)** | Broadcom BCM2712 (16nm process) | Primary execution engine |
| **CPU Architecture** | Quad-Core ARM Cortex-A76 @ 2.4 GHz | 64-bit ARMv8.2-A with ARM NEON SIMD |
| **CPU Cache** | 512 KB L2 cache per core; 2 MB shared L3 | Accelerates deep learning tensor operations |
| **GPU** | Broadcom VideoCore VII @ 800 MHz | Vulkan 1.2, OpenGL ES 3.1 rendering |
| **System Memory (RAM)** | 8 GB LPDDR4X-4267 SDRAM | High-bandwidth unified memory architecture |
| **Storage Subsystem** | 64 GB SanDisk Extreme MicroSDXC (A2, V30) | Host OS, SQLite WAL DB, local datasets |
| **Operating System** | Linux raspberrypi 6.6.20+rpt-rpi-2712 #1 SMP | Debian 12 (Bookworm) 64-bit `aarch64` |
| **I/O Subsystems** | 40-pin GPIO header, I2C1 (Pin 3/5), PWM (Pin 12) | Actuator relay, MPU6050, SG90 servo, LEDs |
| **Thermal Solution** | Active Aluminum Heatsink + PWM Blower Fan | Sustained 2.4 GHz clock under 58°C full load |
| **Power Supply** | Official 27W USB-C PD (5.1V / 5.0A) | Prevents undervoltage throttling during inference |

---

## 4. Hardware Verification & Proof of Acquisition
The camera was verified on device `/dev/video0` using `v4l2-ctl --list-formats-ext`. The first captured frame (`first_frame.jpg`) was acquired on-device, establishing the optical baseline for all downstream detection and telemetry pipelines.
