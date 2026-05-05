---
title: QuantaAI
domain: projects
tags: genai, agents, langgraph, gpt4, nextjs, fastapi, streaming, rag, web-search
sources: [github-quanta-ai, portfolio-projects]
last_updated: 2026-04-07
confidence: 0.95
links: "[[genai-agents]], [[rag-architectures]]"
---

# QuantaAI

Intelligent conversational AI with real-time web search and agentic decision-making.

- **Repo:** https://github.com/HarshTomar1234/QuantaAI

---

## Architecture

4-node LangGraph state machine:

**4-node LangGraph state machine:**

1. **Query Input:** The raw user prompt is ingested into the state graph.
2. **Classifier Node (GPT-4):** Operates with 94% accuracy to determine if external validation or web search is needed. Triggers conditional edge routing.
3. **Search Node (Tavily API):** Conducts high-speed broad retrieval, assigns relevance scoring to documents, and extracts source attribution links.
4. **Generate Node (GPT-4):** Synthesizes the augmented context into a cohesive answer natively supporting streaming.
5. **Response Node:** Manages continuous token streaming and publishes intermediate state updates to the user interface.

## Key Metrics

- **Search-decision accuracy:** 94%
- **Context window:** Last 10 messages with intelligent semantic compression
- **Search provider:** Tavily API
- **Streaming architecture:** Real-time token streaming with phase transparency

## Features

- **Autonomous search detection** — AI decides when to search without explicit commands
- **Multi-stage transparency** — user sees classification → search → generation phases live
- **Source attribution** — all search-based responses include clickable sources with relevance scores
- **Context-aware** — conversation history with intelligent compression
- **Modern UI** — Next.js 14, TypeScript, Tailwind CSS

## Core Tech Stack

- **Agentic Framework:** LangGraph, GPT-4
- **Search & Orchestration:** Tavily API, FastAPI
- **Frontend / Client:** Next.js 14, TypeScript, Tailwind CSS

## Design Patterns

- LangGraph StateGraph with conditional edge routing
- Streaming pipeline using Server-Sent Events (SSE)
- Memory management with sliding window + semantic compression
- Relevance scoring for search result ranking

## Links

- [[genai-agents]] — agent framework domain
- [[rag-architectures]] — retrieval patterns used
