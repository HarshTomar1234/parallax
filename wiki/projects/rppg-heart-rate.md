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

1. **Input Signal:** Capturing raw webcam video frames locally.
2. **Localization:** Extracting precisely the facial ROI through targeted boundary detection.
3. **Time Series Extraction:** Isolating pure RGB data shifting strictly from human skin regions.
4. **Signal Extraction Options:**
   - Deep Learning Route: *PhysNet* execution.
   - Algorithmic Route: *CHROM* or *POS* mapping.
5. **BPM Normalization:** Running Fast Fourier Transform (FFT) and precise peak detection to achieve Beats Per Minute (BPM) estimates.
6. **Delivery:** Plotting signals instantaneously to a real-time web dashboard.

## Why Notable

- Non-contact vital signs monitoring — camera as a medical sensor
- Covers two distinct paradigms: learned (PhysNet) vs. handcrafted signal processing (CHROM, POS)
- Real-time inference with web dashboard

## Core Tech Stack

- **Computer Vision & CNN:** PyTorch, PhysNet Architecture, OpenCV
- **Engineering & Analytics:** Python, SciPy
- **Hosting / Display:** Flask, Streamlit

## Links

- [[computer-vision]] — face detection, video processing
- [[deep-learning]] — PhysNet 3D CNN
