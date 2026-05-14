---
type: tool
title: GBrain — Garry Tan's AI Agent Brain
tags: [agent-memory, knowledge-graph, pgvector, rag, mcp, openclaw, hermes, yc, garry-tan, skills, compiled-truth]
created: 2026-05-14
status: active
source: https://github.com/garrytan/gbrain
stars: ~15,470 (as of 2026-05-14)
version: 0.33.1.1
license: MIT
---

## Compiled Truth

GBrain is Garry Tan's (President & CEO of Y Combinator) open-source "opinionated AI agent brain" — a persistent, self-wiring knowledge system built on Postgres + pgvector + Bun/TypeScript that gives AI agents (OpenClaw, Hermes, Claude Code, etc.) long-term memory over thousands of markdown files. It is not "chat with your notes." It is a compiled intelligence system — each page is an intelligence assessment with a current best understanding ("compiled truth") rewritten on new evidence, and an append-only evidence trail ("timeline") below. The brain wires itself: every page write extracts typed entity links (`attended`, `works_at`, `invested_in`, `founded`, `advises`) with zero LLM calls. Benchmarked at **P@5 49.1%, R@5 97.9%** on a 240-page corpus, beating graph-disabled variant by +31.4 points on precision.

**Garry's production stats (built in 12 days):** 17,888 pages · 4,383 people · 723 companies · 21 autonomous cron jobs. The brain ingests meetings, emails, tweets, voice calls, original ideas while you sleep. You wake up and the brain is smarter.

**Direct connection to this project:** GBrain's GBRAIN_V0.md explicitly cites "Karpathy-style knowledge pages" as the right model for personal knowledge at scale — the exact same pattern this wiki uses. GBrain was built to solve the *database scaling problem* when that pattern hits 5,000+ files (git chokes). The compiled-truth + timeline structure you see in this wiki is the same pattern GBrain was designed to accelerate with a proper retrieval backend.

---

## Timeline

- **2026-04-05** — Open-sourced under MIT license. 5,400+ stars in first 24 hours.
- **2026-04-09** — "Thin Harness, Fat Skills" essay published (linked to YC Spring 2026 talk).
- **2026-04-11** — "Homebrew for Personal AI" essay published.
- **2026-04-15** — Minions (universal agent orchestration via Postgres job queue) design completed.
- **2026-04-18** — Knowledge Runtime design doc published. gbrain-evals sibling repo launched.
- **2026-05-10** — v0.33.1.0: `gbrain whoknows <topic>` command added. Expert-in-network queries.
- **2026-05-13** — v0.33.1.1: Voyage 2048-dim embedding fix. Community-contributed fix (@100yenadmin).
- **2026-05-14** — 15,470 stars, 2,059 forks. Updated same day as this note.

---

## Origin & Context

### Who Built It

