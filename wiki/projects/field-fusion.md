---
title: Field Fusion
domain: projects
tags: [computer-vision, football, yolov8, deepsort, bytetrack, k-means, tracking, pose]
sources: [github-field-fusion, portfolio-projects]
last_updated: 2026-04-07
confidence: 0.95
links: [computer-vision, multi-object-tracking, object-detection]
---

# Field Fusion

Football match analysis via computer vision — player tracking, team classification, tactical analysis.

- **Repo:** https://github.com/HarshTomar1234/Field_Fusion
- **Demo:** https://huggingface.co/spaces/Coddieharsh/field-fusion

---

## Performance

- **Player Detection mAP:** 91%
- **Team Classification:** 89% accuracy (using advanced K-means over jersey colors)
- **Tracking System MOTA:** 94% (powered by ByteTrack integration)

## CV Pipeline

**Platform Workflow:**
1. **Frame Ingestion:** Reading raw broadcast-angle footage.
2. **Detection Phase:** Passing frames through a football-finetuned YOLOv8 model capable of extracting player/ball bounding boxes at 91% mAP.
3. **Team Assignment:** Sampling and applying K-means clustering over bounding boxes to achieve 89% jersey color classification.
4. **Tracking Application:** Establishing state-linking across sequential frames with ByteTrack to output 94% accurate player MOTA tracking.
5. **Perspective Calibration:** Generating mathematically grounded pixel-to-real-world mappings for physical speed and location approximation.
6. **Delivery Engine:** Overlaying comprehensive statistical visualizations, spatial heatmaps, and annotated tracking lines.

## Components

| Component | Method | Accuracy |
|-----------|--------|---------|
| Player detection | YOLOv8 (fine-tuned on football) | 91% mAP |
| Team classification | K-means on jersey color pixels | 89% |
| Ball tracking | Custom YOLO | — |
| Multi-object tracking | ByteTrack | 94% MOTA |
| Speed estimation | Perspective transform + calibration | — |

## Core Tech Stack

- **Computer Vision Core:** Python, OpenCV, Supervision, NumPy
- **Detection & Tracking Libraries:** YOLOv8, ByteTrack, DeepSORT

## Links

- [[computer-vision]] — CV domain
- [[multi-object-tracking]] — ByteTrack algorithm
- [[object-detection]] — YOLO used
