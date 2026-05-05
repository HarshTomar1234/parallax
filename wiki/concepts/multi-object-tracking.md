---
title: Multi-Object Tracking
domain: concepts
tags: [multi-object-tracking, bytetrack, deepsort, kalman-filter, reid, mot]
sources: [github-tennis-vision, github-field-fusion, portfolio-projects]
last_updated: 2026-04-07
confidence: 0.85
links: [tennis-vision, field-fusion, object-detection, computer-vision]
---

# Multi-Object Tracking

Associating detections across video frames to maintain consistent object identities over time. Applied in [[tennis-vision]] and [[field-fusion]].

---

## Problem Statement

Detection gives boxes per frame. Tracking answers: *is the player in frame t the same person as in frame t-1?*

- **Re-identification challenge:** Objects can look identical (players in same jersey)
- **Occlusion challenge:** Objects temporarily disappear, then reappear
- **ID switching:** Tracker assigns a new ID after a short disappearance

## Tracking Paradigm: Tracking-by-Detection

1. Run detector on each frame (YOLO, etc.)
2. Associate new detections to existing tracked objects
3. Update or create tracks

Association cost is computed by combining:
- **IoU** between predicted and detected boxes (positional similarity)
- **Appearance features** (re-ID embedding similarity) — optional

## Kalman Filter

Tracks the state of each object and predicts its next position:

- **State vector:** (x, y, w, h, vx, vy, vw, vh) — position + velocity
- **Predict step:** Advance state forward using constant velocity model
- **Update step:** Correct prediction with the actual detection
- **Gain:** Higher uncertainty → weight the measurement more; lower → trust prediction

Used in SORT, DeepSORT, ByteTrack as the motion model.

## ByteTrack

Primary tracker used in [[tennis-vision]] and [[field-fusion]].

**Key innovation:** Don't discard low-confidence detections — use them for re-association.

### Two-pass association:
1. **First pass:** Associate high-confidence detections (score > threshold_high) to existing tracks using IoU
2. **Second pass:** Associate **low-confidence** detections (threshold_low < score < threshold_high) to the *unmatched* tracks from pass 1
3. **New tracks:** Unmatched high-confidence detections seed new track candidates

**Why this works:** A partially-occluded object gets a lower detection confidence, but ByteTrack still uses it to keep the track alive — preventing premature ID termination.

| Metric | ByteTrack on MOT17 |
|--------|-------------------|
| MOTA | 80.3 |
| IDF1 | 77.3 |
| IDs | 2196 |

## DeepSORT

**SORT + appearance Re-ID embedding:**

- Adds a CNN-based feature extractor to each detection
- Association metric: weighted sum of Mahalanobis distance (motion) + cosine distance (appearance)
- Better at re-identifying after long occlusions vs. pure IoU trackers

Used in [[tennis-vision]] as a secondary consideration; ByteTrack is primary.

## Custom Kalman Interpolation (Ball Tracking)

In [[tennis-vision]], the ball moves fast and is often occluded:
- YOLOv8 ball detector runs on each frame
- Missing detections are filled via polynomial interpolation over the trajectory
- This smooths the trajectory for shot-moment identification

## Hungarian Algorithm

Optimal assignment for the association step:

- Builds a cost matrix: rows = existing tracks, columns = new detections
- Entry = IoU or distance between track and detection
- Hungarian algorithm finds the assignment that minimizes total cost in O(n³)

## Links

- [[object-detection]] — detections that feed the tracker
- [[tennis-vision]] — ByteTrack for player tracking, custom interpolation for ball
- [[field-fusion]] — ByteTrack for athlete/object tracking in agricultural environments
- [[computer-vision]] — parent domain
