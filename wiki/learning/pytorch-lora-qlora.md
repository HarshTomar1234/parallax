---
title: PyTorch LoRA & QLoRA
domain: learning
tags: lora, qlora, fine-tuning, pytorch, quantization, peft, transformers, from-scratch
sources: [https://github.com/HarshTomar1234/PyTorch-LoRA-QLoRA]
last_updated: 2026-05-04
confidence: 0.90
links: [[lora-qlora]], [[lora-theory]], [[deep-learning]], [[reasoning-llms]]
---

# PyTorch LoRA & QLoRA

Pure PyTorch implementations of LoRA and QLoRA from scratch — no PEFT library, no abstraction layers. Every rank decomposition matrix, every quantization bucket, written by hand.

- **Repo:** https://github.com/HarshTomar1234/PyTorch-LoRA-QLoRA

---

## What's Implemented

### LoRA (`lora.py`)

Four adapter classes built from `nn.Module`:

| Class | Wraps | Notes |
|---|---|---|
| `LoRALinear` | `nn.Linear` | Core use case — Q/K/V projections |
| `LoRAEmbedding` | `nn.Embedding` | Token embedding adaptation |
| `LoRAConv2d` | `nn.Conv2d` | Convolutional layers (ViT patch embed) |
| `LoRAModel` | Any model | Replaces target layers, freezes base weights |

All share a `LoRABaseLayer` interface: `lora_A`, `lora_B` matrices, scaling factor `alpha/r`, optional dropout. Weight merging for inference — merged weights produce identical output to the adapter forward pass.

### QLoRA (`qlora.py`)

Stacks three techniques on top of LoRA:

1. **4-bit NF4 quantization** — weights stored as 4-bit NormalFloat, the optimal quantization for normally distributed weights
2. **Double quantization** — quantization constants themselves are quantized (saves ~0.5 bits/param)
3. **Paged optimizers** — optimizer states offloaded to CPU RAM during backward; prevents GPU OOM on long sequences

`QLoRALinear` stores a quantized weight tensor and dequantizes on-the-fly during the forward pass. LoRA adapters run in BF16 on top of the frozen quantized base.

---

## The Math

Standard LoRA forward:

```
y = xW + x(AB)
```

- `W ∈ R^(d×k)` — frozen pre-trained weight
- `A ∈ R^(d×r)`, `B ∈ R^(r×k)` — trainable rank-r matrices
- `r ≪ min(d, k)` — the rank constraint

Scaling: `W' = W + (α/r) · AB`  (or `α/√r` in rank-stabilized variant)

`A` initialised with Kaiming uniform; `B` initialised to zero — so the adapter output is zero at the start of training, matching the pre-trained model exactly.

---

## Training Examples

### ViT on Food101 (LoRA)
- **Target layers:** query, key, value, dense projections
- **Rank:** 8, **alpha:** 16
- **Trainable params:** ~1% of total
- **Training time:** ~1.5 hours (CPU/single GPU)
- LoRA(r=8) reaches 83.8 vs full fine-tune 84.2 on GLUE — 0.4 point gap, 50% fewer params updated

### BERT on IMDB (QLoRA)
- **Quantization:** 4-bit NF4
- **Rank:** 8, double quantization enabled
- **Training time:** ~30 minutes
- Memory at inference: QLoRA uses ~5 GB vs LoRA's ~14 GB vs full fine-tune's ~28 GB (LLaMA 7B reference)

---

## Memory Comparison

| Method | Memory (7B model) | Trainable params |
|---|---|---|
| Full fine-tuning | 28 GB | 100% |
| LoRA (r=8) | 14 GB | ~1–2% |
| QLoRA (4-bit NF4) | 5 GB | ~1–2% |

---

## Why Build From Scratch

Every abstraction in PEFT hides a failure mode. Implementing `LoRALinear` by hand reveals:

- Why `B` must be zero-initialized (non-zero start → random output shift at step 0)
- Why scaling by `α/r` matters (rank changes shouldn't require retuning `α`)
- Why weight merging is lossless (the merged matrix and the adapter forward are algebraically identical)
- Why 4-bit NF4 outperforms INT4 (NF quantization minimises error for Gaussian weight distributions)

This mirrors the [[lora-theory]] concept page, but with runnable code as the proof.

---

## Related

- [[lora-qlora]] — research study of the LoRA and QLoRA papers
- [[lora-theory]] — the mathematical theory behind rank decomposition
- [[deep-learning]] — PyTorch fundamentals this repo is built on
- [[reasoning-llms]] — QLoRA used for fine-tuning reasoning models
