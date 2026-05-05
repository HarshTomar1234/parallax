#!/usr/bin/env python3
"""
Parallax Wiki MCP Server
Exposes the wiki knowledge graph as callable tools for any MCP client (Claude Desktop, etc.).

Tools:
  search_wiki(query)            — semantic keyword search with synonym expansion
  get_page(slug)                — return full markdown content of a page
  get_related(slug, hops)       — return slugs reachable within N hops via links graph
  list_pages(domain?)           — list all pages, optionally filtered by domain

Usage:
  pip install -r requirements.txt
  python server.py
"""

import os
import re
import json
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

WIKI_DIR = Path(__file__).parent.parent / "wiki"
SKIP_DIRS = {".obsidian", "_templates", "_attachments"}

# ---------------------------------------------------------------------------
# Synonym map — expands query terms for semantic coverage
# Each key maps to additional terms that are searched alongside it.
# ---------------------------------------------------------------------------

SYNONYMS: dict[str, list[str]] = {
    "neural network": ["deep learning", "pytorch", "tensorflow"],
    "neural networks": ["deep learning", "pytorch", "tensorflow"],
    "llm": ["large language model", "gpt", "claude", "transformer"],
    "llms": ["large language model", "gpt", "claude", "transformer"],
    "large language model": ["llm", "transformer", "gpt"],
    "fine-tune": ["lora", "qlora", "peft", "finetuning", "fine-tuning"],
    "fine-tuning": ["lora", "qlora", "peft", "finetuning"],
    "finetuning": ["lora", "qlora", "peft", "fine-tuning"],
    "agent": ["multi-agent", "langgraph", "crewai", "ag2", "agentic"],
    "agents": ["multi-agent", "langgraph", "crewai", "ag2", "agentic"],
    "multimodal": ["vlm", "vision language", "palgemma", "clip", "image text"],
    "vlm": ["multimodal", "vision language model", "palgemma", "vlmverse"],
    "object detection": ["yolo", "yolov8", "detr", "detection"],
    "tracking": ["bytetrack", "deepsort", "mot", "multi-object tracking"],
    "diffusion": ["stable diffusion", "ddpm", "denoising", "inpainting"],
    "rag": ["retrieval augmented", "retrieval", "vector store", "embedding"],
    "retrieval": ["rag", "vector store", "embedding", "faiss"],
    "mlops": ["dvc", "mlflow", "docker", "kubernetes", "ci/cd", "monitoring"],
    "deployment": ["docker", "fastapi", "aws", "kubernetes", "flask"],
    "segmentation": ["mask", "instance segmentation", "semantic segmentation"],
    "classification": ["accuracy", "f1", "precision", "recall"],
    "heart rate": ["rppg", "bpm", "physnet", "photoplethysmography"],
    "drug discovery": ["molecuquest", "molecule", "molecular"],
    "deepfake": ["deepguard", "xception", "genimage"],
    "attention": ["transformer", "self-attention", "cross-attention", "softmax"],
    "transformer": ["attention", "bert", "gpt", "vit", "encoder", "decoder"],
}


def _expand_terms(terms: list[str]) -> list[str]:
    """Add synonym expansions to the query term list, preserving order."""
    expanded = list(terms)
    joined = " ".join(terms)
    for phrase, extras in SYNONYMS.items():
        if phrase in joined:
            for e in extras:
                if e not in expanded:
                    expanded.append(e)
    for term in terms:
        if term in SYNONYMS:
            for e in SYNONYMS[term]:
                if e not in expanded:
                    expanded.append(e)
    return expanded


# ---------------------------------------------------------------------------
# Page loader — called on every tool invocation (lazy reload)
# ---------------------------------------------------------------------------

