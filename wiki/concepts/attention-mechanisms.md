---
title: Attention Mechanisms
domain: concepts
tags: attention, transformer, mhsa, rope, kv-cache, gqa, self-attention
sources: [transformers-cv, vlmverse, lora-qlora, portfolio-research]
last_updated: 2026-04-07
confidence: 0.85
links: [[transformers-cv]], [[vlmverse]], [[lora-qlora]], [[deep-learning]], [[vision-transformer]]
---

# Attention Mechanisms

Core concept underlying all modern transformer architectures. Implemented in multiple forms across research repos.

---

## Scaled Dot-Product Attention

> **Attention(Q, K, V) = softmax(Q·Kᵀ / √d_k) · V**

- **Q (Queries):** What we're looking for.
- **K (Keys):** What's available to match against.
- **V (Values):** What we retrieve once a match is found.
- **d_k:** Key dimension — the scaling factor that prevents vanishing gradients in softmax.

## Multi-Head Self-Attention (MHSA)

- Run h attention heads in parallel, each with different W_Q, W_K, W_V projections
- Each head attends to different subspaces (different "aspects" of the input)
- Concatenate outputs → linear projection
- Used in: ViT, DETR, Swin, TimeSformer ([[transformers-cv]])

## Grouped-Query Attention (GQA)

- Fewer K,V heads than Q heads (e.g., 8 KV heads, 32 Q heads)
- Reduces memory bandwidth — KV-Cache size scales with KV heads, not Q heads
- Middle ground between MHA (all unique heads) and MQA (single KV head)
- Implemented in: [[vlmverse]] (PaLiGemma's Gemma decoder)

## Rotary Position Encoding (RoPE)

Traditional position encodings are additive. RoPE applies rotation matrices to Q and K:

> **q_rotated = q · R(θ·m)**
> **k_rotated = k · R(θ·n)**
>
> The dot product of the rotated vectors naturally encodes the **relative position (m − n)** between tokens.

- **Advantage:** No position embedding parameters. Extrapolates to longer sequences than trained on.
- Implemented in: [[vlmverse]] (Gemma), standard in Llama, Mistral, Gemma

## KV-Cache

During autoregressive generation, K and V are recomputed every step — quadratic cost.

KV-Cache stores K, V for all previous tokens:

- **Step t:** Compute K_t and V_t, then store them in the cache.
- **Step t+1:** Reuse all cached K_{1..t}, V_{1..t} — only compute the new K_{t+1}, V_{t+1}.
- **Result:** Generation cost drops from **quadratic** to **linear** in sequence length.

- Implemented in: [[vlmverse]]
- Critical for production inference optimization

## Shifted Window Attention (Swin)

- Divides image into non-overlapping local windows
- Attention within each window → linear complexity in image size
- "Shifted" windows create cross-window connections between layers
- Implemented in: [[transformers-cv]] (Swin Transformer folder)

## Links

- [[transformers-cv]] — implementations of all attention variants
- [[vlmverse]] — RoPE + GQA + KV-Cache in PaLiGemma
- [[vision-transformer]] — MHSA in image classification
