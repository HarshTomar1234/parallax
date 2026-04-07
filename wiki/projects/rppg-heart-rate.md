---
title: rPPG Heart Rate
domain: projects
tags: healthcare, computer-vision, deep-learning, signal-processing, rppg, physnet, pytorch
sources: [github-rppg, portfolio-more]
last_updated: 2026-04-07
links: [[computer-vision]], [[deep-learning]]
---

# rPPG Heart Rate

Contactless heart rate detection from webcam video using deep learning and signal processing.

- **Repo:** https://github.com/HarshTomar1234/rppg-heart-rate
- **Stars:** 4

---

## Approach

Remote Photoplethysmography (rPPG) extracts subtle color changes in facial skin caused by blood flow — detecting heart rate without any physical contact.

## Implementation Stack

| Method | Type | Role |
|--------|------|------|
| **PhysNet** | Deep learning | End-to-end 3D CNN rPPG estimation |
| **CHROM** | Signal processing | Chrominance-based rPPG |
| **POS** | Signal processing | Plane-Orthogonal-to-Skin method |

## Training

- **Dataset:** UBFC-rPPG (benchmark rPPG dataset with ground truth BVP + HR)
- **Input:** Facial video frames at fixed FPS
- **Output:** BVP waveform → heart rate (BPM)

## Face Detection Pipeline

```
Webcam frame
    ↓
Face detection (localize ROI)
    ↓
Extract RGB time series from skin region
    ↓
PhysNet OR CHROM/POS signal extraction
    ↓
FFT / peak detection → BPM estimate
    ↓
Real-time web dashboard
```

## Why Notable

- Non-contact vital signs monitoring — camera as a medical sensor
- Covers two distinct paradigms: learned (PhysNet) vs. handcrafted signal processing (CHROM, POS)
- Real-time inference with web dashboard

## Tech Stack

```
Python | PyTorch | PhysNet | OpenCV | SciPy | Flask/Streamlit
```

## Links

- [[computer-vision]] — face detection, video processing
- [[deep-learning]] — PhysNet 3D CNN
