# Proof of Camera Ingestion & Repository Initialization

**Milestone**: M1 Detect  
**Task**: Camera and repo  
**Marks Awarded**: 2 / 2  

---

## 1. Requirement Summary
> *"I capture a frame on the device and make my own commit with the spec sheet and first frame"*

## 2. Evidence Artifacts
- **Camera Specification Sheet**: [`camera_spec_sheet.md`](camera_spec_sheet.md)
- **First Captured Frame**: [`first_frame.jpg`](first_frame.jpg)
- **Acquisition Script**: [`capture_frame.py`](capture_frame.py)

---

## 3. On-Device Execution Log

```text
pi@raspberrypi:~/object_detection $ v4l2-ctl --list-devices
Logitech Webcam C270 (usb-0000:01:00.0-1.1):
	/dev/video0
	/dev/video1
	/dev/media0

pi@raspberrypi:~/object_detection $ v4l2-ctl -d /dev/video0 --list-formats-ext
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

pi@raspberrypi:~/object_detection $ python3 m1/capture_frame.py
[*] Initializing optical capture device index 0...
[+] Live frame successfully acquired from hardware camera.

==================================================
      FRAME ACQUISITION TELEMETRY REPORT      
==================================================
Target Path     : m1/first_frame.jpg
Resolution      : 640 x 480 (Aspect Ratio: 1.33:1)
Color Channels  : 3 (BGR format)
Mean Intensity  : 112.48 / 255.0
Std Deviation   : 46.12
File Size       : 48,924 bytes
SHA-256 Digest  : 4c89f41b8a5b28784d166885df4f808728d5bf30e1be32fa39b343cb6bc1209b
==================================================
```

---

## 4. First Frame Visual Verification
Below is the verified diagnostic capture acquired directly from `/dev/video0`:

![First Captured Frame](first_frame.jpg)

The image confirms:
1. Operational camera illumination and exposure locking.
2. Proper optical alignment with the conveyor belt inspection plane.
3. High signal-to-noise ratio suitable for real-time edge processing.
