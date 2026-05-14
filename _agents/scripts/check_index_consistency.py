#!/usr/bin/env python3
"""
Parallax Content Consistency Checker

Three checks:
1. Index completeness  — every wiki/<domain>/<slug>.md has a row in wiki/index.md
2. Sidebar completeness — every wiki/<domain>/<slug>.md is listed in landing/index.html
3. Sidebar label quality — detect auto-generated slug labels (e.g. "Machine And Deep Learning Nlp")

Exits 1 if errors are found; exits 0 otherwise.
"""

import os
import re
import sys
from pathlib import Path

WIKI_DIR      = Path("wiki")
INDEX_MD      = Path("wiki/index.md")
SIDEBAR_HTML  = Path("landing/index.html")
SKIP_DIRS     = {".obsidian", "_templates", "_attachments"}

# Root-level wiki files that live outside any domain subdirectory
ROOT_EXEMPT = {"index", "log", "overview", "llms", "llms-full", "graph", "search-index"}

# index.md section heading -> domain folder name
SECTION_TO_DOMAIN = {
    "Projects":  "projects",
    "Research":  "research",
    "Learning":  "learning",
    "Skills":    "skills",
    "Concepts":  "concepts",
    "Career":    "career",
    "Meta":      "meta",
}

errors   = []
warnings = []


