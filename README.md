# Parallax

> A personal AI-maintained knowledge base for @kernel_crush.

**Live:** `d:\LLM-wiki\landing\index.html` (serve with `python -m http.server 5500 --directory landing`)

---

## Structure

```
parallax/
├── landing/          # Web landing page (HTML/CSS/JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── wiki/             # AI-maintained knowledge base
│   ├── index.md      # START HERE — master navigation
│   ├── log.md        # Append-only activity log
│   ├── overview.md   # Who is kernel_crush
│   ├── projects/     # 8 production system pages
│   ├── research/     # Research implementation pages
│   ├── skills/       # Skill domain pages
│   ├── concepts/     # AI/ML concept deep-dives
│   ├── career/       # Work experience, contributions
│   └── meta/         # Knowledge gaps, connections
├── raw/              # Immutable source material
├── AGENTS.md         # LLM agent schema (READ THIS FIRST)
└── llm-wiki.md       # Karpathy's reference architecture
```

## Quick Commands

```bash
# Serve landing page locally
python -m http.server 5500 --directory landing

# View wiki index
cat wiki/index.md

# Add a new source and ingest
# Drop file in raw/ then run ingest prompt from AGENTS.md
```

## Maintenance (Antigravity / Claude Code)

When running an agent on this wiki:
1. Read `AGENTS.md` first — it defines the schema and operations
2. Read `wiki/index.md` to understand the current state
3. Follow the Ingest / Query / Lint operations defined there

## Design

- **Name:** Parallax
- **Tagline:** Knowledge, from a different angle
- **Color:** Cyan (`#38bdf8`) on deep dark (`#080a0e`)
- **Font:** Inter + JetBrains Mono
- **Inspiration:** Karpathy's LLM Wiki pattern
