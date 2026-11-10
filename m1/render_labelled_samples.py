#!/usr/bin/env python3
"""
Milestone 1: Render Tight Labelled Bounding Box Samples
Veyra Pharma Vision Edge System

Reads YOLOv8 format annotations (.txt) and renders tight, high-contrast
bounding boxes on blister pack test images for visual proof.
"""

import os
import glob
import cv2

CLASS_COLORS = {
    0: (0, 0, 255),    # Red for defect
    1: (0, 255, 0),    # Green for no defect (pass)
}

CLASS_NAMES = {
    0: "defect",
    1: "no defect"
}

def render_bounding_boxes():
    base_dir = os.path.dirname(__file__)
    dataset_dir = os.path.join(base_dir, "..", "dataset", "Defect Detection.v1i.yolov8", "test")
    img_dir = os.path.join(dataset_dir, "images")
    lbl_dir = os.path.join(dataset_dir, "labels")
    out_dir = os.path.join(base_dir, "labelled_samples")
    os.makedirs(out_dir, exist_ok=True)

    images = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))
    print(f"[*] Found {len(images)} images in test set. Rendering sample labelled proofs...")

    rendered_count = 0
    for img_path in images[:10]: # Render first 10 representative test samples
        filename = os.path.basename(img_path)
        label_filename = os.path.splitext(filename)[0] + ".txt"
        lbl_path = os.path.join(lbl_dir, label_filename)

        img = cv2.imread(img_path)
        if img is None:
            continue
        h, w, _ = img.shape

        if os.path.exists(lbl_path):
            with open(lbl_path, "r") as f:
                lines = f.readlines()

            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    cls_id = int(parts[0])
                    xc, yc, bw, bh = [float(x) for x in parts[1:5]]
                    
                    # Convert normalized center-width-height to pixel corners
                    x1 = int((xc - bw / 2.0) * w)
                    y1 = int((yc - bh / 2.0) * h)
                    x2 = int((xc + bw / 2.0) * w)
                    y2 = int((yc + bh / 2.0) * h)

                    color = CLASS_COLORS.get(cls_id, (255, 255, 0))
                    name = CLASS_NAMES.get(cls_id, f"Class {cls_id}")

                    # Draw tight bounding box
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                    
                    # Label text badge
                    badge_text = f"{name}"
                    (tw, th), _ = cv2.getTextSize(badge_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(img, (x1, max(0, y1 - 20)), (x1 + tw + 6, max(20, y1)), color, -1)
                    cv2.putText(img, badge_text, (x1 + 3, max(14, y1 - 4)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)

        # Add title header
        cv2.putText(img, f"M1 DATASET v1 TIGHT BOX VERIFICATION: {filename[:28]}...",
                    (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        out_path = os.path.join(out_dir, f"labelled_{filename}")
        cv2.imwrite(out_path, img)
        rendered_count += 1

    print(f"[+] Successfully rendered {rendered_count} labelled images into: {out_dir}")

if __name__ == "__main__":
    render_bounding_boxes()
