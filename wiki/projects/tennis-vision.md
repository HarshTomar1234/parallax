---
title: Tennis Vision
domain: projects
tags: computer-vision, yolov8, bytetrack, pytorch, object-detection, tracking
sources: [github-tennis-vision, portfolio-projects]
last_updated: 2026-04-07
links: [[computer-vision]], [[object-detection]], [[multi-object-tracking]], [[deep-learning]]
---

# Tennis Vision

Real-time tennis match analysis system. Top project by stars (★32).

- **Repo:** https://github.com/HarshTomar1234/Tennis-Vision
- **Demo:** https://huggingface.co/spaces/Coddieharsh/tennis-vision
- **Stars:** 32 | **Forks:** 2
- **Last updated:** Jan 30, 2026

---

## Performance Metrics

- **Player detection:** 95% accuracy (using YOLOv8x, achieving 92.8% mAP@0.5)
- **Ball tracking:** 88% precision (achieving 87.3% mAP@0.5)
- **Court detection:** 91.5% accuracy within a tight 5px tolerance margin
- **Shot classification:** 89.4% overall stroke identification accuracy
- **Processing pipeline speed:** 6.67 FPS (Optimized via 94% memory reduction using ROI cropping)
- **Temporal visualizer speed:** 30 FPS display sync

## Shot Classification Breakdown

| Shot Type | Accuracy |
|-----------|---------|
| Serve     | 95.2% |
| Volley    | 91.3% |
| Smash     | 93.7% |
| Forehand  | 87.8% |
| Backhand  | 86.1% |

## Architecture

- **Player detection:** YOLOv8x, confidence threshold 0.7, size filter 20×50px min
- **Ball tracking:** Custom YOLOv8 trained on 578 images, polynomial interpolation for smooth trajectories
- **Court detection:** ResNet-50 keypoint detection, 14 landmarks
- **Shot classification:** Rule-based classifier — player position + ball trajectory + temporal context
- **Tracking:** ByteTrack for robust multi-object tracking
- **Visualization:** Mini-court bird's-eye view, heatmaps, speed analytics dashboard

## Core Tech Stack

- **AI & Deep Learning:** PyTorch, YOLOv8 (Ultralytics)
- **Computer Vision Pipeline:** OpenCV, ByteTrack, Supervision
- **Languages:** Python

## Key Features

- Real-time player tracking with position heatmaps
- Ball trajectory visualization with shot moment identification
- Automated 12-stroke classification
- Comprehensive statistics dashboard (speeds, distances, shot counts)
- Mini-court tactical visualization

## Links

- [[computer-vision]] — primary domain
- [[object-detection]] — YOLO architecture used
- [[multi-object-tracking]] — ByteTrack tracking
