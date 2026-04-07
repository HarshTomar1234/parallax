---
title: QuantaAI
domain: projects
tags: genai, agents, langgraph, gpt4, nextjs, fastapi, streaming, rag, web-search
sources: [github-quanta-ai, portfolio-projects]
last_updated: 2026-04-07
links: [[genai-agents]], [[rag-architectures]]
---

# QuantaAI

Intelligent conversational AI with real-time web search and agentic decision-making.

- **Repo:** https://github.com/HarshTomar1234/QuantaAI

---

## Architecture

4-node LangGraph state machine:

```
Query Input
    ↓
[Classifier Node] — GPT-4, 94% accuracy determining if search needed
    ↓ (conditional routing)
[Search Node]     — Tavily API, relevance scoring, source attribution
    ↓
[Generate Node]   — GPT-4 response with streaming
    ↓
[Response Node]   — token streaming + intermediate state updates
```

## Key Metrics

```
Search-decision accuracy: 94%
Context window: last 10 messages with semantic compression
Search provider: Tavily API
Streaming: real-time token streaming with phase transparency
```

## Features

- **Autonomous search detection** — AI decides when to search without explicit commands
- **Multi-stage transparency** — user sees classification → search → generation phases live
- **Source attribution** — all search-based responses include clickable sources with relevance scores
- **Context-aware** — conversation history with intelligent compression
- **Modern UI** — Next.js 14, TypeScript, Tailwind CSS

## Tech Stack

```
LangGraph | GPT-4 | Tavily API | Next.js 14 | TypeScript | FastAPI | Tailwind CSS
```

## Design Patterns

- LangGraph StateGraph with conditional edge routing
- Streaming pipeline using Server-Sent Events (SSE)
- Memory management with sliding window + semantic compression
- Relevance scoring for search result ranking

## Links

- [[genai-agents]] — agent framework domain
- [[rag-architectures]] — retrieval patterns used
