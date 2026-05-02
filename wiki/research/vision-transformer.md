---
title: Vision Transformer (ViT)
domain: research
tags: vit, transformer, image-classification, patch-embedding, mhsa, pytorch
sources: [github-transformers-cv, portfolio-research]
last_updated: 2026-04-07
links: [[transformers-cv]], [[attention-mechanisms]], [[deep-learning]], [[computer-vision]]
---

# Vision Transformer (ViT)

From-scratch PyTorch implementation of "An Image is Worth 16x16 Words" (Dosovitskiy et al., 2020). Standalone project and a core architecture in [[transformers-cv]].

- **Repo:** https://github.com/HarshTomar1234/Vision-Transformer-ViT-
- **Commits:** ~55

---

## Core Idea

Treat an image as a sequence of fixed-size patches — then apply a standard Transformer encoder.

> CNNs use inductive biases (translation equivariance, locality). ViT removes those biases and lets the model learn spatial relationships from data via global self-attention.

Requires large-scale pre-training to outperform CNNs — the inductive biases that CNNs impose are actually useful at small data scales.

## Architecture

### 1. Patch Embedding
- Image: H × W × C
- Split into N patches of size P × P → N = (H × W) / P²
- Standard ViT-B/16: P=16, so a 224×224 image → 196 patches
- Each patch flattened → linear projection → D-dimensional embedding

### 2. Position Encoding
- 1D learnable position embeddings added to patch embeddings
- Prepend a learnable `[CLS]` token — its final representation is used for classification

### 3. Transformer Encoder
- L layers, each: **LayerNorm → MHSA → skip-connection → LayerNorm → MLP → skip-connection**
- MLP: 2 linear layers, GELU activation, hidden dim = 4×D
- See [[attention-mechanisms]] for MHSA details

### 4. Classification Head
- Take `[CLS]` token output
- Linear layer → num_classes logits

## ViT Variants

| Model | Layers | Hidden dim | Heads | Params |
|-------|--------|-----------|-------|--------|
| ViT-Ti/16 | 12 | 192 | 3 | 6M |
| ViT-S/16 | 12 | 384 | 6 | 22M |
| **ViT-B/16** | 12 | 768 | 12 | 86M |
| ViT-L/16 | 24 | 1024 | 16 | 307M |
| ViT-H/14 | 32 | 1280 | 16 | 632M |

## Training Results

- CIFAR-10 training notebook included
- ImageNet pre-trained weights loading supported
- Attention map visualizations showing which patches the model attends to

## Key Insight: Why Patch Size Matters

Smaller patches → more tokens → quadratic attention cost but finer spatial resolution.
ViT-B/16 vs ViT-B/32: /16 patches are better but 4× more tokens → 16× more attention compute.

## Comparison: ViT vs CNN

| Property | CNN | ViT |
|----------|-----|-----|
| Inductive bias | Translation equivariance, locality | None (learned) |
| Data efficiency | High (works from scratch) | Low (needs large pre-training) |
| Receptive field | Local → hierarchical | Global from layer 1 |
| Scalability | Moderate | Excellent |
| Interpretability | Grad-CAM on feature maps | Attention maps on patches |

## Links

- [[transformers-cv]] — ViT folder with full implementation + Excalidraw diagrams
- [[attention-mechanisms]] — MHSA that powers every encoder layer
- [[deep-learning]] — domain
- [[computer-vision]] — application domain
