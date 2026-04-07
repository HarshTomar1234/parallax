#!/usr/bin/env python3
"""
Parallax Wiki Validator
Checks that every wiki page has valid frontmatter and required fields.
Run by GitHub Actions on every push to wiki/.
"""

import os
import sys
import re

REQUIRED_FIELDS = ['title', 'domain', 'tags', 'last_updated', 'links']
VALID_DOMAINS = ['projects', 'research', 'skills', 'concepts', 'career', 'meta']
WIKI_DIR = 'wiki'

errors = []
warnings = []
pages_checked = 0

def check_frontmatter(filepath, content):
    """Validate YAML frontmatter of a wiki page."""
    fm_match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---', content)
    if not fm_match:
        errors.append(f"[MISSING FRONTMATTER] {filepath}")
        return

    fm = fm_match.group(1)

    for field in REQUIRED_FIELDS:
        if f'{field}:' not in fm:
            errors.append(f"[MISSING FIELD '{field}'] {filepath}")

    domain_match = re.search(r'domain:\s*(\S+)', fm)
    if domain_match:
        domain = domain_match.group(1).strip()
        if domain not in VALID_DOMAINS:
            warnings.append(f"[UNKNOWN DOMAIN '{domain}'] {filepath}")

def check_page_content(filepath, content):
    """Check for minimum content quality."""
    # Strip frontmatter
    body = re.sub(r'^---[\s\S]*?---\n', '', content).strip()

    if len(body) < 100:
        warnings.append(f"[THIN CONTENT < 100 chars] {filepath}")

    if '[[' not in body:
        warnings.append(f"[NO WIKI LINKS] {filepath}")

# Walk the wiki directory
for root, dirs, files in os.walk(WIKI_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        check_frontmatter(fpath, content)
        check_page_content(fpath, content)
        pages_checked += 1

# Report
print(f"\n=== Parallax Wiki Validator ===")
print(f"Pages checked : {pages_checked}")
print(f"Errors        : {len(errors)}")
print(f"Warnings      : {len(warnings)}")

if warnings:
    print("\n--- Warnings ---")
    for w in warnings:
        print(f"  {w}")

if errors:
    print("\n--- Errors ---")
    for e in errors:
        print(f"  {e}")
    print("\nValidation FAILED.")
    sys.exit(1)
else:
    print("\nValidation PASSED. Wiki structure is healthy.")
    sys.exit(0)
