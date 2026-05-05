#!/usr/bin/env python3
"""
Parallax Wiki MCP Server
Exposes the wiki knowledge graph as callable tools for any MCP client (Claude Desktop, etc.).

Tools:
  search_wiki(query)            — keyword search across all pages
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
# Page loader
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
    slug = stem filename (e.g. 'attention-mechanisms').
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


# Load once at startup
_PAGES: dict[str, dict] = _load_pages()

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
    results = []
    for slug, page in sorted(_PAGES.items()):
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
    page = _PAGES.get(slug)
    if page is None:
        matches = [s for s in _PAGES if slug.lower() in s.lower()]
        if len(matches) == 1:
            page = _PAGES[matches[0]]
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

    start = _PAGES.get(slug)
    if start is None:
        return f"Page '{slug}' not found. Use list_pages() to see available slugs."

    visited: dict[str, int] = {slug: 0}
    frontier = [slug]

    for depth in range(1, hops + 1):
        next_frontier = []
        for current in frontier:
            page = _PAGES.get(current)
            if not page:
                continue
            for neighbour in page["meta"].get("links", []):
                if neighbour not in visited and neighbour in _PAGES:
                    visited[neighbour] = depth
                    next_frontier.append(neighbour)
        frontier = next_frontier

    results = []
    for s, dist in sorted(visited.items(), key=lambda x: (x[1], x[0])):
        if s == slug:
            continue
        m = _PAGES[s]["meta"]
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
    Full-text keyword search across all wiki pages.
    Returns up to 10 results ranked by hit count, with a short excerpt around the first match.
    query can be a phrase or space-separated keywords.
    """
    terms = [t.lower() for t in query.split() if t]
    if not terms:
        return "Empty query."

    scored = []
    for slug, page in _PAGES.items():
        text = page["raw"].lower()
        hits = sum(text.count(t) for t in terms)
        if hits == 0:
            continue

        first_pos = len(text)
        for t in terms:
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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