def _parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter fields we care about (no external parser needed)."""
    fm_match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", content)
    if not fm_match:
        return {}
    fm = fm_match.group(1)

    result = {}

    for key in ("title", "domain", "confidence", "last_updated"):
        m = re.search(rf"^{key}:\s*(.+)", fm, re.MULTILINE)
        if m:
            result[key] = m.group(1).strip()

    for key in ("tags", "links"):
        m = re.search(rf"^{key}:\s*\[([^\]]*)\]", fm, re.MULTILINE)
        if m:
            result[key] = [s.strip() for s in m.group(1).split(",") if s.strip()]
        else:
            result[key] = []

    return result


def _body(content: str) -> str:
    """Strip frontmatter, return body text."""
    return re.sub(r"^---[\s\S]*?---\r?\n", "", content, count=1).strip()


def _load_pages() -> dict[str, dict]:
    """
    Walk wiki/ and return {slug: {meta, body, raw}}.
    Called on every tool invocation so new pages are picked up without restart.
    """
    pages: dict[str, dict] = {}
    for root, dirs, files in os.walk(WIKI_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            path = Path(root) / fname
            slug = path.stem
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue
            meta = _parse_frontmatter(content)
            meta["slug"] = slug
            meta["path"] = str(path.relative_to(WIKI_DIR))
            pages[slug] = {
                "meta": meta,
                "body": _body(content),
                "raw": content,
            }
    return pages


# ---------------------------------------------------------------------------
# MCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("parallax-wiki")


@mcp.tool()
def list_pages(domain: Optional[str] = None):
    """
    List all wiki pages. Optionally filter by domain
    (projects, research, skills, concepts, career, learning, meta).
    Returns a JSON array of {slug, title, domain, confidence}.
    """
    pages = _load_pages()
    results = []
    for slug, page in sorted(pages.items()):
        m = page["meta"]
        if domain and m.get("domain", "").lower() != domain.lower():
            continue
        results.append({
            "slug": slug,
            "title": m.get("title", slug),
            "domain": m.get("domain", ""),
            "confidence": m.get("confidence", ""),
        })
    return json.dumps(results, indent=2)


@mcp.tool()
def get_page(slug: str):
    """
    Return the full markdown content of a wiki page by its slug
    (e.g. 'attention-mechanisms', 'travel-planner', 'synthesis').
    Includes frontmatter so the caller can see confidence, links, tags, etc.
    """
    pages = _load_pages()
    page = pages.get(slug)
    if page is None:
        matches = [s for s in pages if slug.lower() in s.lower()]
        if len(matches) == 1:
            page = pages[matches[0]]
        elif len(matches) > 1:
            return f"Ambiguous slug '{slug}'. Matches: {matches}. Use an exact slug from list_pages."
        else:
            return f"Page '{slug}' not found. Use list_pages() to see available slugs."
    return page["raw"]


@mcp.tool()
def get_related(slug: str, hops: int = 1):
    """
    Return slugs reachable from a given page within N hops via the links graph.
    hops=1 returns direct neighbours; hops=2 returns neighbours-of-neighbours, etc.
    Max hops is capped at 3 to prevent runaway traversal.
    Returns a JSON array of {slug, title, domain, distance}.
    """
    hops = min(max(hops, 1), 3)
    pages = _load_pages()

    if slug not in pages:
        return f"Page '{slug}' not found. Use list_pages() to see available slugs."

    visited: dict[str, int] = {slug: 0}
    frontier = [slug]

    for depth in range(1, hops + 1):
        next_frontier = []
        for current in frontier:
            page = pages.get(current)
            if not page:
                continue
            for neighbour in page["meta"].get("links", []):
                if neighbour not in visited and neighbour in pages:
                    visited[neighbour] = depth
                    next_frontier.append(neighbour)
        frontier = next_frontier

    results = []
    for s, dist in sorted(visited.items(), key=lambda x: (x[1], x[0])):
        if s == slug:
            continue
        m = pages[s]["meta"]
        results.append({
            "slug": s,
            "title": m.get("title", s),
            "domain": m.get("domain", ""),
            "distance": dist,
        })
    return json.dumps(results, indent=2)


@mcp.tool()
def search_wiki(query: str):
    """
    Full-text keyword search across all wiki pages with synonym expansion.
    Synonyms: 'neural network' also matches 'deep learning', 'LLM' also matches
    'transformer', 'agent' also matches 'langgraph'/'crewai', etc.
    Returns up to 10 results ranked by hit count, with a short excerpt.
    """
    base_terms = [t.lower() for t in query.split() if t]
    if not base_terms:
        return "Empty query."

    terms = _expand_terms(base_terms)
    pages = _load_pages()

    scored = []
    for slug, page in pages.items():
        text = page["raw"].lower()

        # Original terms weighted 3x, synonym expansions weighted 1x
        hits = sum(text.count(t) * 3 for t in base_terms)
        hits += sum(text.count(t) for t in terms if t not in base_terms)

        if hits == 0:
            continue

        first_pos = len(text)
        for t in base_terms:
            pos = text.find(t)
            if pos != -1 and pos < first_pos:
                first_pos = pos

        start = max(0, first_pos - 80)
        end = min(len(page["raw"]), first_pos + 160)
        excerpt = page["raw"][start:end].replace("\n", " ").strip()

        scored.append({
            "slug": slug,
            "title": page["meta"].get("title", slug),
            "domain": page["meta"].get("domain", ""),
            "hits": hits,
            "excerpt": f"...{excerpt}...",
        })

    scored.sort(key=lambda x: -x["hits"])
    top = scored[:10]

    if not top:
        return f"No pages matched '{query}'."
    return json.dumps(top, indent=2)


@mcp.tool()
def get_summary(slug: str):
    """
    Return a compact summary of a wiki page: title, domain, confidence, tags,
    and the first meaningful paragraph of body text (stripped of markdown).
    Faster than get_page() when you only need a quick overview.
    """
    pages = _load_pages()
    page = pages.get(slug)
    if page is None:
        matches = [s for s in pages if slug.lower() in s.lower()]
        if len(matches) == 1:
            page = pages[matches[0]]
        elif len(matches) > 1:
            return f"Ambiguous slug '{slug}'. Matches: {matches}."
        else:
            return f"Page '{slug}' not found. Use list_pages() to see available slugs."

    meta = page["meta"]

    # Extract first non-empty, non-heading paragraph from body
    body = page["body"]
    # Strip markdown: headers, bold, italic, wikilinks, URLs, list markers
    clean = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.MULTILINE)
    clean = re.sub(r"\[\[.*?\]\]", "", clean)
    clean = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", clean)
    clean = re.sub(r"[*_`#>|-]", "", clean)
    clean = re.sub(r"https?://\S+", "", clean)

    paragraphs = [p.strip() for p in re.split(r"\n{2,}", clean) if len(p.strip()) > 40]
    first_para = paragraphs[0][:300] if paragraphs else "(no summary available)"

    result = {
        "slug": slug,
        "title": meta.get("title", slug),
        "domain": meta.get("domain", ""),
        "confidence": meta.get("confidence", ""),
        "tags": meta.get("tags", []),
        "last_updated": meta.get("last_updated", ""),
        "links": meta.get("links", []),
        "summary": first_para,
    }
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
