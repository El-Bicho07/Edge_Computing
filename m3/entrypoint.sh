#!/bin/bash
set -e

echo "================================================================="
echo "   VEYRA PHARMA VISION: COLD BOOT CONTAINER INITIALIZATION       "
echo "================================================================="
echo "[*] System Time   : $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "[*] Architecture  : $(uname -m)"
echo "[*] Host Device   : Raspberry Pi 5 Edge Station"

# Phase 1: Hardware peripheral detection
echo "[*] Step 1: Checking V4L2 optical device nodes..."
if [ -e /dev/video0 ]; then
    echo "[+] Found /dev/video0 optical capture node."
else
    echo "[!] /dev/video0 not mapped. Enabling fallback edge simulation mode."
    export MOCK_HARDWARE=1
fi

echo "[*] Step 2: Checking GPIO peripheral access (/dev/gpiomem)..."
if [ -e /dev/gpiomem ]; then
    echo "[+] /dev/gpiomem detected. Hardware GPIO actuation enabled."
else
    echo "[!] /dev/gpiomem unavailable. Sttubbing GPIO with hardware mock layer."
    export MOCK_HARDWARE=1
fi

# Phase 2: Actuator Self-Test on Cold Boot
echo "[*] Step 3: Executing cold-boot hardware actuator self-test..."
python3 -c "
import time, os
from m3.actuator_controller import ActuatorController
print('[COLD BOOT] Cycling conveyor relay and SG90 servo...')
act = ActuatorController()
act.actuate_reject_gate(True)
time.sleep(0.3)
act.actuate_reject_gate(False)
act.illuminate_defect_slot(0)
time.sleep(0.2)
act.clear_all_leds()
act.cleanup()
print('[COLD BOOT] Actuator self-test successfully fired.')
"

# Phase 3: Launch Core Edge Service
echo "[*] Step 4: Launching Veyra Pharma Vision Inspection Dashboard..."
exec python3 app.py
