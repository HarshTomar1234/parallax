---
title: LoRA & QLoRA
domain: research
tags: lora, qlora, peft, fine-tuning, quantization, 4-bit, nf4, llm, memory-efficiency
sources: [github-lora-qlora, portfolio-research]
last_updated: 2026-04-07
confidence: 0.85
links: "[[attention-mechanisms]], [[deep-learning]], [[lora-theory]], [[pytorch-lora-qlora]]"
---

# LoRA & QLoRA

Pure PyTorch implementations of parameter-efficient fine-tuning methods for LLMs and Vision Transformers.

- **Repo:** https://github.com/HarshTomar1234/PyTorch-LoRA-QLoRA

---

## Memory Reduction Results

- **LoRA on BERT:** 65% memory reduction
- **LoRA on LLaMA-7B:** 50% memory reduction
- **QLoRA on LLaMA-65B:** 85% memory reduction (Fits large models onto standard consumer GPUs)

## LoRA — Concept

Standard fine-tuning updates all weights W (huge memory cost).

LoRA freezes W and injects two small trainable matrices A, B:

> **W' = W + ΔW = W + B·A**
> 
> *where:*
> - **B** ∈ R^(d×r)
> - **A** ∈ R^(r×k)
> - **r** << d,k  *(rank, typically 8, 16, or 32)*

- **Parameter reduction:** trains <1% of original parameters
- **Zero inference overhead** — at deployment, B·A merges into W

## QLoRA — Additions

| Innovation | Detail |
|------------|--------|
| **4-bit NF4 Quantization** | Normal Float 4 — optimized for LLM weight distributions (normal dist) |
| **Double Quantization** | Quantizes the quantization constants themselves for extra savings |
| **Paged Optimizers** | Manages GPU memory spikes during backprop |

## Implementation Details

- Custom `LoRALinear` module wrapping `nn.Linear`
- `lora_rank` parameter controls r
- `lora_alpha` controls scaling (ΔW scaled by α/r)
- BitsAndBytes integration for 4-bit loading in QLoRA
- Fine-tuning scripts for BERT, LLaMA-7B, and Vision Transformers

## Practical Significance

Enables fine-tuning Llama-65B on a single GPU with 48GB VRAM — impossible with standard fine-tuning. This is the technique behind most open-source fine-tuned LLMs.

## Links

- [[attention-mechanisms]] — transformer layers where LoRA is applied
- [[deep-learning]] — domain
- [[lora-theory]] — deeper theoretical treatment
- [[pytorch-lora-qlora]] — from-scratch implementation repo
