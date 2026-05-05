---
title: Diffusion Models
domain: concepts
tags: [diffusion, ddpm, score-matching, denoising, generative, noise-schedule]
sources: [transformers-cv, github-profile]
last_updated: 2026-04-07
confidence: 0.8
links: [transformers-cv, deep-learning]
---

# Diffusion Models

Generative models that learn to reverse a gradual noising process. Implemented in [[transformers-cv]].

---

## Core Idea (DDPM)

- **Forward process (fixed):** x₀ → x₁ → ... → x_T ≈ N(0, I)
- **Reverse process (learned):** x_T → x_{T-1} → ... → x₀

At each step *t*, Gaussian noise is added according to:

> **q(x_t | x_{t-1}) = N(x_t; √(1-β_t) · x_{t-1}, β_t · I)**

**β_t** is the noise schedule, typically linear or cosine.

## Reparameterization Trick

The forward process has a closed form — sample x_t directly from x_0:

> **x_t = √(ᾱ_t) · x₀ + √(1 - ᾱ_t) · ε**, where **ε ~ N(0, I)**
>
> **ᾱ_t = ∏ from s=1 to t of (1 - β_s)**

## Training Objective

Train a U-Net ε_θ to predict the noise added at each step:

> **L = E [ ‖ε − ε_θ(x_t, t)‖² ]**
>
> The model learns to predict the exact noise **ε** that was added at timestep **t**.

## Sampling (Inference)

1. **Initialize:** Sample x_T from pure Gaussian noise N(0, I).
2. **Iterate:** For every timestep from T down to 1:
   - Predict the noise component using the trained U-Net: **ε_pred = ε_θ(x_t, t)**
   - Remove the predicted noise to recover x_{t-1}.
3. **Output:** The final denoised result x₀ is the generated sample.

## Implementations in [[transformers-cv]]

| Dataset | Resolution | File |
|---------|-----------|------|
| FashionMNIST | 28×28 grayscale | DDPM_from_scratch.ipynb |
| CIFAR-10 | 32×32 RGB | DDPM_CIFAR10.ipynb |
| CelebA | 64×64 RGB | DDPM_CelebA.ipynb |

## Why Diffusion Beats GANs (2023+)

- No mode collapse
- More stable training (no adversarial game)
- Better diversity of samples
- Controllable with guidance (classifier-free guidance)

## Links

- [[transformers-cv]] — DDPM implementation in Diffusion/ folder
- [[deep-learning]] — domain
