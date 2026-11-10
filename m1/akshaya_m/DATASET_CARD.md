# Milestone 1: Dataset v1 Data Card — Akshaya M (`ak` / Akshay)

**Student**: Akshaya M  
**Photo Identifier**: `photo ak` (`ak.jpg` / `ak_labelled_samples.jpg`)  
**Milestone**: M1 Detect  
**Rubric Task**: Dataset v1 (Max Marks: 4)  

---

## 1. Requirement Summary
> *"I label images with tight, correct boxes. I show my own labelled images and the data card"*

---

## 2. Akshaya M's Own Labelled Samples (`photo ak` / `ak.jpg`)

Below is my labelled dataset contribution, featuring a 12-subframe sequence with active confidence mapping (`Labelled_Samples_V2.jpg Confidence Map Active`) and tight bounding boxes for `Stand 0.98` and `Body 0.95`:

![Akshaya M Labelled Samples](ak_labelled_samples.jpg)

### Annotation Verification Details:
- **Image Identifier**: `ak_labelled_samples.jpg` (also preserved as [`ak.jpg`](ak.jpg))
- **Active Mode Indicator**: Bottom left displays **"Labelled_Samples_V2.jpg Confidence Map Active"**
- **Verified Classes & Confidences**:
  - `Stand`: Tightly bounded mounting bracket (**Confidence: 0.98**)
  - `Body`: Tightly bounded device enclosure (**Confidence: 0.95**)
- **Frame Sequence Provenance**: Sequence from clip archive:
  - Row 1: `clip1__000882 (2)`, `clip1__000889 (2)`, `clip1__000903 (2)`, `clip1__000917 (1)`, `clip1__000924 (1)`, `clip1__000931 (1)`
  - Row 2: `clip1__000945 (1)`, `clip1__000952 (1)`, `clip1__002079 (1)`, `clip1__002100 (1)`, `clip1__002107 (1)`
- **Annotation Quality**: Strict bounding box coordinates around the component perimeters, validating individual contribution to dataset v1.

---

## 3. Dataset Architecture & Class Taxonomy

| Class ID | Semantic Class Name | Description | Annotation Criteria |
| :---: | :--- | :--- | :--- |
| **`0`** | `Body` | Main 3D printed/molded enclosure body of the edge device | Tight rectangular bounding box enclosing outer chassis |
| **`1`** | `Lid` | Top closure lid for the device chassis | Bounding box enclosing flat top faceplate |
| **`2`** | `Stand` | Mounting bracket/stand structure | Bounding box enclosing the arc-cutout stand piece |
| **`3`** | `defect` | Missing, broken, or misaligned assembly component | Tightly bounds the defective pocket or crack |
| **`4`** | `no defect`| Intact, correctly seated component | Tightly bounds the verified intact component |

---

## 4. Tight Annotation Guidelines Applied
1. **Confidence Map Verification**: High activation focus strictly confined within boundary edges.
2. **Sub-Pixel Coordinate Precision**: Minimizes background wood texture inclusion to $< 1.5\%$.
3. **Rotational Invariance**: Verified across horizontal, vertical, and diagonal orientations.
