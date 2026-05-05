---
title: Synthesis
domain: meta
tags: [synthesis, cross-domain, patterns, trajectory, meta]
sources: [wiki-graph, connections, overview]
last_updated: 2026-05-05
confidence: 0.85
links: [connections, overview, attention-mechanisms, deep-learning, mlops, genai-agents]
---

# Synthesis

Cross-domain meta-insights derived from building and studying the full portfolio.

---

## The One Architecture

Every domain in this wiki converges on the same underlying structure: **attention over a context window**.

- Computer vision — ViT patches are tokens; attention replaces convolution
- NLP — transformers replaced RNNs by attending over token sequences
- Multimodal — VLMs treat image patches and text tokens identically
- Agents — tool calls and memory are just tokens in a longer context
- RAG — retrieval expands the context window with external knowledge

The implication: mastering [[attention-mechanisms]] is not a specialisation. It is the foundation that generalises across every subfield.

---

## Research → Production Loop

No project in this wiki exists purely as research or purely as engineering. Every production system uses a research insight; every research implementation was built to be deployed.

| Research insight | Production application |
|---|---|
| YOLOv8 real-time detection | Tennis-Vision player/ball tracking |
| ByteTrack two-pass association | Multi-object tracking in field analysis |
| LoRA parameter efficiency | Fine-tuning LLMs in Decifra and VLMverse |
| RAG retrieval augmentation | QuantaAI document intelligence |
| Diffusion inpainting | DeepGuard adversarial robustness testing |
| SMOTE imbalanced learning | InsureML-Pipeline model training |

The loop is tight: a paper appears → it gets implemented → it gets deployed → deployment constraints feed back into what to study next.

---

## MLOps as the Enabler

[[mlops]] is not a separate skill — it is the connective tissue that makes everything else shippable. Without it, every model in this wiki stays a Jupyter notebook.

Key pattern observed across projects:

1. Model works locally → needs Docker + FastAPI to serve
2. FastAPI works locally → needs CI/CD to deploy reliably
3. CI/CD works → needs monitoring to catch drift
4. Monitoring catches drift → needs retraining pipeline to close the loop

InsureML-Pipeline completes all four steps. Every other project is at step 1 or 2.

---

## The From-Scratch Philosophy

A recurring choice across this wiki: build from scratch before using a framework.

- LoRA and QLoRA implemented in pure PyTorch before using PEFT (see [[pytorch-lora-qlora]])
- Attention mechanisms coded in NumPy before using PyTorch
- MCP client built from scratch in Kubrick before using a library
- RAG pipeline assembled from components before using LangChain

Why: understanding the internals makes debugging production failures fast. Frameworks hide failure modes; scratch implementations expose them.

---

## GenAI Trajectory

Looking across [[genai-agents]], [[vlmverse]], [[reasoning-llms]], and the Kubrick contribution, the trajectory is clear:

1. **2023** — Single-model inference (GPT-4, Claude)
2. **2024** — RAG + tool use (structured outputs, function calling)
3. **2025** — Multi-agent systems (A2A, MCP, orchestration)
4. **2026+** — Multimodal agents with persistent memory and real-time video/audio understanding

The portfolio spans all four phases. Travel-Planner demonstrates step 3; Kubrick demonstrates the step 3→4 transition.

---

## Confidence Distribution

| Domain | Avg confidence | Notes |
|---|---|---|
| Projects (own repos) | 0.95 | Directly from source, built by hand |
| Career | 0.93 | First-person knowledge |
| Skills | 0.89 | Mix of practice and study |
| Concepts | 0.83 | Based on papers + implementations |
| Research | 0.82 | Study + replication, not original research |
| Learning repos | 0.80 | Auto-ingested, less curated |

---

## Knowledge Gaps (Active)

See [[knowledge-gaps]] for the full list. The three most load-bearing gaps right now:

- **Formal evaluation** — no systematic benchmarking across projects
- **Distributed training** — all models trained on single GPU or CPU; no multi-node experience
- **RL fundamentals** — GRPO and DPO are used in [[reasoning-llms]] but the RL theory underneath is shallow

---

## Related

- [[connections]] — structural cross-domain link map
- [[overview]] — career timeline and identity
- [[attention-mechanisms]] — the unifying architecture
- [[mlops]] — the production enabler
- [[genai-agents]] — the current frontier
- [[deep-learning]] — the foundation
