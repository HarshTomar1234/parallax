# CLAUDE.md — Parallax Wiki

> Read this before touching anything. It overrides all defaults.

---

## Project Identity

**Parallax** is a persistent, LLM-compiled knowledge graph for **Harsh Tomar (@kernel_crush)**, an AI/ML Engineer.

- **Live site:** https://harshtomar1234.github.io/parallax/
- **Repo:** https://github.com/HarshTomar1234/parallax
- **Owner:** Harsh Tomar | tomarharsh28303@gmail.com
- **Local path:** `D:/LLM-wiki/`
- **Pattern:** Karpathy-style compiled-truth + timeline wiki

This is not a portfolio. It is a living knowledge system that compounds over time. Every page is interlinked, every concept cross-referenced, and the graph is designed to be navigated by both humans and AI.

---

## Repository Structure

```
parallax/
├── wiki/                    # Core knowledge graph (39 pages) — primary artifact
│   ├── index.md             # Master entry point — read first before any wiki change
│   ├── overview.md          # High-level identity and stats
│   ├── log.md               # Append-only activity log — never edit past entries
│   ├── projects/            # 10 production systems (deployed, real metrics)
│   ├── research/            # 5 from-scratch paper/method implementations
│   ├── skills/              # 4 skill domain pages (CV, GenAI, MLOps, DL)
│   ├── concepts/            # 6 deep-dive AI/ML concept pages
│   ├── career/              # Career timeline, internship, contributions
│   ├── learning/            # 3 learning repository pages
│   ├── meta/                # synthesis, connections, knowledge-gaps
│   ├── _templates/          # Page template — do not treat as content page
│   ├── llms.txt             # AUTO-GENERATED — never hand-edit
│   ├── llms-full.txt        # AUTO-GENERATED — never hand-edit
│   ├── graph.json           # AUTO-GENERATED — never hand-edit
│   └── search-index.json    # AUTO-GENERATED — never hand-edit
├── pages/                   # Deep-dive standalone pages (not in main wiki graph)
│   └── tools/gbrain.md      # Detailed GBrain notes (external tool coverage)
├── mcp/                     # MCP server — wiki as callable tools
│   ├── server.py            # FastMCP server (5 tools)
│   └── requirements.txt     # mcp>=1.0.0
├── landing/                 # Static SPA (Vanilla HTML/CSS/JS)
│   ├── index.html           # Shell with sidebar, topbar, graph overlay
│   ├── style.css            # Obsidian-inspired dark/light theme
│   └── script.js            # Markdown renderer, D3 graph, command palette
├── raw/                     # Immutable source material — agents read, never write
│   └── resumes/             # Domain-specific PDF resumes
├── _agents/
│   ├── scripts/             # Python health/agent scripts (see Health Stack)
│   │   ├── auto_ingest.py   # Ingest: fetch README → generate wiki page → open PR
│   │   ├── validate_wiki.py # Validate frontmatter, structure
│   │   ├── check_orphans.py # Detect orphan pages and broken [[wikilinks]]
│   │   ├── stale_check.py   # Check star drift + staleness (needs GITHUB_TOKEN)
│   │   └── generate_exports.py  # Regenerate llms.txt, graph.json, search-index.json
│   └── workflows/
│       └── ingest.md        # Manual ingest workflow instructions
├── .github/workflows/
│   ├── deploy-pages.yml     # Auto-deploy to GitHub Pages on push
│   ├── agent-ingest.yml     # workflow_dispatch: fetch repo + generate page + PR
│   ├── wiki-validator.yml   # CI: validate_wiki.py + check_orphans.py on wiki push
│   └── stale-check.yml      # Weekly Sunday: star drift check, opens issue if stale
├── scripts/
│   └── commit.py            # Commit helper script
├── AGENTS.md                # Full agent constitution — authoritative schema
└── README.md
```

---

## Domain and Scope

### Knowledge Domains

| Domain | Description | Pages |
|--------|-------------|-------|
| `projects` | Production deployed systems with real metrics | 10 |
| `research` | From-scratch implementations of papers/architectures | 5 |
| `skills` | Broad skill domain clusters (not individual tools) | 4 |
| `concepts` | Deep mathematical/technical concepts | 6 |
| `career` | Timeline, internships, community contributions | 4 |
| `learning` | Learning repos and coursework | 3 |
| `meta` | Synthesis, cross-domain connections, knowledge gaps | 3 |

### Subject Matter

**Core ML/CV/GenAI domains:**
- Computer Vision: object detection, multi-object tracking, video analysis, rPPG
- Generative AI: LLM agents, RAG architectures, reasoning LLMs, LoRA/QLoRA
- Research implementations: Vision Transformer, PaLiGemma (VLMverse), transformers-cv (11 architectures)
- MLOps: pipelines, deployment, CI/CD for ML systems
- Deep Learning: attention mechanisms, diffusion models, foundation models

**Production projects covered:**
`insureml-pipeline` · `travel-planner` · `tennis-vision` · `quanta-ai` · `deepguard` · `decifra` · `molecuquest` · `field-fusion` · `histopathology` · `rppg-heart-rate`

---

## Tech Stack

**Frontend (landing/):**
- Vanilla HTML/CSS/JS — zero framework dependency by design
- `marked.js` for client-side markdown rendering
- `D3.js v7` for force-directed knowledge graph (drag, zoom, domain colors)
- Pre-built `search-index.json` for full-text search with keyword highlighting
- Hosted via GitHub Pages

**Backend/Tooling:**
- Python 3.11 for all agent scripts
- `FastMCP` for the MCP server (`mcp/server.py`)
- GitHub Actions for CI/CD

