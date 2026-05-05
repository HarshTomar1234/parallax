---
title: AgentForge
domain: learning
tags: agents, crewai, langgraph, llamaindex, autogen, smolagents, pydanticai, multi-agent, frameworks
sources: [https://github.com/HarshTomar1234/AgentForge]
last_updated: 2026-05-05
confidence: 0.90
links: "[[genai-agents]], [[reasoning-llms]], [[rag-architectures]], [[vlmverse]]"
---

# AgentForge

Hands-on collection of AI agent implementations across every major framework. Built as a personal learning hub — one framework per directory, working examples throughout.

- **Repo:** https://github.com/HarshTomar1234/AgentForge
- **Stars:** 2 | **Forks:** 1

---

## Frameworks Covered

### CrewAI
Role-based multi-agent orchestration. Agents are assigned personas (researcher, writer, analyst) and collaborate via a sequential or hierarchical crew pipeline. Best for structured, goal-oriented workflows where each agent has a defined responsibility.

### LangGraph
Graph-based agent workflows from the LangChain ecosystem. Nodes are processing steps, edges are transitions — supports cycles (retry loops, reflection) that vanilla chains cannot express. Used for stateful, conditional agent flows.

### LlamaIndex
Data-first agent framework. Specialises in connecting LLMs to structured and unstructured data sources via query engines and tool abstractions. Strong for RAG-heavy agents that need to reason over large document sets.

### PydanticAI
Type-safe agent framework from the Pydantic team. Agents are defined with strict input/output schemas — runtime validation ensures tool calls and responses match expected types. Reduces silent failures in production pipelines.

### AutoGen (AG2)
Microsoft's conversation-driven multi-agent framework. Agents communicate via structured message passing; supports human-in-the-loop at any stage. Well-suited for collaborative code generation and iterative problem solving.

### smolagents
HuggingFace's lightweight agent library. Minimal abstraction — agents write and execute Python code directly as tool calls. Designed for fast prototyping and open-model compatibility.

### Swarm (OpenAI)
OpenAI's experimental multi-agent pattern. Agents hand off control to each other via transfer functions — no central orchestrator. Demonstrates clean A2A (agent-to-agent) handoff patterns.

---

## Key Patterns Learned

| Pattern | Frameworks |
|---|---|
| Role-based crews | CrewAI |
| Graph / stateful flows | LangGraph |
| RAG + tool agents | LlamaIndex |
| Type-safe pipelines | PydanticAI |
| Conversational multi-agent | AutoGen |
| Code-as-tool | smolagents |
| Agent handoff (A2A) | Swarm |

The central insight across all frameworks: **agents are LLMs + tools + a loop**. Every framework is a different opinion on how to structure that loop and coordinate multiple agents within it.

---

## Relation to Other Work

- [[genai-agents]] — the skill domain this repo builds toward
- Travel-Planner uses Google ADK for A2A — same multi-agent pattern as Swarm
- Kubrick AI (open-source contribution) uses FastMCP, a production-grade alternative to these framework-level patterns
- [[reasoning-llms]] — the reasoning capability that makes complex agent chains reliable
- [[rag-architectures]] — used inside LlamaIndex and LangGraph agents for retrieval
- [[vlmverse]] — multimodal extension of agent capabilities
