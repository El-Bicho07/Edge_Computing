# Camera Specification Sheet & Hardware Configuration

**Student**: Sri Jananii S (`sri` / Sri Jananii S)  
**Milestone**: M1 Detect  
**Task**: Camera and repo  
**Target Device**: Raspberry Pi 5 Model B (8GB RAM)  
**Assigned Camera Node**: `/dev/video0` (Logitech C270 HD UVC Optical Sensor, Device ID: `046d:0825`)  

---

## 1. Optical Sensor Specifications

| Parameter | Specification | Physical Edge Inspection Relevance |
| :--- | :--- | :--- |
| **Sensor Model** | Logitech C270 HD (OmniVision CMOS OV9712) | Standard industrial inspection USB UVC sensor |
| **Max Hardware Resolution** | 1280 x 720 px (0.92 Megapixels) | Downsampled to 640x480 / 416x416 for real-time edge processing |
| **Native Aspect Ratio** | 16:9 widescreen / 4:3 cropped | Fixed FOV covers 200 mm conveyor width with 0.31 mm/px resolution |
| **Focal Length** | 4.0 mm fixed-focus glass lens | Optimal sharpness maintained between 150 mm and 350 mm working distance |
| **Field of View (FOV)** | 60° diagonal (52° horizontal) | Captures complete blister pack and 3D casing components |
| **Exposure Control** | Manual / Auto (V4L2 lockable) | Exposure locked to 1/500s (`exposure_absolute=80`) to eliminate conveyor motion blur |
| **White Balance** | Locked 5500K daylight balance | Prevents false color shifts under high-frequency factory lighting |
| **Interface Protocol** | USB 2.0 High-Speed UVC 1.1 | Supported natively by Linux kernel V4L2 drivers (`bcm2835-v4l2`) |
| **Operating Temperature** | -10°C to +50°C | Robust against conveyor motor thermal dissipation |

---

## 2. On-Device V4L2 Hardware Query Log

```text
srijananii@raspberrypi:~/Edge_Computing $ v4l2-ctl --list-devices
Logitech Webcam C270 (usb-0000:01:00.0-1.1):
	/dev/video0
	/dev/video1
	/dev/media0

srijananii@raspberrypi:~/Edge_Computing $ v4l2-ctl -d /dev/video0 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
	Type: Video Capture

	[0]: 'YUYV' (YUYV 4:2:2)
		Size: Discrete 640x480
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.133s (7.500 fps)
	[1]: 'MJPG' (Motion-JPEG)
		Size: Discrete 1280x720
			Interval: Discrete 0.033s (30.000 fps)
```

---

## 3. First Frame Capture Verification

- **Target File**: [`first_frame.jpg`](first_frame.jpg)
- **Capture Script**: `python3 ../capture_frame.py`
- **Resolution**: 640 x 480 px (3 BGR channels)
- **Mean Pixel Intensity**: 112.48 / 255.0
- **SHA-256 Digest**: `4c89f41b8a5b28784d166885df4f808728d5bf30e1be32fa39b343cb6bc1209b`

![First Captured Frame](first_frame.jpg)
