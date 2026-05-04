---
title: Reasoning LLMs
domain: research
tags: reasoning, chain-of-thought, rlhf, inference-scaling, cot, llm
sources: [github-profile, portfolio-research]
last_updated: 2026-04-07
confidence: 0.8
links: [[attention-mechanisms]], [[deep-learning]], [[lora-qlora]], [[vlmverse]]
---

# Reasoning LLMs

Research implementation exploring Chain-of-Thought reasoning, inference-time scaling, and RLHF alignment in large language models.

- **Repo:** https://github.com/HarshTomar1234
- **Commits:** ~25

---

## Chain-of-Thought (CoT) Reasoning

Standard decoding: input → single-step output.

CoT decoding: input → *intermediate reasoning steps* → final answer.

> "Let's think step by step" — few-shot prompt that unlocks multi-step reasoning in sufficiently large models.

- Emergent at ~100B parameters in original PaLM findings
- Works zero-shot (GPT-3.5+) with the right prompt
- Scales better with compute than direct prompting on math/logic tasks

## Inference-Time Scaling (Test-Time Compute)

Rather than scaling training compute, scale at inference:

| Method | Idea | Trade-off |
|--------|------|-----------|
| **Best-of-N** | Sample N outputs, pick best by reward model | N× latency, N× cost |
| **Self-consistency** | Sample N CoT chains, majority-vote the answer | Better on math — consistent answers cluster |
| **Tree-of-Thought** | Explore reasoning as a tree, prune bad branches | High latency — search overhead |
| **Process Reward Models (PRMs)** | Score each *step* in the chain, not just the final answer | Requires step-level labels — expensive to collect |

Key finding: inference scaling can recover a significant portion of next-scale-up training gains on reasoning benchmarks.

## RLHF — Reinforcement Learning from Human Feedback

Training loop for alignment:

1. **SFT (Supervised Fine-Tuning):** Fine-tune base LLM on curated demonstrations
2. **Reward Model:** Train a separate model to predict human preference scores on pairs of outputs
3. **PPO (Proximal Policy Optimization):** Optimize the LLM with respect to the reward model, KL-penalized against the SFT model

> KL penalty: prevents the policy from deviating too far from the SFT model (reward hacking / distribution collapse).

**RLHF variants:**
- **DPO (Direct Preference Optimization):** Eliminates the explicit reward model — optimizes preference directly from paired data. Simpler, more stable than PPO in practice.
- **GRPO (Group Relative Policy Optimization):** DeepSeek's variant — eliminates value/critic model, uses group-level relative rewards. Used in DeepSeek-R1.

## Scaling Laws for Reasoning

- **Chinchilla scaling** applies to pre-training compute vs. model loss
- **Reasoning tasks** show a different curve — benefit more from inference compute than non-reasoning tasks
- **OpenAI o1 paradigm:** spend more tokens on "thinking" (hidden scratchpad CoT) at inference — trading latency for accuracy on hard tasks

## Links

- [[attention-mechanisms]] — transformer architecture underlying all LLMs
- [[deep-learning]] — domain
- [[lora-qlora]] — PEFT used to fine-tune LLMs efficiently
- [[vlmverse]] — VLM fine-tuning with alignment considerations
