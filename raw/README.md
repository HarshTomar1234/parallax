# raw/ — Immutable Source Material

This folder contains the raw sources that feed the Parallax wiki.

## Purpose

- **Immutable** — never edited by AI agents
- **Curated** — add sources intentionally
- **Referrable** — wiki pages cite `sources:` pointing here

## Structure

```
raw/
├── projects/     # Project descriptions, READMEs, demos
├── research/     # Paper PDFs, implementation notes
├── career/       # Resume copies, certificate, recommendation letter
├── learning/     # Course notes, blog links, reading lists
└── assets/       # Screenshots, diagrams
```

## Seeded Sources

| File | Content |
|------|---------|
| career/resumes/ | 6 domain-specific resumes (from D:\documents\harsh resume\) |
| career/recommendation-letter.ref | HarshTomarRecommendationLetter.pdf |
| career/internship-certificate.ref | Internship Completion Certificate |

## How to Add a Source

1. Drop the file in the appropriate subfolder
2. Run Parallax ingest prompt (see AGENTS.md)
3. Agent reads → writes wiki page → updates index → appends log
