---
title: Object Detection
domain: concepts
tags: [object-detection, yolo, detr, anchor-free, nms, map, detection-head]
sources: [github-transformers-cv, github-tennis-vision, portfolio-projects]
last_updated: 2026-04-07
confidence: 0.85
links: [tennis-vision, field-fusion, transformers-cv, computer-vision, multi-object-tracking]
---

# Object Detection

Localizing and classifying objects in images. Core skill applied in [[tennis-vision]], [[field-fusion]], and implemented from scratch in [[transformers-cv]].

---

## Task Definition

Given an image, output N bounding boxes:
- **Box coordinates:** (x_center, y_center, width, height) — normalized to [0,1]
- **Confidence score:** P(object) × IoU
- **Class probabilities:** P(class | object)

## Two-Stage vs One-Stage

| Approach | Examples | Speed | Accuracy |
|----------|---------|-------|----------|
| Two-stage | Faster R-CNN, Mask R-CNN | Slower | Higher |
| **One-stage** | YOLO, SSD, RetinaNet | Fast | Competitive |
| Transformer | **DETR**, DINO, RT-DETR | Variable | SOTA |

## YOLO Family (Primary tool)

**YOLOv5 → YOLOv8** used in production:

- Anchor-based (v5) → anchor-free (v8)
- Single forward pass: image → grid cells, each predicting boxes + classes
- **Backbone:** CSP-DarkNet or C2f blocks for feature extraction
- **Neck:** PANet for multi-scale feature fusion (FPN-style)
- **Head:** Decoupled classification + regression heads (v8)

### YOLOv8 Specifics
- Anchor-free: predicts (x, y, w, h) as offsets from grid cell center
- Uses DFL (Distribution Focal Loss) for box regression
- Task-specific heads for detect / segment / pose / classify / OBB

## DETR — Transformer Detection

Replaces anchors and NMS entirely:

1. **Backbone** extracts features → flattened + positional encoding
2. **Transformer encoder** processes the feature map
3. **N learned object queries** attend to encoder output via cross-attention
4. **FFN** predicts (class, box) per query
5. **Hungarian matching** for bipartite assignment of predictions to ground truth (no NMS needed)

Implemented from scratch in [[transformers-cv]].

## Evaluation Metric: mAP

**mAP@0.5:** Average Precision computed at IoU threshold 0.5
**mAP@0.5:0.95:** Averaged across IoU thresholds from 0.5 to 0.95 in steps of 0.05

- Precision: TP / (TP + FP)
- Recall: TP / (TP + FN)
- AP: area under the precision-recall curve per class
- mAP: mean over all classes

## NMS — Non-Maximum Suppression

Post-processing to eliminate redundant boxes:
1. Sort boxes by confidence descending
2. Keep highest-confidence box
3. Remove all boxes with IoU > threshold against the kept box
4. Repeat

DETR eliminates NMS by design. YOLOv8 still uses NMS at inference.

## Key Techniques Applied

| Technique | Where |
|-----------|-------|
| YOLOv8x (confidence 0.7, size filter 20×50px) | [[tennis-vision]] player detection — 95% accuracy |
| Custom YOLOv8 (trained on 578 images) | [[tennis-vision]] ball tracking — 88% precision |
| YOLOv8 + ByteTrack | [[field-fusion]] — 91% mAP football analysis |
| DETR from scratch | [[transformers-cv]] |
| ResNet-50 keypoint detection | [[tennis-vision]] court landmark detection — 14 landmarks |

## Links

- [[multi-object-tracking]] — tracking detected objects across frames
- [[tennis-vision]] — primary production use
- [[field-fusion]] — agricultural/sports multi-sensor detection
- [[transformers-cv]] — DETR implementation
- [[computer-vision]] — parent domain
