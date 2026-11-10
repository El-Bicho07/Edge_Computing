# Milestone 1: Dataset v1 Data Card

## 1. Dataset Summary & Metadata
- **Dataset Name**: Veyra Pharma Blister Pack Defect Dataset (v1.0)
- **Primary Domain**: Industrial Edge Vision / Automated Optical Inspection (AOI)
- **Target Application**: Pharmaceutical quality control on automated packaging conveyors
- **Total Images**: 929 annotated high-resolution images
- **Annotation Format**: YOLOv8 PyTorch format (`<class_id> <x_center> <y_center> <width> <height>` normalized $[0, 1]$)
- **Licensing**: Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Provenance**: Curated in collaboration with industrial blister packaging lines, managed and preprocessed via Roboflow.

---

## 2. Classes & Taxonomy

The dataset features two mutually exclusive, tightly annotated defect detection classes:

| Class ID | Semantic Class Name | Description | Annotation Visual Criteria | Frequency in Dataset |
| :--- | :--- | :--- | :--- | :--- |
| **`0`** | `defect` | Missing tablet, crushed foil cavity, fractured/split tablet, foreign particulate, or foil seal puncture. | Bounding box tightly bounds the defective pill pocket or anomaly with zero padding. | ~46.2% of instances |
| **`1`** | `no defect` | Intact, fully filled, undamaged, correctly sealed pharmaceutical blister cavity. | Bounding box tightly fits the perimeter of the intact pill pocket. | ~53.8% of instances |

---

## 3. Annotation Protocol & Tight Bounding Box Standards

To prevent boundary ambiguity during edge model training:
1. **Tight Boundary Rule**: Boxes must bound only the physical cavity or tablet without exceeding the pocket perimeter by more than 2 pixels.
2. **Cavity Alignment**: For missing tablets, the bounding box encloses the empty recessed foil pocket where the tablet should have resided.
3. **Puncture & Defect Inclusions**: Foil tears and foreign particulates are enclosed along with the immediate surrounding pocket area.
4. **Occlusion & Truncation Handling**: Blister packs entering or leaving the FOV are annotated only if at least $70\%$ of the pill pocket is visible.

---

## 4. Preprocessing & Sensor Normalization
- **Acquisition Hardware**: Logitech C270 HD CMOS optical sensor mounted normal ($90^\circ \pm 1^\circ$) to the conveyor plane at 180 mm working distance.
- **Illumination**: Controlled 5500K daylight-balanced diffused ring lighting eliminating ambient daylight shifts.
- **Resolution**: Images captured at $1280 \times 720$, normalized and resized to $640 \times 640$ (and $416 \times 416$ for inference).
- **Pixel Data**: Auto-orientation enabled with EXIF orientation stripping to ensure consistent spatial orientation.
- **Augmentation**: No artificial distortion, perspective skewing, or blurring applied, preserving true optical defect signatures.

---

## 5. Dataset Split & Class Distribution

The dataset is strictly partitioned into three independent partitions:

| Split Name | Image Count | Percentage (%) | Instance Count | Class 0 (`defect`) | Class 1 (`no defect`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | 743 | 80.0% | 1,486 | 682 (45.9%) | 804 (54.1%) |
| **Validation** | 93 | 10.0% | 186 | 88 (47.3%) | 98 (52.7%) |
| **Test** | 93 | 10.0% | 186 | 86 (46.2%) | 100 (53.8%) |
| **Total** | **929** | **100.0%** | **1,858** | **856** | **1,002** |

> [!IMPORTANT]
> The test split was isolated prior to model selection and hyperparameter tuning. Zero images from the test set were ever exposed to training or validation.

---

## 6. Sample Labelled Images
Verified images with tight bounding boxes rendered are preserved in [`labelled_samples/`](labelled_samples/):
- `defect_missing_pill_tight.jpg` (Class 0: Missing pill detected in pocket 3)
- `defect_cracked_tablet_tight.jpg` (Class 0: Fractured tablet with visible fissure)
- `defect_foil_puncture_tight.jpg` (Class 0: Ruptured cavity backing foil)
- `normal_intact_pack_tight.jpg` (Class 1: Intact 6-pill matrix)
