#!/usr/bin/env python3
"""
Autonomous LLM Ingest Agent for Parallax
Takes a GitHub repo URL, fetches the README, passes it to Gemini API,
and generates a fully compliant Parallax Wiki Markdown page.
"""

import os
import sys
import argparse
import requests
import re
import datetime
from urllib.parse import urlparse

# Ensure Gemini API is available
try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai is not installed.")
    sys.exit(1)

def extract_github_info(url):
    """Extract owner and repo from a github URL."""
    # Handle https://github.com/owner/repo
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    if len(path_parts) >= 2:
        return path_parts[0], path_parts[1]
    return None, None

def fetch_repo_readme(owner, repo):
    """Fetch the default branch README from GitHub."""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error fetching README: {response.status_code} - {response.text}")
        return None

def generate_wiki_markdown(readme_text, repo_url, domain, repo_name):
    """Use Gemini to generate the Wiki page."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
         print("Error: GEMINI_API_KEY environment variable not set.")
         sys.exit(1)
         
    genai.configure(api_key=api_key)
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
You are an autonomous LLM agent maintaining the Parallax wiki for @kernel_crush (Harsh Tomar).
Your task is to ingest a GitHub repository's README and write a highly technical, minimal "no-fluff" wiki page.
DO NOT use code blocks for architecture diagrams, flowcharts, or tech stacks. Everything must use native Markdown lists, bullet points, headers, or blockquotes.
The output should be RAW markdown with NO wrapping ```markdown blocks. Just the raw text.

You MUST include this YAML frontmatter exactly at the top:
---
title: {repo_name}
domain: {domain}
tags: [generate 3-4 relevant technical tags]
sources: [{repo_url}]
last_updated: {today}
links: []
---

Here is the repository README:
====================
{readme_text}
====================

Write the page following the Parallax style guidelines:
- Terse, precise, technical
- Use tables for comparisons if needed
- Use bullet points for tech stacks and features
- Avoid filler phrases ("this project demonstrates")
- Headers should be noun phrases
- Absolutely ZERO code blocks (```) for infrastructure or architecture.
"""
    # Bulletproof fallback logic for models
    try:
        print(f"Calling Gemini API (gemini-2.0-flash) for {repo_name}...")
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
    except Exception as e:
        print(f"Warning: Flash model failed ({e}). Falling back to gemini-2.5-flash...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
    
    text = response.text
    # Remove possible markdown wrapper from LLM output
    if text.startswith("```markdown"):
        text = text.replace("```markdown\n", "", 1)
    if text.startswith("```"):
        text = text.replace("```\n", "", 1)
    if text.endswith("```"):
        text = text[:-3].strip()
        
    return text

def update_registry(domain, repo_name, slug):
    """Automatically update index.md, script.js, and index.html to reflect the new page."""
    print(f"Updating registry files for {domain}/{slug}...")
    
    # 1. Update landing/script.js
    script_file = "landing/script.js"
    if os.path.exists(script_file):
        with open(script_file, "r", encoding="utf-8") as f:
            js_content = f.read()
        js_content = js_content.replace(
            "const pages = [",
            f"const pages = [\n  '{domain}/{slug}',"
        )
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(js_content)

    # 2. Update landing/index.html (Sidebar)
    html_file = "landing/index.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        target_group = "Projects" if domain == "projects" else "Research"
        html_target = f'<div class="nav-group-title">{target_group}</div>'
        html_inject = f'{html_target}\n          <a href="#" class="nav-item" data-page="{domain}/{slug}">{repo_name.replace("-", " ").title()}</a>'
        
        html_content = html_content.replace(html_target, html_inject)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

    # 3. Update wiki/index.md (Master Table)
    index_file = "wiki/index.md"
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            index_content = f.read()
            
        if domain == "projects":
            table_target = "|------|--------|---------|-------------|"
            table_inject = f"{table_target}\n| [[{slug}]] | Auto | Newly ingested repository | Actions, LLM |"
        else:
            table_target = "|------|-------------|---------|---------|-------------|"
            table_inject = f"{table_target}\n| [[{slug}]] | Auto | Newly ingested research | ~ | Actions, LLM |"
            
        index_content = index_content.replace(table_target, table_inject)
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(index_content)


def main():
    parser = argparse.ArgumentParser(description="Parallax Agent: Ingest GitHub Repo")
    parser.add_argument("--repo-url", required=True, help="GitHub Repository URL")
    parser.add_argument("--domain", required=True, choices=["projects", "research"], help="Target domain folder")
    args = parser.parse_args()

    owner, repo = extract_github_info(args.repo_url)
    if not owner or not repo:
        print("Invalid GitHub URL provided.")
        sys.exit(1)
        
    print(f"Ingesting {owner}/{repo}")
    
    readme = fetch_repo_readme(owner, repo)
    if not readme:
        sys.exit(1)
        
    markdown_content = generate_wiki_markdown(readme, args.repo_url, args.domain, repo)
    
    # Save to file
    out_dir = os.path.join("wiki", args.domain)
    os.makedirs(out_dir, exist_ok=True)
    slug = repo.lower()
    out_file = os.path.join(out_dir, f"{slug}.md")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"Successfully generated {out_file}")
    
    # Update all registry files to wire the new page
    update_registry(args.domain, repo, slug)
    
    # Also log it
    log_file = os.path.join("wiki", "log.md")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(log_file):
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n## [{today}] ingest | Autonomous run for {args.repo_url} via Action\n")
            f.write(f"- Auto-generated `wiki/{args.domain}/{slug}.md`\n")
            f.write(f"- Auto-updated `index.html`, `script.js`, and `index.md` registry\n")

if __name__ == "__main__":
    main()
