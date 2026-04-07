---
title: RAG Architectures
domain: concepts
tags: rag, retrieval, vector-db, embeddings, chunking, langchain, pinecone, chroma, faiss
sources: [github-ragify, github-pdf-chat, portfolio-more, ai-internship]
last_updated: 2026-04-07
links: [[genai-agents]], [[ai-internship]], [[quanta-ai]]
---

# RAG Architectures

Retrieval-Augmented Generation — grounding LLM responses in external knowledge.

---

## Core Pattern

```
Query
  ↓
[Embed query] → vector
  ↓
[Vector DB search] → top-k relevant chunks
  ↓
[Augmented prompt] = query + retrieved chunks
  ↓
[LLM generation] → grounded response
```

## Key Components

### Embedding
- **OpenAI text-embedding-3-small/large** — high quality, API-based
- **HuggingFace sentence-transformers** — open-source, local
- **Domain-specific:** SPECTER for academic papers ([[ai-internship]])

### Vector Stores
| Store | When |
|-------|------|
| **Pinecone** | Managed, production, scale |
| **Chroma** | Local dev, fast setup |
| **FAISS** | In-memory, high performance, no server |

### Chunking Strategies
- Recursive character splitting — respects document structure
- Semantic chunking — splits on meaning boundaries
- Sliding window — overlap for context preservation
- Document-aware — tables, headers as atomic units

### Retrieval Patterns
- **Similarity search** — cosine or dot product ANN
- **MMR (Maximum Marginal Relevance)** — diversity-aware retrieval
- **Hybrid (BM25 + vector)** — keyword + semantic
- **Cross-encoder reranking** — second-pass relevance scoring

---

## Applied Systems

- **[[ai-internship]]** — multi-source RAG over PubMed, ResearchGate, Google Scholar
- **[[quanta-ai]]** — Tavily search + GPT-4 generation (web-RAG variant)
- **RAGify** (https://github.com/HarshTomar1234/RAGify) — RAG hub with multiple patterns
- **Multiple PDF ChatApp** — document-level RAG, source attribution

---

## Advanced Patterns

### HyDE (Hypothetical Document Embeddings)
Generate a hypothetical answer, embed it, retrieve on that — better retrieval for questions.

### FLARE (Forward-Looking Active REtrieval)
Retrieves on-demand during generation when confidence drops.

### Self-RAG
LLM decides when to retrieve, what to retrieve, and whether retrieved content is useful.

---

## Links

- [[genai-agents]] — RAG is core to agent tool use
- [[ai-internship]] — production RAG system
- [[quanta-ai]] — web search as external knowledge source
