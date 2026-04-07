---
title: Log
domain: meta
tags: log, activity, chronological
sources: []
last_updated: 2026-04-07
links: [[index]]
---

# Parallax — Activity Log

Append-only. Format: `## [YYYY-MM-DD] operation | description`

---

## [2026-04-07] init | Parallax wiki bootstrapped

- Wiki structure created from scratch
- Sources: GitHub profile (67 repos), portfolio site, 6 domain resumes, recommendation letter, internship certificate
- Initial pages compiled: index, overview, tennis-vision, transformers-cv, and all stub pages
- Landing page built and deployed locally: dark minimalist design with particle field, bento grid layout
- AGENTS.md schema written

**Pages created:**
- wiki/index.md
- wiki/overview.md
- wiki/log.md
- wiki/projects/tennis-vision.md
- wiki/research/transformers-cv.md
- wiki/career/ai-internship.md
- wiki/career/open-source.md
- wiki/career/community.md
- wiki/skills/computer-vision.md
- wiki/skills/genai-agents.md
- wiki/skills/mlops.md

**Raw sources seeded:**
- raw/projects/ — 8 production project descriptions
- raw/research/ — 5 research implementations
- raw/career/ — internship, community, open source details

---

## [2026-04-07] ingest | Full wiki content build from source materials

- All 8 production project pages authored from GitHub repos + portfolio
- All 5 research implementation pages built from repo analysis
- Skills, concepts, career, meta sections populated
- 30+ pages total with cross-linked `[[wiki-link]]` references

**Pages created (batch):**
- wiki/projects/ — quanta-ai, deepguard, decifra, molecuquest, field-fusion, histopathology, rppg-heart-rate
- wiki/research/ — vlmverse, lora-qlora, reasoning-llms, vision-transformer
- wiki/skills/ — mlops, genai-agents, computer-vision, deep-learning
- wiki/concepts/ — attention-mechanisms, diffusion-models, rag-architectures, lora-theory
- wiki/career/ — community, open-source
- wiki/meta/ — knowledge-gaps, connections

---

## [2026-04-07] refactor | Native markdown formatting pass

- All code blocks converted to native markdown (lists, blockquotes, tables)
- Removed flowchart-style ASCII diagrams — replaced with numbered prose workflows
- Tech Stack sections restructured into categorized bullet lists
- Full grep scan confirmed zero remaining ``` blocks across all wiki pages

---

## [2026-04-07] feat | Landing page UI + Command Palette

- Built Obsidian-inspired dark UI: sidebar, topbar, content pane
- Implemented Ctrl+K Command Palette with client-side full-text search
- Pre-fetches and indexes all wiki .md files on page load
- Keyword highlighting in search results
- Fixed search Enter-key navigation to directly trigger `loadPage()`

---

## [2026-04-07] fix | Created missing pages resolving 404 links

- Created wiki/skills/deep-learning.md (linked from 6 pages)
- Created wiki/concepts/lora-theory.md (linked from research/lora-qlora)

---

## [2026-04-07] infra | GitHub Actions + real agent scripts wired up

- Created .github/workflows/wiki-validator.yml — runs on every push to wiki/ and weekly on schedule
- Created _agents/scripts/validate_wiki.py — validates frontmatter, domain, required fields
- Created _agents/scripts/check_orphans.py — detects pages with zero inbound links
- Automation now provably runs; not just aspirational

---

## [2026-04-07] docs | README premium overhaul

- Added badges (stars, last-commit, page count, agent-maintained)
- Embedded screenshots of landing page and wiki page
- Added feature table, repo structure tree, knowledge graph listing, quick start
- Added Karpathy attribution

---

## [2026-04-07] ingest | Autonomous run for https://github.com/HarshTomar1234/Travel-Planner via Action
- Auto-generated `wiki/projects/travel-planner.md` using Gemini API

## [2026-04-07] ingest | Autonomous run for https://github.com/HarshTomar1234/InsureML-Pipeline via Action
- Auto-generated `wiki/projects/insureml-pipeline.md`
- Auto-updated `index.html`, `script.js`, and `index.md` registry

## [2026-04-07] ingest | Autonomous run for https://github.com/HarshTomar1234/Computer-Vision via Action
- Auto-generated `wiki/learning/computer-vision.md`
- Auto-updated `index.html`, `script.js`, and `index.md` registry

## [2026-04-07] ingest | Autonomous run for https://github.com/HarshTomar1234/torchquest via Action
- Auto-generated `wiki/learning/torchquest.md`
- Auto-updated `index.html`, `script.js`, and `index.md` registry

## [2026-04-08] ingest | Autonomous run for https://github.com/HarshTomar1234/Machine-and-Deep-Learning-NLP via Action
- Auto-generated `wiki/learning/machine-and-deep-learning-nlp.md`
- Auto-updated `index.html`, `script.js`, and `index.md` registry
