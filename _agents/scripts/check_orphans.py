#!/usr/bin/env python3
"""
Parallax Orphan & Broken-Link Detector
- Orphans: pages with no inbound [[links]] from other pages
- Broken links: [[links]] that reference non-existent pages
Run by GitHub Actions weekly.
"""

import os
import re
import sys

WIKI_DIR = 'wiki'

# Build a map of all pages and all outbound links
all_pages = set()
outbound_links = {}  # slug -> set of linked slugs

SKIP_DIRS = {'.obsidian', '_templates', '_attachments'}

for root, dirs, files in os.walk(WIKI_DIR):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        if not fname.endswith('.md'):
            continue
        slug = fname.replace('.md', '')
        all_pages.add(slug)
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Body [[wikilinks]]
        links = set(re.findall(r'\[\[([^\]]+)\]\]', content))
        # Frontmatter links: [slug1, slug2] array (plain slugs, no brackets)
        fm_match = re.match(r'^---[\s\S]*?^---', content, re.MULTILINE)
        if fm_match:
            fm = fm_match.group(0)
            links_field = re.search(r'^links:\s*\[([^\]]+)\]', fm, re.MULTILINE)
            if links_field:
                for s in links_field.group(1).split(','):
                    links.add(s.strip())
        outbound_links[slug] = links

# Find inbound link counts (only for existing pages)
inbound_count = {slug: 0 for slug in all_pages}
broken_links = []  # (source_slug, broken_target)

# Pages that are prose/logs and may contain example [[link]] syntax
BROKEN_LINK_SKIP = {'log'}

for page, links in outbound_links.items():
    for linked in links:
        if linked in inbound_count:
            inbound_count[linked] += 1
        elif page not in BROKEN_LINK_SKIP:
            broken_links.append((page, linked))

# Orphans = pages with zero inbound links (excluding index and log)
EXEMPT = {'index', 'log', 'overview'}
orphans = [slug for slug, count in inbound_count.items()
           if count == 0 and slug not in EXEMPT]

print(f"\n=== Parallax Orphan & Broken-Link Detector ===")
print(f"Total pages   : {len(all_pages)}")
print(f"Orphans       : {len(orphans)}")
print(f"Broken links  : {len(broken_links)}")

if orphans:
    print("\n--- Orphan Pages (no inbound links) ---")
    for o in sorted(orphans):
        print(f"  [[{o}]]")
    print("\nConsider linking these pages from relevant pages.")
else:
    print("\nNo orphan pages. Knowledge graph is fully connected.")

if broken_links:
    print("\n--- Broken Links (target page does not exist) ---")
    for source, target in sorted(broken_links):
        print(f"  [[{target}]]  <- referenced in {source}.md")
    print("\nCreate the missing pages or remove the references.")

# Don't fail CI for orphans/broken-links — just warn
sys.exit(0)
