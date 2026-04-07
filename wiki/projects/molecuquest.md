---
title: MoleCuQuest
domain: projects
tags: drug-discovery, molecular-ai, nvidia-nim, rdkit, cma-es, qed, next-js, firebase
sources: [github-molecuquest, portfolio-projects]
last_updated: 2026-04-07
links: [[genai-agents]], [[deep-learning]]
---

# MoleCuQuest

AI-driven molecular research platform combining generative AI with computational chemistry.

- **Repo:** https://github.com/HarshTomar1234/MoleCuQuest

---

## Core Capabilities

| Feature | Detail |
|---------|--------|
| **Molecule Generation** | NVIDIA MolMIM for novel structure generation with desired properties |
| **3D Visualization** | Real-time interactive rendering via RDKit |
| **Chemical Analysis** | PubChem API integration for compound research |
| **Optimization** | CMA-ES (Covariance Matrix Adaptation Evolution Strategy) |
| **Drug-likeness** | QED scoring (Quantitative Estimate of Drug-likeness) |

## Architecture

```
User Input (molecular constraints / targets)
    ↓
NVIDIA MolMIM API  →  novel SMILES generation
    ↓
RDKit              →  3D visualization + property calculation
    ↓
CMA-ES             →  evolutionary optimization toward target properties
    ↓
QED Scoring        →  pharmaceutical viability filter
    ↓
PubChem API        →  cross-reference known compounds
    ↓
Next.js UI + Firebase persistence
```

## Why It Matters

Applies modern generative AI (NIMs) to computational chemistry — a bridge between LLM-era tooling and drug discovery. CMA-ES optimization is notable: it's a derivative-free evolutionary strategy well-suited for optimizing molecular properties in non-differentiable chemical space.

## Tech Stack

```
Python | NVIDIA MolMIM (NIM) | RDKit | Next.js | Firebase | PubChem API | CMA-ES
```

## Links

- [[genai-agents]] — NIM API usage pattern
- [[deep-learning]] — generative model backend
