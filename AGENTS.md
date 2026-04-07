# AGENTS.md — Parallax Wiki Schema

## Identity
This is **Parallax** — a personal LLM-assisted knowledge base for @kernel_crush (Harsh Tomar), an AI/ML Engineer.

The wiki's purpose is to serve as a persistent, compounding knowledge base — supported iteratively via LLM-assisted workflows, navigated by both humans and AI. Not a portfolio. A living knowledge system.

## Wiki Structure

```
wiki/
├── index.md           # Master entry point — always read this first
├── log.md             # Append-only activity log
├── overview.md        # High-level synthesis of the owner's work & identity
├── projects/          # One page per production project
├── research/          # Research implementations and paper deep-dives
├── skills/            # Skill domain pages
├── concepts/          # AI/ML concepts with depth
├── career/            # Career timeline, experience, contributions
└── meta/              # Knowledge gaps, contradictions, connection maps
```

## Page Format

Every wiki page MUST include this frontmatter:
```yaml
---
title: [Page Title]
domain: [projects | research | skills | concepts | career | meta]
tags: [comma-separated tags]
sources: [list of source files that contributed to this page]
last_updated: [YYYY-MM-DD]
links: [list of [[wiki-links]] to related pages]
---
```

## Conventions

- Use `[[wiki-link]]` format for cross-references between pages
- Every project page MUST link to its skill domains and any related concept pages
- Every concept page MUST link to projects where it was applied
- Use code blocks for technical specs, numbers, and metrics
- Be precise — include real numbers (accuracy %, GitHub stars, dataset sizes) not vague terms

## Operations

### Ingest
When triggered via the **LLM Auto-Ingest** GitHub Action:
1. Agent securely fetches the remote repository (e.g., GitHub README)
2. Content is routed via the Gemini API with strict Parallax schema constraints
3. Generate native Markdown `.md` page (NO wrapping codeblocks)
4. Create an automatic Pull Request under `wiki/projects` or `wiki/research`
5. A human (you) reviews the PR, updates index/log, and merges

### Query
When asked a question:
1. Read `wiki/index.md` to identify relevant pages
2. Read those pages
3. Synthesize an answer
4. If the answer is substantive, file it back as a new wiki page

### Lint
Periodically check for:
- Orphan pages (no inbound links)
- Missing cross-references
- Stale metrics that should be updated
- Concepts mentioned but without their own page

## Style Guidelines

- Terse, precise, technical — no fluff
- Use tables for comparisons
- Use bullet points for lists of specs/features
- Headers should be noun phrases, not full sentences
- Avoid filler phrases like "this is a" or "this project demonstrates"
