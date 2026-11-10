# syntax=docker/dockerfile:1
# Milestone 3: Production Edge Container for Veyra Pharma Vision
# Target Platform: linux/arm64 (Raspberry Pi 5)

FROM python:3.11-slim-bookworm

LABEL maintainer="Veyra Edge AI Team <team5@veyravision.internal>"
LABEL description="Edge AI Blister Pack Defect Detection & Conveyor Actuator Service"
LABEL milestone="M3 Decide and Act"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MOCK_HARDWARE=0

WORKDIR /app

# Install system dependencies (V4L2, OpenCV runtime, GPIO headers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    v4l-utils \
    libgpiod2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY working-packages.txt /app/
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir \
    ultralytics==8.4.174 \
    opencv-python-headless==4.10.0.84 \
    Flask==3.1.3 \
    gpiozero==2.0.1 \
    numpy==2.2.4 \
    pillow==11.1.0 \
    paho-mqtt==2.1.0 \
    pymodbus==3.6.8

# Copy application and milestone code
COPY . /app/

# Ensure entrypoint is executable
RUN chmod +x /app/m3/entrypoint.sh

EXPOSE 5000 1883 502

HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

ENTRYPOINT ["/app/m3/entrypoint.sh"]
