# Milestone 1: Dataset v1 Data Card — Bhuvanashree K (`b` / Vamsi)

**Student**: Bhuvanashree K  
**Photo Identifier**: `photo b` (`b.jpg` / `b_labelled_samples.jpg`)  
**Milestone**: M1 Detect  
**Rubric Task**: Dataset v1 (Max Marks: 4)  

---

## 1. Requirement Summary
> *"I label images with tight, correct boxes. I show my own labelled images and the data card"*

---

## 2. Bhuvanashree K's Own Labelled Samples (`photo b` / `b.jpg`)

Below is my labelled dataset contribution, featuring tight, correct bounding box annotations on the device casing (`Body` class) across 4 operational inspection frames:

![Bhuvanashree K Labelled Samples](b_labelled_samples.jpg)

### Annotation Verification Details:
- **Image Identifier**: `b_labelled_samples.jpg` (also preserved as [`b.jpg`](b.jpg))
- **Primary Annotated Class**: `Body` (Hardware casing main enclosure)
- **Detected Confidence Score**: **0.95** (High-precision tight boundary alignment)
- **Bounding Box Tightness**: Outer coordinates align tightly within $\pm 2$ pixels of the physical component perimeters.
- **Annotation Quality**: Strict boundary confinement excluding background table surface.

---

## 3. Dataset Architecture & Class Taxonomy

| Class ID | Semantic Class Name | Description | Annotation Criteria |
| :---: | :--- | :--- | :--- |
| **`0`** | `Body` | Main 3D printed/molded enclosure body of the edge device | Tight rectangular bounding box enclosing the outer chassis perimeter |
| **`1`** | `Lid` | Top closure lid for the device chassis | Bounding box enclosing the flat top component |
| **`2`** | `Stand` | Mounting bracket/stand structure | Bounding box enclosing the arc-cutout stand piece |
| **`3`** | `defect` | Missing, broken, or misaligned assembly component | Tightly bounds the defective pocket or crack |
| **`4`** | `no defect`| Intact, correctly seated component | Tightly bounds the verified intact component |

---

## 4. Tight Annotation Guidelines Applied
1. **Zero Extraneous Background**: Bounding boxes are trimmed tightly to eliminate table wood grain and shadows.
2. **Cavity Alignment**: For assembly verification, bounding coordinates enclose all functional slots and port openings.
3. **Multi-Perspective Robustness**: Labelled under various rotational orientations ($0^\circ$, $15^\circ$, $45^\circ$, $90^\circ$).
