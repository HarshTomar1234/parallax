# Parallax

A self-organizing digital nervous system and AI-maintained knowledge base. Built to document the frontiers of Machine Learning, Computer Vision, and Generative AI from first principles. Inspired by Andrej Karpathy's minimal LLM Wiki pattern.

## Overview

Parallax serves as a persistent, compounding knowledge system for Harsh Tomar (@kernel_crush). It is not a static portfolio, but rather a living architectural map maintained by specialized LLM agents.

## Structure

- `/wiki`: The core AI-maintained knowledge graph, organized by projects, research, skills, and concepts.
- `/raw`: Immutable source material (papers, unformatted code, meeting notes) ingested by the agents.
- `/harsh resume`: Versioned PDF resumes targeting specific ML and AI domains.
- `/landing`: A static web interface for navigating the knowledge base locally.

## Agent System

The repository utilizes autonomous agents dictated by the schema in `AGENTS.md`. These agents perform Ingestion (reading new sources to generate markdown), Querying (synthesizing answers from past projects), and Linting (maintaining the structural integrity of the interlinked graph).

## Getting Started

Start at the Master Index: [wiki/index.md](wiki/index.md)
