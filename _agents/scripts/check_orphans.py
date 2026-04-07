#!/usr/bin/env python3
"""
Parallax Orphan Page Detector
Finds wiki pages that have no inbound [[links]] from other pages.
Run by GitHub Actions weekly.
"""

import os
import re
import sys

WIKI_DIR = 'wiki'

# Build a map of all pages and all outbound links
all_pages = set()
outbound_links = {}  # page -> set of linked page slugs

for root, dirs, files in os.walk(WIKI_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        slug = fname.replace('.md', '')
        all_pages.add(slug)
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        links = set(re.findall(r'\[\[([^\]]+)\]\]', content))
        outbound_links[slug] = links

# Find inbound link counts
inbound_count = {slug: 0 for slug in all_pages}
for page, links in outbound_links.items():
    for linked in links:
        if linked in inbound_count:
            inbound_count[linked] += 1

# Orphans = pages with zero inbound links (excluding index and log)
EXEMPT = {'index', 'log', 'overview'}
orphans = [slug for slug, count in inbound_count.items()
           if count == 0 and slug not in EXEMPT]

print(f"\n=== Parallax Orphan Detector ===")
print(f"Total pages : {len(all_pages)}")
print(f"Orphans     : {len(orphans)}")

if orphans:
    print("\n--- Orphan Pages (no inbound links) ---")
    for o in sorted(orphans):
        print(f"  [[{o}]]")
    print("\nConsider linking these pages from relevant pages.")
else:
    print("\nNo orphan pages. Knowledge graph is fully connected.")

# Don't fail CI for orphans — just warn
sys.exit(0)
