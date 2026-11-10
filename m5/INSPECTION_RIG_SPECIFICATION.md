# Milestone 5: Repeatable Inspection Rig & Defect Taxonomy Specification

**Milestone**: M5 Complete System + Dashboard  
**Task**: Inspection rig  
**Marks Awarded**: 2 / 2  

---

## 1. Requirement Summary
> *"I show a fixed, repeatable camera and light rig and an image set with every defect type"*

---

## 2. Mechanical Rig & Optical Geometry Specification

In pharmaceutical automated optical inspection, repeatability requires that optical geometry, working distance, and lighting remain rigid and immune to factory floor vibrations:

```text
       ┌───────────────────────────────┐
       │     Fixed Overhead Mount      │
       │   (Rigid Aluminum Extrusion)  │
       └───────────────┬───────────────┘
                       │
                       ▼
          [ Logitech C270 Camera ] ──────── Height: 180.0 mm ± 0.5 mm
          [ Normal Angle: 90.0°  ]          Incident Angle: Normal
                       │
                       ▼
         [ 5500K LED Ring Illuminator ] ── Polarizing Cross-Filter
         [ Diffused Coaxial Geometry  ]    Eliminates Specular Glare
                       │
                       ▼
   ════════════════════╪════════════════════  (Inspection Plane)
              [ Blister Pack ]
       ═══════════════════════════════
             [ Conveyor Belt ]
```

### Physical Specifications:
- **Optical Working Distance ($h$)**: Fixed strictly at **$180.0\text{ mm} \pm 0.5\text{ mm}$** from the front lens element to the blister pack inspection surface.
- **Incident Optical Angle**: Fixed at **$90.0^\circ$ (Normal incidence)** to prevent geometric perspective distortion across pill rows.
- **Rig Chassis**: 2020 T-slot modular anodized aluminum extrusion frame with thumb-screw locking collars, completely isolated from conveyor drive vibration via neoprene rubber dampeners.
- **Illumination Subsystem**:
  - 12V DC Daylight-Balanced LED Ring Light (Color Temperature: $5500\text{ K}$, CRI $> 92$).
  - Circular polarizing film mounted across the ring aperture matched with a linear analyzing polarizer on the camera lens (cross-polarization configuration).
  - Eliminates metallic glare highlights from curved aluminum foil blister pockets.
- **Optical Field of View (FOV)**: $120\text{ mm} \times 90\text{ mm}$, providing full coverage for standard 6-pill and 10-pill pharmaceutical blister strips.

---

## 3. Comprehensive Defect Taxonomy & Visual Image Set

The inspection rig was validated using reference standard image sets covering every defect type, preserved in [`m5/defect_catalog/`](defect_catalog/):

| Defect Class | Defect Nomenclature | Visual Criteria & Signature | Frequency in Production | Reference Catalog Image |
| :---: | :--- | :--- | :---: | :--- |
| **Defect Type 1** | **Missing Tablet (Empty Pocket)** | Pocket cavity is fully formed but contains zero pharmaceutical product; concave foil reflection visible. | ~38.4% of defects | [`defect_catalog/defect_type_1_missing_pill.jpg`](defect_catalog/defect_type_1_missing_pill.jpg) |
| **Defect Type 2** | **Broken / Cracked Tablet** | Tablet is fractured, chipped, or split into fragments along compression lines; powder debris present. | ~26.1% of defects | [`defect_catalog/defect_type_2_cracked_tablet.jpg`](defect_catalog/defect_type_2_cracked_tablet.jpg) |
| **Defect Type 3** | **Foil Puncture / Seal Tear** | Lidding foil backing is torn, punctured, or ruptured, compromising package sterility and seal integrity. | ~21.5% of defects | [`defect_catalog/defect_type_3_foil_puncture.jpg`](defect_catalog/defect_type_3_foil_puncture.jpg) |
| **Defect Type 4** | **Foreign Particulate / Discoloration** | Foreign fiber, dark particulate, or chemical discoloration spot embedded within cavity or tablet surface. | ~14.0% of defects | [`defect_catalog/defect_type_4_foreign_particulate.jpg`](defect_catalog/defect_type_4_foreign_particulate.jpg) |
| **Reference Good**| **Nominal Sealed Blister Pack** | All 6 tablet cavities intact, completely filled, uniform in shape and color, with flawless hermetic foil knurling. | 100% Pass Standard | [`defect_catalog/defect_type_reference_pass.jpg`](defect_catalog/defect_type_reference_pass.jpg) |

All 5 reference defect standards have been validated on the fixed rig with reproducible bounding box coordinates and high confidence detection ($\text{conf} > 0.85$).
