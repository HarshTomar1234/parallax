---
title: transformers-CV
domain: research
tags: [transformers, computer-vision, pytorch, vit, detr, swin, sam, diffusion, gan, vae, jepa]
sources: [github-transformers-cv]
last_updated: 2026-04-07
confidence: 0.85
links: [vision-transformer, attention-mechanisms, diffusion-models, deep-learning, computer-vision]
---

# transformers-CV

Comprehensive library of transformer architectures for computer vision — implemented from scratch in PyTorch.

- **Repo:** https://github.com/HarshTomar1234/transformers-CV
- **Commits:** 173
- **Language:** Jupyter Notebook (98.3%), HTML (1.2%)

---

## Architectures Implemented (11)

| Architecture | Type | Notable Detail |
|-------------|------|----------------|
| **ViT** | Classification | CIFAR-10 + ImageNet training, patch embedding, MHSA |
| **DETR** | Object Detection | End-to-end detector, bipartite matching loss, Excalidraw diagrams |
| **Swin Transformer** | Hierarchical | Shifted window attention, interactive HTML masking demos |
| **SAM** | Segmentation | SAM + SAM 2 inference notebooks, video segmentation |
| **TimeSformer** | Video | From-scratch V2 implementation, Kinetics-400, Pre-LN interactive diagram |
| **Flamingo VLM** | Vision-Language | Few-shot captioning with OpenFlamingo-9B |
| **AutoEncoders** | Generative | Vanilla AE, VAE, VQ-VAE — MNIST, FashionMNIST |
| **GAN** | Generative | Vanilla GAN, DCGAN (CelebA), 10 interactive HTML diagrams |
| **DDPM** | Diffusion | FashionMNIST 28×28, CIFAR-10 32×32, CelebA 64×64 |
| **JEPA** | Self-supervised | I-JEPA, V-JEPA, V-JEPA 2, LLM-JEPA family |
| **DeiT** | Classification | Data-Efficient Image Transformer paper + notes |

## Structure Pattern

Each architecture folder contains:
- `README.md` — detailed documentation with math
- Architecture diagrams (Excalidraw + PNG)
- From-scratch implementation notebooks
- Inference notebooks with pre-trained models
- Original research paper (PDF)
- Interactive HTML visualizations (where applicable)

## Key Research Papers Covered

- "An Image is Worth 16x16 Words" (ViT)
- "End-to-End Object Detection with Transformers" (DETR)
- "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows"
- "Segment Anything" (SAM)
- "Is Space-Time Attention All You Need for Video Understanding?" (TimeSformer)
- "Flamingo: a Visual Language Model for Few-Shot Learning"
- "Denoising Diffusion Probabilistic Models" (DDPM)
- I-JEPA, V-JEPA, V-JEPA 2, LLM-JEPA papers

## Links

- [[vision-transformer]] — ViT standalone project
- [[attention-mechanisms]] — theoretical underpinning
- [[diffusion-models]] — DDPM implementation
- [[deep-learning]] — domain
