---
title: AI Internship
domain: career
tags: internship, rag, langchain, fastapi, research-profiling, work-experience
sources: [portfolio-home, recommendation-letter, internship-certificate, resumes]
last_updated: 2026-04-07
confidence: 0.95
links: [[genai-agents]], [[rag-architectures]], [[overview]]
---

# AI Internship

First professional AI engineering role. Designed and built a production intelligent research profiling system.

---

## Role

- **Title:** AI Engineer Intern
- **Certificate:** Verified (Internship Completion Certificate on file)
- **Recommendation:** Letter from supervising engineer (positive, on file)

---

## What Was Built

### Intelligent Research Profiling System

A multi-source aggregation system that compiles researcher profiles automatically by ingesting data across three primary domains:

- **PubMed:** Biomedical publications and medical semantic data.
- **ResearchGate:** Academic social network connections and pre-prints.
- **Google Scholar:** Citations, h-index metrics, and verified publication history.

**Workflow Architecture:**
1. **API Aggregation Layer:** Fast routing and data orchestration built on `FastAPI`.
2. **Semantic Search Agents:** `LangChain` powered RAG agents to chunk, embed, and index raw text pipelines.
3. **Structuring:** Unstructured academic papers are converted into pristine researcher profiles.
4. **Discovery:** LLMs analyze the vector space to generate real-time collaborator recommendations.

### RAG Search Agents

- Built contextual recommendation agents on top of aggregated data
- Used LangChain for chain orchestration and tool calling
- Semantic similarity for collaborator matching
- Contextual response generation for query answering

---

## Collaboration

- Worked with healthcare professionals on search algorithm refinement
- Iterative feedback loop with domain experts to validate relevance of results

---

## Core Tech Stack

- **Languages & Frameworks:** Python, FastAPI
- **AI/ML & Agents:** LangChain, RAG Architectures, Vector Databases
- **Integrated Data APIs:** PubMed API, Google Scholar API, ResearchGate API

---

## What This Demonstrated

- Production-level agentic system design (beyond toy examples)
- API design for ML systems
- Domain-specific RAG tuning (academic/healthcare)
- Professional collaboration with non-engineers

---

## Links

- [[genai-agents]] — skills applied
- [[rag-architectures]] — core technique used
- [[overview]] — career timeline
