---
title: Computer Vision
domain: skills
tags: computer-vision, yolo, opencv, tracking, segmentation, detection, pose
sources: [github-profile, portfolio-projects, portfolio-research, resumes]
last_updated: 2026-04-07
confidence: 0.9
links: "[[tennis-vision]], [[field-fusion]], [[histopathology]], [[rppg-heart-rate]], [[transformers-cv]], [[object-detection]], [[multi-object-tracking]]"
---

# Computer Vision

Core domain. Applied across production systems, research, and healthcare.

---

## Proficiency Map

| Area | Depth | Applied In |
|------|-------|-----------|
| Object Detection | Deep | [[tennis-vision]], [[field-fusion]] |
| Multi-Object Tracking | Deep | [[tennis-vision]], [[field-fusion]] |
| Segmentation | Strong | [[transformers-cv]] (SAM, Swin, DETR) |
| Pose Estimation | Working | BBoxMaskPose (ICCV 2025) |
| Medical Imaging | Applied | [[histopathology]], [[rppg-heart-rate]] |
| Video Analysis | Applied | [[tennis-vision]], [[field-fusion]], TimeSformer |
| Optical Flow | Working | [[field-fusion]] speed estimation |

---

## Tools & Frameworks

### Detection
- **YOLOv5, YOLOv8, YOLOv8x** — custom training, fine-tuning, inference
- **ResNet-50** — keypoint detection (court landmarks in Tennis Vision)
- **MobileNetV2** — transfer learning for classification (Histopathology)
- **DETR** — end-to-end transformer detection (transformers-cv)

### Tracking
- **ByteTrack** — primary tracker (Tennis Vision player tracking, Field Fusion)
- **DeepSORT** — re-identification-based tracking
- **Custom Kalman Filter interpolation** — ball trajectory smoothing

### Segmentation
- **SAM + SAM 2** — zero-shot segmentation, video segmentation
- **U-Net** — medical segmentation
- **Mask R-CNN** — instance segmentation

### Core Libraries
- **OpenCV** — video I/O, image processing, perspective transforms, Optical Flow
- **Supervision** — annotation, tracking utilities
- **Albumentations** — augmentation pipelines

---

## Key Techniques Mastered

- Confidence threshold tuning + NMS
- Custom dataset annotation + YOLO fine-tuning
- Perspective transformation for metric space (Field Fusion speed estimation)
- ROI-based processing for memory efficiency (94% reduction in Tennis Vision)
- K-means clustering for visual classification (team jerseys)
- Grad-CAM for CNN explainability
- rPPG signal extraction from RGB video

---

## Projects Using This Skill

- [[tennis-vision]] — 95% player detection, 88% ball tracking
- [[field-fusion]] — 91% mAP football analysis
- [[histopathology]] — MobileNetV2 + Grad-CAM cancer detection
- [[rppg-heart-rate]] — contactless heart rate from webcam
- [[transformers-cv]] — 11 CV architectures from scratch
