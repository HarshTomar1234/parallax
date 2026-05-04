---
title: Connections
domain: meta
tags: cross-domain, connections, synthesis, graph, patterns
sources: []
last_updated: 2026-04-07
confidence: 0.85
links: [[index]], [[overview]], [[knowledge-gaps]], [[synthesis]]
---

# Connections

Cross-domain connection map. Patterns that emerge when the knowledge graph is read as a whole rather than page by page.

---

## Architecture Convergence: Everything Becomes Attention

The knowledge graph reveals a single architectural thread running through every research project:

| Project | Architecture | Attention Type |
|---------|-------------|----------------|
| [[vision-transformer]] | ViT | MHSA on image patches |
| [[transformers-cv]] (Swin) | Hierarchical ViT | Shifted-window attention |
| [[transformers-cv]] (DETR) | Encoder-decoder | Cross-attention for object queries |
| [[vlmverse]] (PaLiGemma) | SigLIP + Gemma | GQA + RoPE |
| [[lora-qlora]] | BERT / LLaMA | Attention layers are the LoRA injection sites |
| [[reasoning-llms]] | GPT/LLaMA family | Attention + KV-Cache for inference scaling |

See [[attention-mechanisms]] for the unifying theory.

---

## Production ↔ Research Loop

Each production project connects to an underlying research implementation:

| Production system | Research foundation |
|-------------------|-------------------|
| [[tennis-vision]] (YOLO + ByteTrack) | [[transformers-cv]] (DETR), [[object-detection]], [[multi-object-tracking]] |
| [[histopathology]] (ViT + ResNet) | [[vision-transformer]], [[transformers-cv]] |
| [[vlmverse]] (PaLiGemma fine-tuning) | [[lora-qlora]] (the PEFT method), [[attention-mechanisms]] (GQA, RoPE) |
| [[quanta-ai]] (LLM pipeline) | [[reasoning-llms]] (CoT, alignment) |
| [[field-fusion]] (multi-sensor + tracking) | [[object-detection]], [[multi-object-tracking]] |

Pattern: implement the research first, ship the application second.

---

## MLOps as the Production Enabler

The [[mlops]] skill is the connective tissue between research and production:

- [[deepguard]] — adversarial robustness + FastAPI + ONNX deployment
- [[insureml-pipeline]] — full ML lifecycle: MongoDB → training → S3 → EC2 → CI/CD
- [[decifra]] — XAI layer (SHAP/LIME) on top of model inference
- [[quanta-ai]] — LLMOps pipeline with TypeScript + Next.js frontend

Common infrastructure: FastAPI (API layer) · Docker (packaging) · GitHub Actions (CI/CD) · AWS/cloud (deployment).

---

## GenAI as the Emerging Trajectory

The knowledge graph has a clear temporal direction — older pages are deep-CV, newer pages are GenAI/Agents:

```
2024 → Computer Vision (Tennis Vision, Field Fusion, Histopathology)
2025 → Research breadth (transformers-cv × 11 architectures)
2025 → VLMs (vlmverse, PaLiGemma)
2025 → Agents (Travel Planner, Quanta AI, MCP, LangGraph)
2026 → Infrastructure (InsureML-Pipeline, MLOps tooling)
```

See [[knowledge-gaps]] for where this trajectory is heading (Mamba, LLMOps, distributed training).

---

## The "From-Scratch" Philosophy as a Unifying Principle

The strongest signal across all research pages:

- [[vision-transformer]] — ViT from scratch, not a wrapper
- [[transformers-cv]] — 11 architectures from scratch, not imports
- [[lora-qlora]] — custom `LoRALinear` module, not PEFT library
- [[reasoning-llms]] — implementing CoT and RLHF mechanics, not calling an API

This is a deliberate learning strategy: understand the mechanism, then use the library. The implementations are learning artifacts, not library replacements.

---

## Links

- [[index]] — full page catalog
- [[overview]] — identity and career context
- [[knowledge-gaps]] — what's missing from the graph
