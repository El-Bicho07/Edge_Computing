# Milestone 4: Industrial Edge Threat Model (Purdue Model & STRIDE)

**Milestone**: M4 Monitor and Connect  
**Task**: Threat model  
**Rubric Weight**: 1 Marks  

---

## 1. Requirement Summary
> *"I show one threat per level and 2 mitigations applied"*

---

## 2. 4-Level Industrial Threat Matrix (Purdue Model)

In alignment with IEC 62443 industrial cybersecurity standards, threats are identified across all four functional tiers of the Purdue Enterprise Reference Architecture:

| Purdue Tier | Level Name | Operational Assets | Identified Cyber-Physical Threat | STRIDE Classification | Impact / Risk Severity |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Level 0 / 1** | **Physical Process & Sensing** | Optical Camera, IR Proximity Sensor, SG90 Servo, MPU6050 I2C | **Sensor Line Tampering / Hardware Spoofing**: Attacker physically disconnects or ties IR sensor to logic HIGH, blinding the system so defective packs pass uninspected. | **Tampering** | **CRITICAL**: Defective pharmaceuticals bypass inspection undetected. |
| **Level 2** | **Edge Control Station** | Raspberry Pi 5, Linux OS, Docker Runtime, SQLite Database | **Unauthorized Local Privilege Escalation & DB Tampering**: Local USB attack injecting malicious firmware or altering `data/inspection.db` records to hide manufacturing defects. | **Elevation of Privilege / Repudiation** | **HIGH**: Compromises regulatory compliance (21 CFR Part 11 audit trails). |
| **Level 3** | **Operations & Factory LAN** | Modbus TCP (Port 502), MQTT Broker, SCADA Supervisors | **Man-in-the-Middle (MitM) Eavesdropping & Packet Injection**: Eavesdropper intercepts unencrypted MQTT telemetry or sends forged `CONVEYOR_HALT_CMD` packets to halt production. | **Information Disclosure / Tampering** | **HIGH**: Operational downtime, loss of production telemetry confidentiality. |
| **Level 4** | **Enterprise & Cloud Link** | REST APIs, ERP/MES Interfaces, Remote OTA Update Server | **Compromised Update Payload / Supply Chain Attack**: Attacker hijacks OTA update server to push malicious neural weights or backdoored firmware to fleet of edge devices. | **Spoofing / Tampering** | **CRITICAL**: Remote hostile takeover of industrial machinery. |

---

## 3. Two Concrete Mitigations Actively Applied in Code

### Mitigation 1: Mutual TLS v1.3 with Certificate Authority Verification (Level 3 Applied)
- **Problem**: Plaintext MQTT/Modbus enables network sniffing and packet replay.
- **Implemented Mitigation**:
  1. Configured Mosquitto broker with `allow_anonymous false` and enforced TLS v1.3 encryption on port 8883 in [`m4/mqtt/mosquitto.conf`](../mqtt/mosquitto.conf).
  2. Integrated x509 root certificate verification (`ca.crt`) and PBKDF2 credential hashing in [`m4/test_secure_mqtt.py`](../test_secure_mqtt.py).
  3. All inspection verdicts and motor health scores are encrypted using 256-bit AES-GCM, preventing unauthorized eavesdropping or command injection on the factory LAN.

### Mitigation 2: Dual Hardware Watchdog & Fail-Safe State Lockout (Level 0/1 & 2 Applied)
- **Problem**: Physical sensor tampering or software hanging could allow defective items to clear.
- **Implemented Mitigation**:
  1. Programmed an independent optical heartbeat watchdog thread in [`m3/decision_engine.py`](../../M3/decision_engine.py) monitoring frame inter-arrival time ($\Delta t$).
  2. If $\Delta t > 500\text{ ms}$, the system automatically cuts power to the conveyor motor solid-state relay (`GPIO 14`, Normally-Open logic) and locks all actuators into a safe shutdown state.
  3. Conveyor cannot resume until physical reset button (`GPIO 16`) or authenticated dashboard operator command clears the latch.
