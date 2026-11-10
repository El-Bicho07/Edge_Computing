#!/usr/bin/env python3
"""
Milestone 4: Unsupervised Vibration Anomaly Model Training
Veyra Pharma Vision Edge System

Trains an Isolation Forest / One-Class Statistical Anomaly Model
STRICTLY on normal vibration data runs (normal_run_1..3.csv).
Zero fault data is seen during training.
"""

import os
import sys
import glob
import csv
import json
import numpy as np

def extract_features_from_csv(csv_path):
    """Computes statistical and frequency domain features over windows."""
    ax, ay, az = [], [], []
    gx, gy, gz = [], [], []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ax.append(float(row["accel_x_g"]))
            ay.append(float(row["accel_y_g"]))
            az.append(float(row["accel_z_g"]))
            gx.append(float(row["gyro_x_dps"]))
            gy.append(float(row["gyro_y_dps"]))
            gz.append(float(row["gyro_z_dps"]))

    # Feature engineering over 50-sample windows (~1.0s window)
    window_size = 50
    step = 25
    features = []

    for i in range(0, len(ax) - window_size + 1, step):
        w_ax = np.array(ax[i:i+window_size])
        w_ay = np.array(ay[i:i+window_size])
        w_az = np.array(az[i:i+window_size])
        w_gx = np.array(gx[i:i+window_size])
        w_gy = np.array(gy[i:i+window_size])

        # 1. Total Acceleration Vector Magnitude (RMS)
        amag = np.sqrt(w_ax**2 + w_ay**2 + w_az**2)
        rms_accel = np.sqrt(np.mean(amag**2))
        std_accel = np.std(amag)
        peak_to_peak = np.ptp(amag)

        # 2. Gyroscope RMS Velocity
        gmag = np.sqrt(w_gx**2 + w_gy**2)
        rms_gyro = np.sqrt(np.mean(gmag**2))

        # 3. Spectral Energy
        fft_energy = float(np.sum(np.abs(np.fft.rfft(amag))**2) / window_size)

        features.append([rms_accel, std_accel, peak_to_peak, rms_gyro, fft_energy])

    return np.array(features)

def train_anomaly_model():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "data")
    model_meta_path = os.path.join(base_dir, "anomaly_model_meta.json")

    print("\n" + "="*70)
    print("      M4 MOTOR VIBRATION ANOMALY MODEL TRAINING (NORMAL ONLY)      ")
    print("="*70)

    normal_files = [os.path.join(data_dir, f"normal_run_{i}.csv") for i in range(1, 4)]
    print("[*] Ingesting Normal Training Runs (Zero Fault Exposure):")
    for nf in normal_files:
        print(f"    - {os.path.basename(nf)}")

    all_normal_features = []
    for nf in normal_files:
        feats = extract_features_from_csv(nf)
        all_normal_features.append(feats)

    X_train = np.vstack(all_normal_features)
    print(f"[+] Total Normal Training Feature Vectors: {X_train.shape[0]} windows (5 features each)")

    # Compute Feature Mean and Standard Deviation (Z-score normalization)
    mu = np.mean(X_train, axis=0)
    sigma = np.std(X_train, axis=0) + 1e-6
    X_train_norm = (X_train - mu) / sigma

    # Statistical Mahalanobis / Euclidean Distance Baseline
    train_scores = np.sqrt(np.sum(X_train_norm**2, axis=1))
    max_train_score = float(np.max(train_scores))
    p99_train_score = float(np.percentile(train_scores, 99))

    # Anomaly Decision Threshold: Mean + 3.5 * Std (Extreme Value Theory)
    threshold = float(np.mean(train_scores) + 3.5 * np.std(train_scores))

    print("\n[*] Training Baseline Statistics:")
    print(f"    - Mean Training Score       : {np.mean(train_scores):.4f}")
    print(f"    - 99th Percentile Score     : {p99_train_score:.4f}")
    print(f"    - Maximum Normal Score      : {max_train_score:.4f}")
    print(f"    - Calibrated Alert Cutoff   : {threshold:.4f} (3.5-Sigma Boundary)")

    # Save model metadata
    model_params = {
        "model_type": "Statistical Mahalanobis Envelope / Isolation Metric",
        "trained_on": "Normal baseline runs 1, 2, 3 only",
        "num_training_samples": int(X_train.shape[0]),
        "feature_names": ["rms_accel", "std_accel", "peak_to_peak", "rms_gyro", "fft_energy"],
        "mean_vector": mu.tolist(),
        "std_vector": sigma.tolist(),
        "alert_threshold": round(threshold, 4),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    with open(model_meta_path, "w") as f:
        json.dump(model_params, f, indent=2)

    print(f"\n[+] Anomaly Model Parameters saved to: {model_meta_path}")
    print("="*70 + "\n")
    return model_params

if __name__ == "__main__":
    train_anomaly_model()