Garry Tan is President & CEO of Y Combinator (world's most prominent startup accelerator — funded Airbnb, Stripe, OpenAI, Dropbox, etc.). Before YC he co-founded Initialized Capital (early Coinbase, Instacart, Reddit, Cruise). Former designer at Posterous, Palantir.

He is a prolific builder in the 2026 AI era. His 2026 run rate on logical code change is **~810× his 2013 pace** (11,417 vs 14 logical lines/day). In the last 60 days before GBrain's release: 3 production services + 40+ shipped features, part-time while running YC full-time.

### The Problem It Solves

A 7,471-file / 2.3GB markdown wiki **chokes git**. Git doesn't scale past ~5K files for wiki-style use. The Karpathy-style compiled-truth + timeline model is right, but needs a real database underneath. GBrain ports patterns from a production-grade Ruby on Rails RAG system (3-tier chunking, hybrid search with RRF, multi-query expansion, 4-layer dedup) to a standalone Bun + TypeScript tool.

### The Ecosystem

GBrain exists in a three-repo ecosystem by Garry Tan:
- **gbrain** — the brain/knowledge layer (this document)
- **gstack** — Claude Code setup: 23 opinionated tools serving as CEO, Designer, Eng Manager, Release Manager, Doc Engineer, QA. The "coding brain."
- **OpenClaw** / **Hermes** — the AI agent harnesses that use gbrain as their knowledge backend

**GStack is the playbook. OpenClaw runs the agents. GBrain is what they know.**

---

## Core Architecture

Three distribution modes wrap the same `BrainEngine` interface:

```
+-------------------+     +-------------------+     +-------------------+
|   npm package     |     |  Compiled binary  |     |   MCP server      |
|   (library)       |     |  (CLI)            |     |   (stdio/HTTP)    |
+-------------------+     +-------------------+     +-------------------+
| bun add gbrain    |     | GitHub Releases   |     | gbrain serve      |
| WHO: OpenClaw,    |     | WHO: Humans       |     | WHO: Claude Code, |
|      Hermes       |     |                   |     |  Cursor, ChatGPT  |
+-------------------+     +-------------------+     +-------------------+
         |                         |                         |
         +-------------------------+-------------------------+
                                   |
                          +--------v--------+
                          |  BrainEngine    |
                          |  (pluggable     |
                          |   interface)    |
                          +-----------------+
                     +-------------+-------------+
                     |                           |
              +------v------+            +-------v-------+
              | Postgres    |            | PGLite        |
              | Engine      |            | Engine        |
              | (default)   |            | (zero-config) |
              +-------------+            +---------------+
```

### Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Database | Postgres + pgvector | World-class hybrid search: tsvector, HNSW, pg_trgm |
| Zero-config mode | PGLite (WebAssembly Postgres) | `gbrain init` with no external deps |
| Hosting | Supabase Pro ($25/mo) | Zero-ops. 8GB. Managed pgvector. |
| Runtime | Bun + TypeScript | GStack ecosystem. Fast. Compiles to binary. |
| Embeddings | OpenAI text-embedding-3-large OR Voyage | 1536 dims (reduced from 3072). ~$0.13/1M tokens |
| LLM (chunking/expansion) | Claude Haiku | Cheapest for topic boundary detection + query expansion |
| Background jobs | Minions (Postgres-native job queue) | See §Minions below |
| Distribution | npm + binary + MCP | Library + CLI + agent protocol |

---

## The Knowledge Model

The core insight: **personal knowledge at scale is an intelligence problem, not a storage problem.**

### Page Structure: Compiled Truth + Timeline

Every brain page has two zones:

```markdown
---
type: person
title: Sarah Chen
tags: [engineering, acme-corp]
---

## Executive Summary
One paragraph. How you know them, why they matter.

## State
VP Engineering at Acme Corp. Managing 45-person team.

## What They Believe
Strong opinions on test coverage. "Ship it when the tests pass."

## Assessment
Sharp technical leader. Under-appreciated internally. Watch for burnout.

## Trajectory
Ascending. Likely CTO track if the migration succeeds.

---

## Timeline

- **2026-04-07** | Met at team sync. Discussed API migration timeline.
  [Source: Meeting notes, 2026-04-07 2:00 PM PT]
- **2026-04-03** | Mentioned in email re Q2 planning.
  [Source: Gmail, sarah@acmecorp.com, 2026-04-03 10:30 AM PT]
```

**Two rules:**
| Zone | Action | Explanation |
|------|--------|-------------|
| Compiled truth | **REWRITE** | Current synthesis. Changes when evidence changes. |
| Timeline | **APPEND ONLY** | Evidence trail. Never edited, only added to. |

**Assessment is the value.** "Sharp technical leader" is something no API can provide — it's YOUR read. That's what makes a brain page better than LinkedIn.

### Database Schema (9 tables)

```
pages          → compiled_truth + timeline + frontmatter (JSONB) + search_vector
content_chunks → 3-tier chunks + embedding (1536 dims via HNSW)
links          → typed edges: attended | works_at | invested_in | founded | advises
tags           → page tagging
timeline_entries → structured timeline (normalized from the text column)
raw_data       → original API responses stored for re-processing
page_versions  → full snapshots (gbrain history / diff / revert)
ingest_log     → provenance of all ingestion runs
config         → key-value brain configuration
```

**Indexes:** GIN on search_vector, GIN on frontmatter (JSONB), HNSW on embeddings (cosine), pg_trgm on title for fuzzy slug resolution.

### Self-Wiring Knowledge Graph

Entity extraction is **deterministic (zero LLM calls)**. Pattern matching on every page write:
- Detects: person names, company names, org affiliations
- Creates typed links automatically: `attended`, `works_at`, `invested_in`, `founded`, `advises`
- `gbrain graph <slug> --depth 5` traverses via recursive CTE

---

## Search Architecture

```
Query: "when should you ignore conventional wisdom?"
           |
           v
+---------------------+
| Multi-query expansion|  (Claude Haiku, optional)
| → "contrarian thinking"
| → "going against the crowd"
+---------------------+
     |   |   |
  [embed all 3 queries]
     +---+---+
         |
    +----+----+
    |         |
    v         v
+--------+ +--------+
| Vector | | Keyword|
| HNSW   | | tsvector|
| cosine | | ts_rank |
+--------+ +--------+
    |         |
+------------------+
| RRF Fusion       |
| score = sum(     |
|   1/(60 + rank)) |
+------------------+
         |
+------------------+
| 4-Layer Dedup    |
| 1. By source     |
| 2. Cosine > 0.85 |
| 3. Type cap 60%  |
| 4. Per-page max  |
+------------------+
         |
+------------------+
| Stale alerts     |
| (compiled_truth  |
|  older than      |
|  latest timeline)|
+------------------+
```

**Three search modes:**
| Mode | When to use |
|------|-------------|
| `gbrain search "term"` | Keyword / tsvector — exact terms |
| `gbrain query "question"` | Hybrid RRF — best for natural language |
| `gbrain get <slug>` | Direct — when you know the slug |

**New in v0.33.1:** `gbrain whoknows "topic"` — finds the top 5 people/companies in your network who know about a subject. Ranking formula: `log(1 + match) × exp(-days/180) × (0.5 + 0.5 × salience)`. Use `--explain` to see the factor breakdown.

### Chunking Strategies

| Strategy | When to use | Algorithm |
|----------|-------------|-----------|
| **Semantic** | Compiled truth | Embed each sentence, Savitzky-Golay filter for topic boundaries |
| **Recursive** | Timeline | 5-level delimiter hierarchy, 300-word chunks, 50-word overlap |
| **LLM-guided** | Explicitly requested | Claude Haiku finds topic shifts in sliding windows |

---

## The Skills System

This is the heart of GBrain's philosophy.

**A skill file is a fat markdown document that encodes an entire workflow: when to fire, what to check, how to chain with other skills, what quality bar to enforce. No skill logic is in the binary.**

Skills are markdown procedures the AI agent reads and follows. They are simultaneously:
1. **Documentation** for humans reading them
2. **Specification** for the implementing agent
3. **Package** for the distribution system
4. **Source code** for the resulting capability

*"Markdown is code."*

### The 34 Built-in Skills (selected)

| Skill | What It Does |
|-------|-------------|
| `skills/ingest/SKILL.md` | Ingest meetings, docs, articles → compiled truth + timeline + links |
| `skills/query/SKILL.md` | 3-layer search (FTS + vector + structured). Synthesize with citations. |
| `skills/maintain/SKILL.md` | Find contradictions, stale info, orphans, dead links, tag inconsistency |
| `skills/enrich/SKILL.md` | Enrich from Crustdata, Happenstance, Exa. Store raw data, distill to compiled truth. |
| `skills/briefing/SKILL.md` | Daily briefing: meetings with context, active deals, open threads |
| `skills/migrate/SKILL.md` | Universal migration from Obsidian, Notion, Logseq, plain markdown, CSV, JSON, Roam |
| `skills/cold-start/SKILL.md` | Day-one bootstrapping: contacts, calendar, email, conversations, social, archives |
| `skills/RESOLVER.md` | Routing table — which skill to read for which task |

**RESOLVER.md is the dispatcher.** Claude Code has a built-in resolver — skills have description fields and the model matches user intent automatically. *"You never have to remember `/ship` exists. The description IS the resolver."*

### Skill as Method Call

```
/enrich-founder(TARGET="Maria Santos", QUESTION="is she building what she says?", DATASET="applications+github+1:1 transcripts")
/enrich-founder(TARGET="Pedro Kim", QUESTION="what sector is he really in?", DATASET="same")
```

Same skill, different parameters → radically different output. This is **software design using markdown as the programming language and human judgment as the runtime.**

---

## "Thin Harness, Fat Skills" Philosophy

From Garry's YC Spring 2026 talk:

> *"The 2x people and the 100x people are using the same models. The difference is five concepts that fit on an index card."*

On March 31, 2026, Anthropic accidentally shipped Claude Code's source code to npm (512,000 lines). Garry's read: *"The secret sauce isn't the model. It's the thing wrapping the model: the harness."*

**The Anti-Pattern:** Fat harness, thin skills — 40+ tool definitions eating half the context window. God tools with 2-5 second MCP round-trips. REST API wrappers for every endpoint.

**The Right Pattern:** Thin harness (200 lines, file I/O + tool dispatch + context management + safety), fat skills (markdown procedures encoding judgment).

### The 5 Definitions

1. **Skill File** — reusable markdown procedure teaching the model HOW to do something, not WHAT. Works like a method call with parameters.
2. **Harness** — the program running the LLM loop. Four jobs: run model, read/write files, manage context, enforce safety. That's the "thin."
3. **Resolver** — routing table for context. When task type X appears, load document Y first. Not a menu — a trigger.
4. **Latent vs. Deterministic** — latent space is where intelligence lives (judgment, synthesis). Deterministic is where trust lives (SQL, code, same input = same output). Wrong layer = failure.
5. **Diarization** — model reads 50 documents, writes 1 structured intelligence page. No SQL query produces this. No RAG pipeline produces this.

### Three Layers

```
Fat skills         (top — 90% of the value, where intelligence lives)
Thin CLI harness   (middle — ~200 lines, dispatch + context)
Your app           (bottom — QueryDB, ReadDoc, Search, deterministic foundation)
```

Push intelligence UP into skills. Push execution DOWN into deterministic tooling. Keep the harness THIN.

---

## "Homebrew for Personal AI" — Markdown as Code

Sequel to Thin Harness. The distribution corollary.

Traditional package managers distribute artifacts (binaries, source tarballs). GBrain distributes **recipes**: markdown files describing capabilities with enough specificity that an AI agent implements them from scratch. No dependency hell. No version conflicts. No transitive vulnerability chains. Because there is no upstream code — just a description of what to build and why.

```bash
gbrain install voice-agent
```

The agent reads the markdown spec and builds the Twilio integration, WebSocket server, Telegram bot hooks, brain lookup — all shaped to whatever infrastructure you already have.

**A good recipe has five sections:**
1. Architecture — component diagram (what talks to what)
2. Routing logic — decision tree (when X, do Y)
3. Integration points — external systems named
4. Judgment calls — the hard part, actual value
5. Failure modes — what goes wrong and what to do

**The moat is taste, not code.** Best AI agent setups will be open source by default. Closed configs are competing against someone publishing a recipe that 1,000 agents implement overnight. The recipe propagates at the speed of a git push.

---

## The Brain-Agent Loop

The read-write cycle that makes the brain compound over time:

```
Signal arrives (message, meeting, email, tweet, link)
    │
    ▼
DETECT entities (people, companies, concepts, original thinking)
    │  → spawn sub-agent
    ▼
READ: check brain FIRST (before responding)
    │  → gbrain search "{entity name}"
    │  → gbrain query "what do we know about {topic}"
    ▼
RESPOND with brain context (every answer is better with context)
    ▼
WRITE: update brain pages (new info → compiled truth + timeline)
    │  → gbrain put {slug}
    │  → add_timeline_entry
    │  → add_link (cross-reference)
    ▼
SYNC: gbrain indexes changes
    ▼
(next signal arrives — agent is now smarter)
```

**Two invariants:**
1. Every READ improves the response — if you answered about a person without checking their brain page, you gave a worse answer.
2. Every WRITE improves future reads — if a meeting mentioned new info and you didn't update the page, you created a gap that will bite you later.

---

## The Enrichment Pipeline

7-step protocol with **tiered spend** — full pipeline for key people, light touch for passing mentions:

| Tier | Triggered by | API calls | Sources |
|------|-------------|-----------|---------|
| Tier 1 | Key people, inner circle, portfolio | 10-15 | Crustdata, Happenstance, Circleback, Captain, Twitter, LinkedIn, Google Contacts |
| Tier 2 | Notable people, occasional interactions | 3-5 | Web search + social + brain cross-reference |
| Tier 3 | Minor mentions, everyone worth tracking | 1-2 | Brain cross-reference + social if handle known |

**The philosophy:** A brain page should read like an intelligence dossier crossed with a therapist's notes, not a LinkedIn scrape.
- What they believe (ideology, worldview)
- What they're building (current projects)
- What motivates them (ambition drivers)
- What makes them emotional (angry, excited, defensive, proud)
- Their trajectory (ascending, plateauing, pivoting, declining)
- Hard facts (table stakes)

**Facts are table stakes. Texture is the value.**

**Key rule:** Twitter/X is the most underrated data source. Tweets reveal beliefs, what they're building, hobby horses, network (reply patterns), trajectory (posting frequency, tone shifts). Richer than LinkedIn for the "What They Believe" section.

---

## Minions — Agent Orchestration Protocol

GBrain's Postgres-native job queue (added ~v0.11). The vision: *"GBrain IS the agent control plane."*

**The core insight:** Separate deterministic work (API fetch, token refresh, scrape+write) from judgment work (triage, assessment, enrichment). Deterministic jobs run **zero LLM tokens**, survive restarts, execute in milliseconds.

### Schema

```sql
minion_jobs: id, name, queue, status, data (JSONB), progress (JSONB),
             tokens_input, tokens_output, tokens_cache_read,
             parent_job_id (for DAGs), lock_token, attempts_made,
             inbox (separate table), stacktrace (transcript)

minion_inbox: per-job sidechannel messaging (read receipts via read_at)
```

### Job States
`waiting → active → completed/failed/dead/cancelled/paused`

### Key Features
- **pg LISTEN/NOTIFY** — sub-second event delivery vs 5s polling (PGLite falls back to polling)
- **Structured progress** — `{step, total, message, tokens_in, tokens_out, last_tool}`
- **Token accounting** — accumulates per job + rollup to parent job
- **Inbox sidechannel** — steer running agents mid-flight with typed messages
- **Session transcripts** — full audit trail of every agent run
- **Resource governor** — CPU/memory-aware concurrency management, circuit breaker at 90% memory
- **Job replay** — `replayJob(id, overrides?)` for debugging failures
- **AbortController integration** — clean pause/resume without duplicate execution

### Shell Jobs (v0.14.0+)

Deterministic crons (API fetch, token refresh, scrape+write) moved off the LLM gateway:
> "Zero tokens per fire, ~60% gateway headroom."

---

## Brains & Sources — Multi-Brain Topology

Two orthogonal axes:
- **Brain** = a database (PGLite file, self-hosted Postgres, or Supabase)
- **Source** = a named content repo *inside* a brain

```
gbrain query "X"              → host brain, default source
gbrain query "X" --brain team → team's brain
gbrain query "X" --source gstack → different repo within same brain
```

**Resolution precedence (same pattern for both axes):**
1. `--brain` / `--source` flag
2. `GBRAIN_BRAIN_ID` / `GBRAIN_SOURCE` env var
3. `.gbrain-mount` / `.gbrain-source` dotfile in directory
4. Longest-prefix path match
5. `sources.default` config
6. Fallback: `host` / `default`

**Rule of thumb:** If the data owner changes → brain boundary. Same owner, different topic → source boundary.

**Cross-brain federation is the agent's job**, not the DB's. The agent has the brain list (`gbrain mounts list`), decides when to fan out, synthesizes findings, cites `brain:source:slug`.

---

## Integrations System — Senses & Reflexes

**Senses** (data inputs): voice-to-brain, email-to-brain, x-to-brain, calendar-to-brain, meeting-sync, photos-to-brain
**Reflexes** (automated responses): meeting-prep, entity-enrich, dream-cycle, deal-tracker, follow-up-nudge

The `gbrain integrations` dashboard:
```
$ gbrain integrations
  SENSES                                        STATUS
  voice-to-brain    Phone calls -> brain pages  ACTIVE    last call: 2h ago
  email-to-brain    Gmail -> entity updates     ACTIVE    47 emails today
  x-to-brain        Twitter -> media pages      ACTIVE    312 tweets tracked

  REFLEXES                                      STATUS
  dream-cycle       Overnight brain maintenance ACTIVE    last run: 3am
  entity-enrich     Auto-enrich new contacts    ACTIVE    12 enriched today

  This week: 1,247 signals ingested. 34 new entity pages.
```

Recipes are distributed as YAML frontmatter + markdown body — the agent reads the spec and builds it. No Docker, no npm packages. The markdown IS the installer.

---

## Brain vs Memory vs Session

Critical routing rule — three layers, three purposes:

| Information type | Goes in |
|-----------------|---------|
| Facts about the world: people, companies, deals, meetings, concepts | **GBrain** — world knowledge, durable |
| How the agent operates: preferences, tool config, session continuity | **Agent memory** — operational state |
| What was just said, current task | **Session context** — already in window |

**Common mistakes:**
- Don't store people in agent memory ("Pedro prefers email" → that's a fact about Pedro, goes in GBrain on his page)
- Don't store user preferences in GBrain (goes in agent memory)
- Agent memory doesn't survive resets on some platforms — critical world knowledge MUST be in GBrain

