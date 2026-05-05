---
title: LoRA Theory
domain: concepts
tags: [peft, fine-tuning, linear-algebra, svd, rank-decomposition]
sources: [research-papers]
last_updated: 2026-04-07
confidence: 0.85
links: [lora-qlora, attention-mechanisms]
---

# Low-Rank Adaptation (LoRA) Theory

A foundational concept in Parameter-Efficient Fine-Tuning (PEFT) that enables the tuning of gigantic models on consumer hardware.

---

## The Mathematical Intuition

When a massive neural network (like LLaMA or GPT) learns a new downstream task, it doesn't need to change every single one of its billion parameters independently. The "intrinsic rank" of the task-specific update is small.

Standard Fine-Tuning updates the massive weight matrix **W**.
LoRA freezes **W** and adds a small, trainable residual pathway composed of two low-rank matrices, **A** and **B**.

> **ΔW = B × A**

If **W** is *10,000 × 10,000* (100,000,000 parameters), and we choose a rank *r = 8*:
- **B** is *10,000 × 8* (80,000 parameters)
- **A** is *8 × 10,000* (80,000 parameters)

Total trainable parameters: **160,000** instead of 100 million (a **99.8% reduction**).

## Why It Works

1. **Initialization:** **A** is initialized with random Gaussian numbers, but **B** is initialized to zero. Therefore, at the start of training, **B × A = 0**, meaning the model behaves exactly like the original pre-trained model.
2. **Backpropagation:** Gradients only flow into **A** and **B**.
3. **Inference:** Once training is done, you can multiply **B × A** to get **ΔW**, and permanently add it to **W**. There is **zero latency overhead** during inference.

## The QLoRA Extension

QLoRA takes this further by quantizing the base weights (**W**) into a highly compressed 4-bit format (NF4). You cannot train 4-bit weights, but you *can* run forward passes through them. The gradients are computed in 16-bit precision and applied to the 16-bit **A** and **B** LoRA matrices, enabling fine-tuning of a 65-Billion parameter model on a single GPU.

## Related Resources
- **[[lora-qlora]]** — My PyTorch implementation of these mechanics.
- **[[attention-mechanisms]]** — The transformer layers where LoRA is typically injected.
