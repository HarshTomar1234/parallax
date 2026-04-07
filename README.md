<p align="center">
  <h1 align="center">🌌 Parallax</h1>
  <p align="center">
    <strong>A self-organizing, LLM-assisted knowledge base for Machine Learning, Computer Vision, and Generative AI.</strong>
  </p>
  <p align="center">
    <em>Inspired by <a href="https://github.com/karpathy">Andrej Karpathy's</a> minimal LLM Wiki pattern.</em>
  </p>
  <p align="center">
    <a href="https://github.com/HarshTomar1234/parallax"><img src="https://img.shields.io/github/stars/HarshTomar1234/parallax?style=flat-square&color=3b82f6" alt="Stars"></a>
    <a href="https://github.com/HarshTomar1234/parallax/commits/main"><img src="https://img.shields.io/github/last-commit/HarshTomar1234/parallax?style=flat-square&color=22c55e" alt="Last Commit"></a>
    <a href="wiki/index.md"><img src="https://img.shields.io/badge/pages-30%2B-blue?style=flat-square" alt="Pages"></a>
    <a href="AGENTS.md"><img src="https://img.shields.io/badge/agent--assisted-✓-purple?style=flat-square" alt="Agent Assisted"></a>
    <a href="https://harshtomar1234.github.io/parallax/"><img src="https://img.shields.io/badge/live%20demo-→-orange?style=flat-square" alt="Live Demo"></a>
  </p>
  <p align="center">
    <strong><a href="https://harshtomar1234.github.io/parallax/">🌐 harshtomar1234.github.io/parallax</a></strong>
  </p>
</p>

---

## What is Parallax?

Parallax is **not a portfolio**. It is a persistent, compounding knowledge system — a living architectural map maintained by LLM-assisted agentic workflows. Every page is interlinked, every concept cross-referenced, and the entire graph is designed to be navigated by both humans and AI.

**Built for:** [Harsh Tomar (@kernel_crush)](https://github.com/HarshTomar1234) — AI/ML Engineer

---

## Screenshots

<p align="center">
  <img src="images/landing%20page.png" alt="Parallax Landing Page" width="80%">
  <br>
  <em>Landing Page — Dark-mode wiki interface with sidebar navigation & Ctrl+K search</em>
</p>

<p align="center">
  <img src="images/opensource%20page.png" alt="Parallax Open Source Page" width="80%">
  <br>
  <em>Wiki Page — Clean native markdown rendering with interlinked navigation</em>
</p>

---

## Features

| Feature | Description |
|---------|-------------|
| **30+ Interlinked Wiki Pages** | Projects, research implementations, skills, concepts, and career history — all cross-referenced |
| **Ctrl+K Command Palette** | Client-side instant search across the entire knowledge base with keyword highlighting |
| **LLM-Assisted Workflows** | Structured schema for ingesting new repos, generating pages, and validating the knowledge graph |
| **Obsidian-style Dark UI** | Premium dark-mode interface with glassmorphism search, sidebar navigation, and responsive layout |
| **Pure Native Markdown** | Zero code blocks for content — everything renders as clean, professionally formatted documentation |
| **Wiki-style Cross-links** | `[[wiki-link]]` format for seamless cross-referencing between pages |

---

## Repository Structure

```
parallax/
├── wiki/                    # Core knowledge graph
│   ├── index.md             # Master entry point
│   ├── overview.md          # High-level identity & stats
│   ├── log.md               # Append-only activity log
│   ├── projects/            # 8 production system pages
│   ├── research/            # From-scratch implementations
│   ├── skills/              # Skill domain pages (CV, GenAI, MLOps, DL)
│   ├── concepts/            # Deep-dive concept pages
│   ├── career/              # Career timeline & contributions
│   └── meta/                # Knowledge gaps, connection maps
├── landing/                 # Static web interface
│   ├── index.html           # SPA shell with sidebar + topbar
│   ├── style.css            # Obsidian-inspired dark theme
│   └── script.js            # Markdown renderer + Command Palette
├── raw/                     # Immutable source material
│   └── resumes/             # Domain-specific PDF resumes
├── scripts/                 # Utility scripts (e.g. auto-commit)
├── _agents/workflows/       # Agent workflow definitions
├── AGENTS.md                # Agent schema & conventions
└── README.md
```

---

## Knowledge Graph

### Projects (Production Systems)
`tennis-vision` · `quanta-ai` · `deepguard` · `decifra` · `molecuquest` · `field-fusion` · `histopathology` · `rppg-heart-rate`

### Research (From-Scratch Implementations)
`transformers-cv` (11 architectures) · `vlmverse` (PaLiGemma) · `lora-qlora` · `reasoning-llms` · `vision-transformer`

### Skills
`computer-vision` · `genai-agents` · `mlops` · `deep-learning`

### Concepts
`attention-mechanisms` · `diffusion-models` · `rag-architectures` · `lora-theory`

---

## Agentic Workflows

The repository utilizes an LLM-assisted workflow system defined in [`AGENTS.md`](AGENTS.md). Rather than fully autonomous black-box agents, this repository uses explicit prompts and scripts to assist the human creator in:

- **Ingestion** — Reading new sources (GitHub repos, papers) to generate structured wiki pages
- **Querying** — Synthesizing answers from the knowledge graph
- **Linting** — Detecting orphan pages, missing cross-references, and stale metrics

Trigger ingestion via the `/ingest` workflow defined in `_agents/workflows/ingest.md`.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/HarshTomar1234/parallax.git
cd parallax

# Serve locally
python -m http.server 8000

# Open in browser
# http://localhost:8000/landing/index.html
```

Or start reading directly: **[wiki/index.md](wiki/index.md)**

---

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JS, Inter + JetBrains Mono fonts
- **Rendering:** marked.js (client-side markdown → HTML)
- **Search:** Custom client-side indexer with keyword highlighting
- **Agents:** LLM-assisted workflows via AGENTS.md schema
- **Hosting:** Static files — auto-deployed to GitHub Pages via CI/CD

> *Note: The choice of a lightweight Vanilla HTML/JS stack with client-side indexing is a deliberate architectural decision. It prioritizes extreme simplicity, portability, and decades-long resilience over modern framework complexity.*

---

<p align="center">
  <strong>Built with 🧠 by <a href="https://github.com/HarshTomar1234">@kernel_crush</a></strong>
  <br>
  <a href="https://harshtomar1234.github.io/parallax/">Live Wiki</a> · <a href="https://kernel-crush.netlify.app">Portfolio</a> · <a href="https://www.linkedin.com/in/harsh-tomar-a96a38256/">LinkedIn</a> · <a href="https://x.com/kernel_crush">X</a>
</p>