---

## Performance & Benchmarks

**BrainBench** (240-page Opus-generated rich-prose corpus):
- **P@5: 49.1%** (precision at 5)
- **R@5: 97.9%** (recall at 5)
- Beats graph-disabled variant by **+31.4 points P@5**
- Beats ripgrep-BM25 + vector-only RAG by similar margin
- The graph layer + v0.12 extract quality together carry the gap

Full scorecards in sibling repo: [gbrain-evals](https://github.com/garrytan/gbrain-evals)

**Storage estimate for 7,471 pages:**
| Component | Size |
|-----------|------|
| Page text | ~150MB |
| Embeddings (22K × 1536 × 4 bytes) | ~134MB |
| HNSW index (~2× embeddings) | ~270MB |
| Chunks, indexes, links, versions | ~200MB |
| **Total** | **~750MB** |

**Initial embedding cost for 7,471 pages: ~$4-5.** Budget alternative: `--chunker recursive` first, upgrade to semantic later.

---

## CLI Reference (Key Commands)

```bash
gbrain init                     # Create brain (PGLite default, Supabase for 1000+ files)
gbrain import <dir>             # Import markdown directory (auto-chunk + embed)
gbrain query "question"         # Hybrid search (vector + keyword + RRF)
gbrain search "term"            # Keyword search (tsvector)
gbrain get <slug>               # Read page by slug
gbrain put <slug>               # Write/update page
gbrain whoknows "topic"         # Who in your network knows about this?
gbrain whoknows "topic" --explain  # Show ranking factors
gbrain graph <slug> --depth 5  # Traverse link graph (recursive CTE)
gbrain backlinks <slug>         # Incoming links
gbrain recall --since-last-run --pending --rollup  # Morning pulse
gbrain recall --watch 60        # Watch mode (refresh every 60s)
gbrain doctor                   # Brain health dashboard
gbrain doctor --fix             # Auto-fix issues
gbrain health                   # Stats: page count, embed coverage, orphans
gbrain embed --stale            # Re-embed stale pages
gbrain sync                     # Sync local markdown repo to index
gbrain serve                    # MCP server (stdio)
gbrain upgrade                  # Self-update (npm / binary / ClawHub)
gbrain apply-migrations         # Run skill migration files
```

---

## Trust Boundary & Security

GBrain distinguishes:
- **Trusted local CLI callers** (`OperationContext.remote = false`, set by `src/cli.ts`)
- **Untrusted agent-facing callers** (`remote = true`, set by `src/mcp/server.ts`)

Security-sensitive operations like `file_upload` tighten filesystem confinement when `remote = true`. MCP stdio transport is inherently local (client spawns `gbrain serve` as subprocess). No multi-user, no RLS, no OAuth in v0 single-user mode.

**Privacy rule (contributors):** Never commit real names of people, companies, or funds into public artifacts. Use generic placeholders (`alice-example`, `acme-example`, `fund-a`). GBrain pages reference real contacts; public docs must not.

---

## What People Are Saying

### Garry Tan's Own Words (X / Twitter)

> *"If you want your OpenClaw or Hermes Agent to be able to have perfect total recall of all 10,000+ markdown files, GBrain is here to help. It's exactly my OpenClaw/Hermes Agent setup. MIT-licensed open source. Hope it helps you build your mini-AGI."* — [@garrytan](https://x.com/garrytan/status/2042497872114090069)

> *"GBrain is my attempt to be in control of my own personal AI that could become my intentionally designed cognitive armor. Open source open prompts means you aren't under the API line. It's more important to be above the API line now than ever."* — [@garrytan](https://x.com/garrytan/status/2043075944743923845)

> *"GBrain v0.10.0 is a big one. My personal OpenClaw setup and brain can now be yours. I've perfected my RESOLVER.md, my SOUL.md and ACLs for multi-user brain access. Now there are 24 distinct fat skills with fat code, fully tested with e2e tests, evals and unit tests."* — [@garrytan](https://x.com/garrytan/status/2044291663213015491)

> *"Hi, I might give it away as open source (it's called GBrain)"* — [@garrytan](https://x.com/garrytan/status/2044945773541089321) *(early tease)*

### From Community Builders

- One builder running the same setup tweeted an example: asked his agent "who is A?" and it pulled 108 emails, 91 meetings, inferred the person's role from five years of behavioral patterns.
- A common mistake in community posts: treating gbrain as "memory" (like a chat context). It's a **library** — world knowledge that persists durably, not operational state. Confusing these leads to disappointment.
- HN thread reaction from `flawn`: *"He is living the AI Psychosis"* (skeptical of the scope/ambition)
- `fileoffset` on HN: *"If you think for a living, you should know who Pedro is"* (supportive reference to real use case)
- X Community `GBRAIN Community`: 43 members as of research date
- Technical analysis (Fenado AI): "GBrain Leverages Git and Postgres for Robust Multi-Agent AI Memory" — highlighting the git + postgres dual-layer approach as novel

### Steve Yegge Quote (cited by Garry in "Thin Harness, Fat Skills")

> *"People using AI coding agents are 10x to 100x as productive as engineers using Cursor and chat today, and roughly 1000x as productive as Googlers were back in 2005."*

Garry's commentary: *"The 2x people and the 100x people are using the same models. The difference is five concepts that fit on an index card."*

---

## How This Connects to This Wiki (Parallax / LLM-wiki)

This project (LLM-wiki) uses the **exact same Karpathy-pattern** that GBrain was built around. From GBrain's `GBRAIN_V0.md`:

> *"The compiled truth + timeline model (Karpathy-style knowledge pages) is right, but it needs a real database underneath. A 7,471-file / 2.3GB markdown wiki is choking git."*

**What GBrain adds on top of the pattern this project uses:**
1. Postgres/PGLite backend replacing raw git for search at scale
2. Vector embeddings + hybrid search (this project uses git + the parallax MCP for search)
3. Automated ingestion from external sources (meetings, email, X, voice)
4. Self-wiring knowledge graph (typed links extracted without LLM calls)
5. Skills system for agent workflows over the brain
6. Minions job queue for autonomous background processing
7. Dream cycle — overnight brain maintenance: contradiction detection, stale citation repair, consolidation

**Practical implication:** When this wiki grows beyond ~2,000-3,000 pages and git search becomes sluggish, GBrain's architecture (especially the PGLite zero-config mode) is the natural next step. `gbrain import <this-wiki-dir>` and all 34 skills become available immediately.

GBrain also explicitly supports the **multi-brain topology** that would allow this personal wiki to coexist with other knowledge stores (e.g., a team brain) — each with its own access control and search scope.

---

## Key Design Decisions (from the code)

1. **Postgres over SQLite** — 3+ years of proven RAG patterns. tsvector, pgvector HNSW, pg_trgm. SQLite is a future pluggable engine.
2. **Library-first distribution** — `bun add gbrain`. CLI and MCP are thin wrappers. Zero-overhead for OpenClaw integration.
3. **Trigger-based tsvector** — not generated column. Timeline entries are in a separate table; cross-table FTS requires a trigger.
4. **Auto-embed during import** — no separate step. `--no-embed` flag defers. `embedded_at` column enables `--stale` backfill.
5. **Semantic chunker on compiled_truth, recursive on timeline** — compiled truth needs topic-aware boundaries; timeline has predictable format.
6. **Token costs computed at read time**, not stored — `cost_usd` column was dropped (Codex outside-voice recommendation). Token counts are stable; USD pricing is volatile.
7. **No multi-tenant in v0** — single-user, local-only. MCP stdio is inherently local. Multi-user path: Supabase RLS + per-user API keys.
8. **Agent handler NOT in GBrain** — GBrain provides the queue infrastructure + clean handler contract. Actual agent execution lives in the platform plugin (OpenClaw, Hermes, etc.).

---

## Future / Roadmap

From TODOS.md and design docs:

**v1 candidates:**
- `gbrain ask` — natural language CLI alias for `gbrain query`
- **Intelligence compiler** — every fact as a first-class claim with source span, entity links, validity window, confidence, contradiction status
- **Web UI** — optional Vercel-hosted dashboard
- **SQLite engine** — community PRs welcome
- **Docker Compose** for self-hosted Postgres
- **Multi-user** — Supabase RLS + per-user API keys
- **Active skills via Trigger.dev** — application-specific briefings, meeting prep

**v0.34+ candidates (eval-gated):**
- Formal `relationships` table (composite-keyed, from `whoknows` substrate)
- Community detection (`page_communities` table + Louvain via graphology)
- `gbrain stale` and `gbrain prep <person-slug>` — OpenClaw skills layer
- Proactive nudges, intro suggestions, conversation continuity

**Phase 3 (agent orchestration):**
- `gbrain jobs dashboard` — live TUI showing all agents, token spend, tool calls
- Multi-tenant auth — runtime MCP access control, per-platform API keys
- Agent composition patterns — map-reduce, pipeline, approval gates as first-class primitives

---

## Related Topics

- [[karpathy-wiki-pattern]] — the compiled-truth + timeline pattern GBrain is built around
- [[mcp-protocol]] — how GBrain exposes tools to Claude Code, Cursor, ChatGPT
- [[pgvector]] — the vector database layer powering hybrid search
- [[openclaw]] — Garry's agent harness for non-coding tasks
- [[hermes-agent]] — second supported agent harness
- [[gstack]] — Garry's Claude Code tools setup (the coding brain)
- [[rag-hybrid-search]] — the retrieval architecture used
- [[claude-haiku]] — used for query expansion and LLM-guided chunking
- [[minions-job-queue]] — the Postgres-native background job system
