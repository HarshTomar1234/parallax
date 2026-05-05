---
title: Writing & Technical Blog
domain: career
tags: [writing, blog, technical-writing, autoresearch, karpathy, llm, autonomous-ml]
sources: [notion-blog]
last_updated: 2026-05-05
confidence: 0.95
links: [overview, open-source, reasoning-llms]
---

# Writing & Technical Blog

Published technical writing on autonomous ML systems, LLM internals, and modern training infrastructure.

---

## Deconstructing Autoresearch

**Published:** 2026
**Platform:** Notion (public)
**URL:** https://kernel-crush.notion.site/Deconstructing-Autoresearch-A-Complete-Technical-Deep-Dive-into-Autonomous-ML-Research-33c4df040c148059a83dd14b9b2b4044

A complete technical deep dive into Andrej Karpathy's autoresearch repository — an autonomous ML research system that runs, evaluates, and iterates on experiments without human intervention.

### What It Covers

**Autonomous Loop Protocol**
- Fixed 5-minute time budget per experiment
- Git as experiment tracker (each run is a commit)
- ~96 experiments per overnight GPU session
- Evaluation metric: Bits Per Byte (BPB) — language-model cross-entropy in interpretable units

**Data Pipeline**
- BPE tokenization internals
- Zero-waste bin packing for sequence batching
- Why token efficiency matters at scale

**8+ Modern GPT Architectural Enhancements**
- RoPE (Rotary Position Embedding) — full mathematical derivation
- Flash Attention 3 — IO-aware attention with hardware memory hierarchy analysis
- QK-Norm — stabilizing attention logits at large sequence lengths
- Residual stream scaling — depth-aware initialization
- ReLU² activation — sparse activations and why they outperform GELU in this regime
- Logit soft-capping — preventing entropy collapse

**Muon Optimizer**
- Polar decomposition via Newton-Schulz iteration (mathematical proof included)
- Why orthogonal gradient updates outperform AdamW for transformer weight matrices
- Pseudocode walkthrough

**Systems Engineering**
- `torch.compile` internals — kernel fusion, graph capture
- Gradient accumulation for simulating large batch sizes
- BFloat16 mixed precision — numerical stability vs. Float16

### Why This Post Matters

The central thesis: *human researchers are the throughput bottleneck in ML research, not compute*. Autoresearch removes that bottleneck by treating the experiment loop itself as an automatable engineering problem.

Writing this required understanding not just what each component does, but why it was chosen over alternatives — the exact reasoning a practitioner needs to apply these ideas to new problems.

---

## Links

- [[reasoning-llms]] — RL and post-training methods, closely related to autonomous research
- [[overview]] — career timeline
- [[open-source]] — other public technical contributions
