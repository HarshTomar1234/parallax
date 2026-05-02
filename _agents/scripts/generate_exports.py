#!/usr/bin/env python3
"""
Parallax Export Generator
Produces three AI-consumable artifacts from the wiki:

  wiki/llms.txt       — one-line summary per page (inject into LLM context)
  wiki/llms-full.txt  — full content of every page (complete context dump)
  wiki/graph.json     — nodes + edges knowledge graph (agent traversal)

Run manually or via CI before deployment:
  python _agents/scripts/generate_exports.py
"""

import os
import re
import json
import datetime

WIKI_DIR = 'wiki'
SKIP_SLUGS = {'log', 'llms', 'llms-full'}  # don't include the exports themselves


def parse_frontmatter(content):
    """Extract YAML frontmatter fields as a dict of raw strings."""
    fm = {}
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---', content)
    if not match:
        return fm
    for line in match.group(1).splitlines():
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        fm[key.strip()] = val.strip()
    return fm


def strip_frontmatter(content):
    """Remove YAML frontmatter block from content."""
    return re.sub(r'^---[\s\S]*?---\n', '', content).strip()


def extract_summary(body, slug):
    """Pull the first meaningful sentence/line from the page body."""
    # Try first non-header, non-empty line
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('|') or line.startswith('-') or line.startswith('*'):
            continue
        # Strip inline markdown
        clean = re.sub(r'\[\[([^\]]+)\]\]', r'\1', line)
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
        clean = re.sub(r'[`*_]', '', clean)
        clean = clean.strip('> ').strip()
        if len(clean) > 20:
            return clean[:200]
    return slug.replace('-', ' ').title()


def extract_wikilinks(content):
    """Return list of linked page slugs from [[wikilinks]] in content."""
    return list(set(re.findall(r'\[\[([^\]|]+)', content)))


def collect_pages():
    """Walk wiki/ and return list of page dicts."""
    pages = []
    for root, dirs, files in os.walk(WIKI_DIR):
        # Skip the exports themselves on re-runs
        dirs[:] = [d for d in dirs if d not in ('__pycache__',)]
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            slug = fname[:-3]
            if slug in SKIP_SLUGS:
                continue
            rel = os.path.relpath(os.path.join(root, fname), WIKI_DIR)
            page_id = rel.replace('\\', '/').replace('.md', '')

            content = open(os.path.join(root, fname), encoding='utf-8').read()
            fm = parse_frontmatter(content)
            body = strip_frontmatter(content)
            links = extract_wikilinks(content)

            pages.append({
                'id': page_id,
                'slug': slug,
                'title': fm.get('title', slug),
                'domain': fm.get('domain', ''),
                'tags': fm.get('tags', ''),
                'last_updated': fm.get('last_updated', ''),
                'confidence': float(fm.get('confidence', 0.8)),
                'summary': extract_summary(body, slug),
                'links': links,
                'body': body,
                'path': os.path.join(root, fname),
            })
    return pages


def write_llms_txt(pages):
    """One-line-per-page summary file for quick LLM context injection."""
    lines = [
        '# Parallax — @kernel_crush AI/ML Knowledge Graph',
        '# Generated: ' + datetime.date.today().isoformat(),
        '# Format: [domain/slug] Title — Summary',
        '#',
        '# Paste this file into any LLM context to make the full wiki queryable.',
        '',
    ]
    # Group by domain
    domains = {}
    for p in pages:
        domains.setdefault(p['domain'] or 'meta', []).append(p)

    domain_order = ['projects', 'research', 'skills', 'concepts', 'career', 'learning', 'meta', '']
    for domain in domain_order:
        if domain not in domains:
            continue
        lines.append(f'## {domain.upper() or "ROOT"}')
        for p in sorted(domains[domain], key=lambda x: x['id']):
            tags = p['tags'].strip('[]').replace('"', '').replace("'", '')
            lines.append(f"[{p['id']}] {p['title']} - {p['summary']}")
        lines.append('')

    out = '\n'.join(lines)
    with open(os.path.join(WIKI_DIR, 'llms.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    print(f"  wrote wiki/llms.txt ({len(pages)} pages, {len(out)} chars)")


def write_llms_full_txt(pages):
    """Full content dump — every page concatenated with clear delimiters."""
    sections = [
        '# Parallax — Full Wiki Dump',
        '# Generated: ' + datetime.date.today().isoformat(),
        '# Contains full content of all ' + str(len(pages)) + ' wiki pages.',
        '# Use for deep context injection or offline LLM search.',
        '',
    ]
    for p in sorted(pages, key=lambda x: x['id']):
        sections.append(f"{'='*60}")
        sections.append(f"PAGE: {p['id']}")
        sections.append(f"TITLE: {p['title']}")
        sections.append(f"DOMAIN: {p['domain']}")
        sections.append(f"TAGS: {p['tags']}")
        sections.append(f"LAST_UPDATED: {p['last_updated']}")
        sections.append(f"LINKS: {', '.join(p['links'])}")
        sections.append(f"{'='*60}")
        sections.append(p['body'])
        sections.append('')

    out = '\n'.join(sections)
    with open(os.path.join(WIKI_DIR, 'llms-full.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    print(f"  wrote wiki/llms-full.txt ({len(out):,} chars)")


def write_graph_json(pages):
    """JSON knowledge graph — nodes + edges for agent traversal."""
    slug_to_id = {p['slug']: p['id'] for p in pages}

    nodes = []
    for p in pages:
        nodes.append({
            'id': p['id'],
            'title': p['title'],
            'domain': p['domain'],
            'tags': [t.strip().strip('"\'') for t in p['tags'].strip('[]').split(',') if t.strip()],
            'last_updated': p['last_updated'],
            'confidence': p['confidence'],
            'summary': p['summary'],
            'inbound_count': 0,   # filled below
            'outbound_count': len(p['links']),
        })

    # Build edges and count inbound
    edges = []
    id_to_node = {n['id']: n for n in nodes}

    for p in pages:
        for linked_slug in p['links']:
            target_id = slug_to_id.get(linked_slug)
            if target_id and target_id != p['id']:
                edges.append({
                    'source': p['id'],
                    'target': target_id,
                })
                if target_id in id_to_node:
                    id_to_node[target_id]['inbound_count'] += 1

    graph = {
        'meta': {
            'generated': datetime.date.today().isoformat(),
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'owner': '@kernel_crush',
            'repo': 'https://github.com/HarshTomar1234/parallax',
        },
        'nodes': sorted(nodes, key=lambda n: n['id']),
        'edges': edges,
    }

    out = json.dumps(graph, indent=2, ensure_ascii=False)
    with open(os.path.join(WIKI_DIR, 'graph.json'), 'w', encoding='utf-8') as f:
        f.write(out)
    print(f"  wrote wiki/graph.json ({len(nodes)} nodes, {len(edges)} edges)")


if __name__ == '__main__':
    print('Parallax Export Generator')
    print(f'  Scanning {WIKI_DIR}/ ...')
    pages = collect_pages()
    print(f'  Found {len(pages)} pages')
    print()
    write_llms_txt(pages)
    write_llms_full_txt(pages)
    write_graph_json(pages)
    print()
    print('Done. Commit wiki/llms.txt, wiki/llms-full.txt, wiki/graph.json')
