---
title: Field Fusion
domain: projects
tags: computer-vision, football, yolov8, deepsort, bytetrack, k-means, tracking, pose
sources: [github-field-fusion, portfolio-projects]
last_updated: 2026-04-07
links: [[computer-vision]], [[multi-object-tracking]], [[object-detection]]
---

# Field Fusion

Football match analysis via computer vision — player tracking, team classification, tactical analysis.

- **Repo:** https://github.com/HarshTomar1234/Field_Fusion
- **Demo:** https://huggingface.co/spaces/Coddieharsh/field-fusion

---

## Performance

```
Player detection mAP: 91%
Team classification: 89% accuracy (K-means on jersey colors)
Tracking MOTA: 94% (ByteTrack)
```

## CV Pipeline

```
Frame input
    ↓
YOLOv8 (football fine-tuned)  → player/ball detection (91% mAP)
    ↓
K-means clustering             → jersey color → team assignment (89% acc)
    ↓
ByteTrack                      → multi-player tracking (94% MOTA)
    ↓
Perspective transformation     → camera calibration → speed estimation
    ↓
Possession stats + heatmaps + tactical overlays
```

## Components

| Component | Method | Accuracy |
|-----------|--------|---------|
| Player detection | YOLOv8 (fine-tuned on football) | 91% mAP |
| Team classification | K-means on jersey color pixels | 89% |
| Ball tracking | Custom YOLO | — |
| Multi-object tracking | ByteTrack | 94% MOTA |
| Speed estimation | Perspective transform + calibration | — |

## Tech Stack

```
Python | YOLOv8 | ByteTrack | DeepSORT | OpenCV | Supervision | NumPy
```

## Links

- [[computer-vision]] — CV domain
- [[multi-object-tracking]] — ByteTrack algorithm
- [[object-detection]] — YOLO used
