#!/usr/bin/env python3
"""
Parallax Stale Metrics Checker

Checks two things:
1. Star counts — fetches live GitHub stars for every projects/ page and flags drift > 10%
2. Staleness — flags pages whose last_updated is older than the domain threshold (from AGENTS.md)

Opens a GitHub issue if anything is stale. Requires GITHUB_TOKEN env var.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.error
from datetime import date, timedelta
from pathlib import Path

WIKI_DIR = Path("wiki")
SKIP_DIRS = {".obsidian", "_templates", "_attachments"}
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = os.environ.get("REPO_OWNER", "HarshTomar1234")
REPO_NAME = "parallax"

# Days before a page is considered stale per domain (mirrors AGENTS.md)
STALENESS_DAYS = {
    "projects": 90,
    "research": 180,
    "skills": 180,
    "concepts": 365,
    "career": 60,
    "learning": 90,
    "meta": 30,
}


def _gh_api(path: str) -> dict:
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  [warn] GitHub API {path} → HTTP {e.code}")
        return {}


def _parse_frontmatter(content: str) -> dict:
    fm_match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", content)
    if not fm_match:
        return {}
    fm = fm_match.group(1)
    result = {}
    for key in ("title", "domain", "last_updated"):
        m = re.search(rf"^{key}:\s*(.+)", fm, re.MULTILINE)
        if m:
            result[key] = m.group(1).strip()
    # Extract star count from body: look for "Stars:** N" or "**Stars:** N"
    stars_m = re.search(r"\*\*Stars:\*\*\s*(\d+)", content)
    if stars_m:
        result["wiki_stars"] = int(stars_m.group(1))
    # Extract repo slug from GitHub URL in body
    repo_m = re.search(r"github\.com/[^/]+/([A-Za-z0-9_.-]+)", content)
    if repo_m:
        result["github_repo"] = repo_m.group(1)
    return result


def _load_pages() -> list[dict]:
    pages = []
    for root, dirs, files in os.walk(WIKI_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            path = Path(root) / fname
            content = path.read_text(encoding="utf-8")
            meta = _parse_frontmatter(content)
            meta["slug"] = path.stem
            meta["path"] = str(path)
            pages.append(meta)
    return pages


def check_star_drift(pages: list[dict]) -> list[str]:
    """Return list of stale star-count warnings."""
    warnings = []
    project_pages = [p for p in pages if p.get("domain") == "projects" and p.get("github_repo")]

    for p in project_pages:
        repo = p["github_repo"]
        wiki_stars = p.get("wiki_stars")
        if wiki_stars is None:
            continue

        data = _gh_api(f"/repos/{REPO_OWNER}/{repo}")
        live_stars = data.get("stargazers_count")
        if live_stars is None:
            print(f"  [skip] {repo} — could not fetch live stars")
            continue

        if wiki_stars == 0:
            drift_pct = 100 if live_stars > 0 else 0
        else:
            drift_pct = abs(live_stars - wiki_stars) / wiki_stars * 100

        if drift_pct > 10:
            warnings.append(
                f"**{p['slug']}** — wiki says ★{wiki_stars}, GitHub says ★{live_stars} "
                f"({drift_pct:.0f}% drift)"
            )
            print(f"  [stale stars] {p['slug']}: wiki={wiki_stars} live={live_stars}")
        else:
            print(f"  [ok] {p['slug']}: ★{live_stars} (within 10% of wiki ★{wiki_stars})")

    return warnings


def check_staleness(pages: list[dict]) -> list[str]:
    """Return list of pages past their domain staleness threshold."""
    warnings = []
    today = date.today()

    for p in pages:
        domain = p.get("domain", "")
        threshold = STALENESS_DAYS.get(domain)
        last_updated_str = p.get("last_updated", "")
        if not threshold or not last_updated_str:
            continue
        try:
            last_updated = date.fromisoformat(last_updated_str)
        except ValueError:
            continue

        age_days = (today - last_updated).days
        if age_days > threshold:
            warnings.append(
                f"**{p['slug']}** (`{domain}`) — last updated {last_updated_str} "
                f"({age_days} days ago, threshold {threshold}d)"
            )
            print(f"  [stale page] {p['slug']}: {age_days}d old (threshold {threshold}d)")

    return warnings


def open_github_issue(star_warns: list[str], stale_warns: list[str]) -> None:
    lines = ["Automated stale metrics check found the following issues:\n"]

    if star_warns:
        lines.append("## Star Count Drift (>10% from live GitHub)\n")
        lines.extend(f"- {w}" for w in star_warns)
        lines.append("")

    if stale_warns:
        lines.append("## Pages Past Staleness Threshold\n")
        lines.extend(f"- {w}" for w in stale_warns)
        lines.append("")

    lines.append("\n_Update the affected wiki pages and bump `last_updated` to close this issue._")
    body = "\n".join(lines)

    payload = json.dumps({
        "title": f"[stale-check] Metrics drift detected — {date.today().isoformat()}",
        "body": body,
        "labels": ["stale", "automated"],
    }).encode()

    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            print(f"\nIssue opened: {data.get('html_url', '(no URL)')}")
    except Exception as e:
        print(f"\n[error] Could not open issue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("=== Parallax Stale Metrics Check ===\n")

    pages = _load_pages()
    print(f"Pages loaded: {len(pages)}\n")

    print("--- Star count drift ---")
    star_warns = check_star_drift(pages)

    print("\n--- Page staleness ---")
    stale_warns = check_staleness(pages)

    total = len(star_warns) + len(stale_warns)
    print(f"\nTotal issues: {total}")

    if total == 0:
        print("All metrics up to date.")
        sys.exit(0)

    if not GITHUB_TOKEN:
        print("\n[warn] No GITHUB_TOKEN — skipping issue creation.")
        for w in star_warns + stale_warns:
            print(f"  {w}")
        sys.exit(0)

    print("\nOpening GitHub issue...")
    open_github_issue(star_warns, stale_warns)
