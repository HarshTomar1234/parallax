---
title: Diffusion Models
domain: concepts
tags: diffusion, ddpm, score-matching, denoising, generative, noise-schedule
sources: [transformers-cv, github-profile]
last_updated: 2026-04-07
links: [[transformers-cv]], [[deep-learning]]
---

# Diffusion Models

Generative models that learn to reverse a gradual noising process. Implemented in [[transformers-cv]].

---

## Core Idea (DDPM)

```
Forward process (fixed):   x_0 → x_1 → ... → x_T ≈ N(0, I)
Reverse process (learned): x_T → x_{T-1} → ... → x_0

At each step t, add Gaussian noise:
  q(x_t | x_{t-1}) = N(x_t; √(1-β_t)·x_{t-1}, β_t·I)

β_t: noise schedule (linear or cosine)
```

## Reparameterization Trick

The forward process has a closed form — sample x_t directly from x_0:

```
x_t = √(ᾱ_t)·x_0 + √(1-ᾱ_t)·ε,   ε ~ N(0, I)
ᾱ_t = ∏_{s=1}^{t} (1 - β_s)
```

## Training Objective

Train a U-Net ε_θ to predict the noise added at each step:

```
L = E_{t,x_0,ε} [ ||ε - ε_θ(x_t, t)||² ]
```

## Sampling (Inference)

```
Start: x_T ~ N(0, I)
For t = T, T-1, ..., 1:
  ε_pred = ε_θ(x_t, t)        # predict noise
  x_{t-1} = denoise step      # remove predicted noise
Return x_0                     # generated sample
```

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