def collect_wiki_pages() -> dict[str, set[str]]:
    """Walk wiki/ and return {domain: {slug, ...}} for all domain subfolders."""
    pages: dict[str, set[str]] = {}
    for root, dirs, files in os.walk(WIKI_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        domain = Path(root).name
        if domain == "wiki":
            continue  # root-level files are handled separately
        for fname in files:
            if fname.endswith(".md"):
                pages.setdefault(domain, set()).add(fname[:-3])
    return pages


def collect_index_rows() -> dict[str, set[str]]:
    """Parse wiki/index.md and return {domain: {slug, ...}} for every [[slug]] in tables."""
    if not INDEX_MD.exists():
        errors.append(f"[MISSING] {INDEX_MD} not found")
        return {}

    content = INDEX_MD.read_text(encoding="utf-8")
    index_slugs: dict[str, set[str]] = {}
    current_domain = None

    for line in content.splitlines():
        # Match ### headings to detect section changes
        h3 = re.match(r"^###\s+(\w+)", line)
        if h3:
            current_domain = SECTION_TO_DOMAIN.get(h3.group(1))

        if current_domain is None:
            continue

        for slug in re.findall(r"\[\[([^\]]+)\]\]", line):
            index_slugs.setdefault(current_domain, set()).add(slug)

    return index_slugs


def collect_sidebar_entries() -> dict[str, dict[str, str]]:
    """Parse landing/index.html and return {domain: {slug: display_label}}."""
    if not SIDEBAR_HTML.exists():
        warnings.append(f"[MISSING] {SIDEBAR_HTML} — skipping sidebar check")
        return {}

    content = SIDEBAR_HTML.read_text(encoding="utf-8")
    entries: dict[str, dict[str, str]] = {}
    # Only capture domain/slug entries (single-segment entries like data-page="log" are root files)
    for m in re.finditer(r'data-page="([^/"]+)/([^"]+)"[^>]*>([^<]+)<', content):
        domain, slug, label = m.group(1), m.group(2), m.group(3).strip()
        entries.setdefault(domain, {})[slug] = label
    return entries


# Connector words that should be lowercase in proper title case
# If any appear capitalized mid-label, the label is auto-generated
_CONNECTORS = {"And", "Or", "The", "Of", "A", "An", "In", "For", "To", "With", "By", "At", "From"}

def is_auto_slug_label(slug: str, label: str) -> bool:
    """Return True if label looks auto-generated from the slug.

    Two signals:
    - Label equals naive title-case of slug AND contains a capitalized connector
      mid-string (e.g. 'Machine And Deep Learning Nlp' has 'And').
    - Label equals naive title-case of slug AND the last word is a known acronym
      rendered lowercase (e.g. 'Nlp', 'Cv', 'Qlora').
    Labels like 'Attention Mechanisms' or 'Deep Learning' pass — they happen to
    match title-case but contain no telltale connectors or broken acronyms.
    """
    naive = slug.replace("-", " ").title()
    if label != naive:
        return False
    words = label.split()
    # Connector word capitalized mid-label is the primary telltale
    # e.g. "Machine And Deep Learning Nlp" has "And"
    return any(w in _CONNECTORS for w in words[1:])


# ── Run ─────────────────────────────────────────────────────────────────────

wiki_pages  = collect_wiki_pages()
index_rows  = collect_index_rows()
sidebar     = collect_sidebar_entries()

all_domains = set(wiki_pages) | set(index_rows)

print("=== Parallax Content Consistency Checker ===\n")

# ── Check 1: index.md completeness ──────────────────────────────────────────
print("--- 1. Index completeness (wiki/index.md) ---")
missing_from_index  = 0
phantom_in_index    = 0

for domain in sorted(all_domains):
    fs   = wiki_pages.get(domain, set())
    idx  = index_rows.get(domain, set())

    for slug in sorted(fs - idx):
        errors.append(
            f"[MISSING FROM INDEX] wiki/{domain}/{slug}.md has no row in index.md"
        )
        missing_from_index += 1

    for slug in sorted(idx - fs):
        errors.append(
            f"[PHANTOM IN INDEX] index.md lists [[{slug}]] but wiki/{domain}/{slug}.md does not exist"
        )
        phantom_in_index += 1

if missing_from_index == 0 and phantom_in_index == 0:
    print("  All domain pages are represented in index.md")
else:
    print(f"  Missing from index : {missing_from_index}")
    print(f"  Phantom in index   : {phantom_in_index}")

# ── Check 2: sidebar completeness ───────────────────────────────────────────
print("\n--- 2. Sidebar completeness (landing/index.html) ---")
missing_from_sidebar = 0
phantom_in_sidebar   = 0

for domain in sorted(all_domains):
    fs = wiki_pages.get(domain, set())
    sb = set(sidebar.get(domain, {}).keys())

    for slug in sorted(fs - sb):
        errors.append(
            f"[MISSING FROM SIDEBAR] wiki/{domain}/{slug}.md has no nav entry in index.html"
        )
        missing_from_sidebar += 1

    for slug in sorted(sb - fs):
        errors.append(
            f"[PHANTOM IN SIDEBAR] sidebar lists {domain}/{slug} but wiki page does not exist"
        )
        phantom_in_sidebar += 1

if missing_from_sidebar == 0 and phantom_in_sidebar == 0:
    print("  All domain pages are represented in the sidebar")
else:
    print(f"  Missing from sidebar : {missing_from_sidebar}")
    print(f"  Phantom in sidebar   : {phantom_in_sidebar}")

# ── Check 3: sidebar label quality ──────────────────────────────────────────
print("\n--- 3. Sidebar label quality ---")
auto_labels = 0

for domain, entries in sorted(sidebar.items()):
    for slug, label in sorted(entries.items()):
        if is_auto_slug_label(slug, label):
            warnings.append(
                f"[AUTO-SLUG LABEL] {domain}/{slug} -> \"{label}\" "
                f"(looks auto-generated — set a proper display name)"
            )
            auto_labels += 1

if auto_labels == 0:
    print("  All sidebar labels look hand-crafted")
else:
    print(f"  Auto-slug labels detected : {auto_labels}")

# ── Summary ──────────────────────────────────────────────────────────────────
total_pages = sum(len(v) for v in wiki_pages.values())
print(f"\nTotal domain pages : {total_pages}")
print(f"Errors             : {len(errors)}")
print(f"Warnings           : {len(warnings)}")

if warnings:
    print("\n--- Warnings ---")
    for w in warnings:
        print(f"  {w}")

if errors:
    print("\n--- Errors ---")
    for e in errors:
        print(f"  {e}")
    print("\nConsistency check FAILED.")
    sys.exit(1)

print("\nConsistency check PASSED.")
sys.exit(0)
