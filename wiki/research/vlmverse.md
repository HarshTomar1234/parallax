---
title: VLMverse — PaLiGemma
domain: research
tags: vlm, vision-language, paligemma, siglip, gemma, rope, kv-cache, pytorch
sources: [github-vlmverse, portfolio-research]
last_updated: 2026-04-07
confidence: 0.8
links: [[attention-mechanisms]], [[transformers-cv]], [[deep-learning]]
---

# VLMverse — PaLiGemma

Complete from-scratch PyTorch implementation of PaLiGemma vision-language model.

- **Repo:** https://github.com/HarshTomar1234/VLMverse

---

## Architecture

PaLiGemma fuses two components:

**PaLiGemma Pipeline Fusion:**
1. **Vision Encoding:** The input image is parsed by a `SigLIP Vision Encoder` into 196 discrete visual tokens (based on 224×224 images and 16×16 patches).
2. **Token Prepension:** These visual tokens are projected and linearly prepended directly into the text token sequence.
3. **Language Decoding:** The `Gemma Language Decoder` ingests the fused token sequence to execute autoregressive generation.

## SigLIP Vision Encoder

- Vision Transformer architecture
- 16×16 patch size on 224×224 images → 196 tokens
- Sigmoid loss instead of softmax (SigLIP vs CLIP distinction)
- Contrastive pretraining on image-text pairs

## Gemma Language Decoder

| Component | Spec |
|-----------|------|
| Architecture | Decoder-only Transformer |
| Normalization | RMSNorm (instead of LayerNorm) |
| Activation | GeLU |
| Position encoding | Rotary Position Encoding (RoPE) |
| Attention | Grouped-Query Attention (GQA) |

## Key Implementation Details

- **RoPE** — rotation matrices applied to Q/K vectors at each layer; position-aware without absolute embeddings
- **KV-Cache** — cached key-value pairs for efficient autoregressive inference (reduces quadratic to linear for generation)
- **GQA** — fewer key-value heads than query heads, reducing memory bandwidth bottleneck

## Why This Matters

PaLiGemma represents modern multimodal architecture. Implementing it from scratch demonstrates:
- Deep understanding of vision-language fusion
- Mastery of RoPE, GQA, RMSNorm — components now standard in Llama, Gemma, Mistral
- KV-Cache implementation — critical for production inference optimization

## Links

- [[attention-mechanisms]] — RoPE, GQA, KV-Cache deep dives
- [[transformers-cv]] — companion library
- [[deep-learning]] — domain
