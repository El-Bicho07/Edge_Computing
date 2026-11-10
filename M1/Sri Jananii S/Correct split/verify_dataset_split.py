#!/usr/bin/env python3
"""
Milestone 1: Dataset Split Verification and Leakage Detection Engine
Veyra Pharma Vision Edge System

Verifies:
1. Exact Train / Validation / Test image counts and percentage distribution
2. Class balance across splits
3. Cryptographic SHA-256 cross-split image duplication check (Zero Data Leakage proof)
4. Evaluation of the standard 70/20/10 industrial split
"""

import os
import glob
import hashlib
from collections import Counter

def compute_file_hash(filepath):
    """Computes SHA-256 digest of an image file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify_dataset_partitions():
    base_dir = os.path.dirname(__file__)
    dataset_root = os.path.join(base_dir, "..", "dataset", "Defect Detection.v1i.yolov8")

    splits = ["train", "valid", "test"]
    split_data = {}
    all_hashes = {}

    print("\n" + "="*70)
    print("      M1 DATASET SPLIT VERIFICATION & ZERO LEAKAGE AUDIT       ")
    print("="*70)
    print(f"[*] Dataset Directory: {os.path.abspath(dataset_root)}")

    total_images = 0
    for split in splits:
        img_dir = os.path.join(dataset_root, split, "images")
        lbl_dir = os.path.join(dataset_root, split, "labels")

        images = glob.glob(os.path.join(img_dir, "*.jpg")) + glob.glob(os.path.join(img_dir, "*.png"))
        labels = glob.glob(os.path.join(lbl_dir, "*.txt"))

        # Read class labels
        class_counts = Counter()
        hashes = {}
        for img_path in images:
            fhash = compute_file_hash(img_path)
            fname = os.path.basename(img_path)
            hashes[fname] = fhash
            all_hashes[(split, fname)] = fhash

            # Corresponding label
            lbl_name = os.path.splitext(fname)[0] + ".txt"
            lbl_path = os.path.join(lbl_dir, lbl_name)
            if os.path.exists(lbl_path):
                with open(lbl_path, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if parts:
                            class_counts[int(parts[0])] += 1

        split_data[split] = {
            "image_count": len(images),
            "label_count": len(labels),
            "classes": class_counts,
            "hashes": hashes
        }
        total_images += len(images)

    print(f"[+] Total Images Discovered: {total_images}")
    print("\n" + "-"*70)
    print(f"{'Split':<12} | {'Images':<8} | {'Ratio (%)':<10} | {'Defect (0)':<12} | {'No Defect (1)':<14}")
    print("-" * 70)

    for split in splits:
        d = split_data[split]
        count = d["image_count"]
        pct = (count / max(total_images, 1)) * 100.0
        c0 = d["classes"][0]
        c1 = d["classes"][1]
        print(f"{split.capitalize():<12} | {count:<8} | {pct:>8.2f}% | {c0:<12} | {c1:<14}")
    print("-" * 70)

    # Cross-Split Leakage Audit
    print("\n[*] Conducting Cryptographic Cross-Split Data Leakage Audit...")
    train_hashes = set(split_data["train"]["hashes"].values())
    val_hashes = set(split_data["valid"]["hashes"].values())
    test_hashes = set(split_data["test"]["hashes"].values())

    train_val_overlap = train_hashes.intersection(val_hashes)
    train_test_overlap = train_hashes.intersection(test_hashes)
    val_test_overlap = val_hashes.intersection(test_hashes)

    leakage_detected = len(train_val_overlap) + len(train_test_overlap) + len(val_test_overlap)

    print(f"    - Overlap (Train <-> Validation) : {len(train_val_overlap)} duplicate image files")
    print(f"    - Overlap (Train <-> Test)       : {len(train_test_overlap)} duplicate image files")
    print(f"    - Overlap (Validation <-> Test)  : {len(val_test_overlap)} duplicate image files")

    if leakage_detected == 0:
        print("[+] ZERO DATA LEAKAGE CONFIRMED: All partitions are strictly mathematically disjoint.")
    else:
        print(f"[!] WARNING: {leakage_detected} duplicate image files detected across partitions!")

    # 70/20/10 Partition Formulation
    print("\n[*] Target 70/20/10 Split Calibration:")
    t70 = int(round(total_images * 0.70))
    v20 = int(round(total_images * 0.20))
    t10 = total_images - t70 - v20
    print(f"    - 70% Train Target : {t70} images ({t70/total_images*100:.1f}%)")
    print(f"    - 20% Valid Target : {v20} images ({v20/total_images*100:.1f}%)")
    print(f"    - 10% Test Target  : {t10} images ({t10/total_images*100:.1f}%)")
    print("="*70 + "\n")

    return {
        "total_images": total_images,
        "splits": split_data,
        "leakage_count": leakage_detected
    }

if __name__ == "__main__":
    verify_dataset_partitions()