**MCP Server (5 tools):**
```bash
# Add to Claude Code
claude mcp add parallax -- python D:/LLM-wiki/mcp/server.py
```
Tools: `search_wiki` · `get_page` · `get_summary` · `get_related` · `list_pages`

---

## Page Format

Every wiki page **must** have this frontmatter:

```yaml
---
title: [Title-case noun phrase — no verbs]
domain: [projects | research | skills | concepts | career | learning | meta]
tags: tag-one, tag-two, tag-three   # 3–6 tags, lowercase, hyphenated, no brackets
sources: [github-url-or-slug]        # never empty []
last_updated: YYYY-MM-DD
confidence: 0.0–1.0                  # see scale below
links: [[wiki-link-one]], [[wiki-link-two]]  # minimum 2 for project/research/concept
---
```

**Confidence scale:**

| Score | Meaning |
|-------|---------|
| 0.9–1.0 | Directly verified from source code / live project / personal experience |
| 0.7–0.89 | From README/docs — accurate but not depth-verified |
| 0.5–0.69 | Synthesized from secondary sources — treat as approximate |
| < 0.5 | Speculative or outdated — flag for re-verification |

---

## Style Rules

These apply to ALL wiki content — agent-generated or human-written:

| Rule | Example |
|------|---------|
| Terse, precise, technical | "95% mAP@0.5" not "strong performance" |
| Real numbers only | "★27 stars" not "popular repo" |
| No filler phrases | Never "This project demonstrates..." |
| Headers = noun phrases | "Architecture" not "How it works" |
| Tables for comparisons | Model variants, performance breakdowns |
| Bullet lists for tech stacks | Categorized by layer |
| No fenced code blocks for architecture | Use bullet lists, tables, blockquotes instead |
| `[[wikilinks]]` for cross-references | Always — never bare text for page names |
| No vague confidence defaults | Don't default-0.8 everything without verifying |

---

## Agent Conventions

### Ingest (adding a new page)

1. Check `wiki/llms.txt` — if slug already present, update don't create
2. Compute slug: `repo_name.lower()`, hyphens only
3. Check `wiki/<domain>/<slug>.md` does not exist
4. Generate page using `_agents/scripts/auto_ingest.py` or manually per template
5. Update `landing/script.js`, `landing/index.html`, `wiki/index.md` via inject markers
6. Append entry to `wiki/log.md`
7. Run `python _agents/scripts/check_orphans.py` — must return 0 orphans
8. Open Pull Request — **never commit directly to `main`**

**Quality gate — FAIL if:**
- Frontmatter missing any required field
- `links: []` is empty on a project/research/concept page
- Body contains fenced code blocks for architecture/tech stack
- Body < 300 chars after stripping frontmatter
- Hallucinated contact info

### After merge

Run `python _agents/scripts/generate_exports.py` to regenerate exports.
(Runs automatically in `deploy-pages.yml`.)

### File conventions

| Path | Rule |
|------|------|
| `wiki/<domain>/<slug>.md` | Slug = lowercase, hyphens only |
| `raw/<domain>/` | Immutable — never write here |
| `wiki/llms.txt` · `graph.json` · `search-index.json` | Auto-generated — never hand-edit |
| `landing/index.html` | Sidebar via `AGENT_INJECT_SIDEBAR_*` markers only |
| `wiki/index.md` | Tables via `AGENT_INJECT_TABLE_*` markers only |
| `wiki/log.md` | Append-only — never delete or edit past entries |
| `phase-reports/` | Local audit artifacts — gitignored, never commit |

### Staleness thresholds

| Domain | Re-verify after |
|--------|----------------|
| `projects` | 90 days |
| `career` | 60 days |
| `meta` | 30 days |
| `research`, `skills` | 180 days |
| `concepts` | 365 days |
| `learning` | 90 days |

---

## Health Stack

Custom health tools for this markdown wiki project:

```yaml
structure:     python _agents/scripts/validate_wiki.py
connectivity:  python _agents/scripts/check_orphans.py
exports:       python _agents/scripts/generate_exports.py
stale:         python _agents/scripts/stale_check.py  # requires GITHUB_TOKEN env var
```

**Known issue in `stale_check.py`:** Contains `→` character (U+2192) that fails on Windows cp1252 console encoding. Run with `PYTHONIOENCODING=utf-8` or use `! PYTHONIOENCODING=utf-8 python _agents/scripts/stale_check.py`.

When running `/health`, use these four scripts instead of tsc/biome/knip (this is not a TypeScript project).

---

## Git and PR Rules

- **Never commit directly to `main`** — always open a PR
- **Never add `Co-Authored-By: Claude ...` to commits**
- **Never add `🤖 Generated with Claude Code` to PR descriptions**
- PR descriptions: use `-` bullet lists, not `- [ ]` checkboxes
- Commit messages: imperative mood, no trailing period
- `wiki/log.md` must be appended after every wiki write

---

## Skill Routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore

---

## One-Sentence Rules for Claude

1. Read `wiki/index.md` before touching any wiki content.
2. Never write a page without frontmatter.
3. Never leave `links: []` on a project, research, or concept page.
4. Never commit directly to `main` — always PR.
5. Always append to `wiki/log.md` after every wiki write operation.
6. Run `check_orphans.py` before committing wiki changes.
7. Update existing pages instead of creating duplicates.
8. When running `/health`, use the Python scripts above — not tsc/biome/bun/knip.
9. The `pages/` directory is separate from `wiki/` — pages there are standalone deep-dives, not in the graph.
10. Auto-generated files (`llms.txt`, `graph.json`, `search-index.json`) are never hand-edited.
