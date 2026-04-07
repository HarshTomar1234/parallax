---
description: Ingests a new GitHub repository or content source to automatically build out a new Parallax wiki page.
---

# Ingest Workflow

When the user triggers this workflow (e.g. by typing `/ingest <github-url>`), execute the following steps explicitly and purely as an AI agent maintaining the Parallax wiki:

1. **Analyze Target**
   - Identify the provided GitHub URL or codebase.
   - Use your `read_url_content` tool to fetch the `README.md` or use terminal tools to temporarily `git clone` the repository into the `/tmp/` directory to scrape the code structure, tech stack, and purpose.

2. **Generate Native Markdown**
   - Synthesize a highly technical, minimal "no-fluff" page based on `AGENTS.md` rules.
   - Make sure to strictly include the YAML frontmatter:
     ```yaml
     ---
     title: [Project Name]
     domain: projects (or research)
     tags: [relevant-tags]
     sources: [github-link]
     last_updated: [YYYY-MM-DD]
     links: []
     ---
     ```
   - Save this new `.md` file to `d:\LLM-wiki\wiki\projects\` (if production) or `d:\LLM-wiki\wiki\research\` (if from-scratch implementation).

3. **Update Master Graphs**
   - Open `d:\LLM-wiki\wiki\index.md`. Include the newly generated project at the top of the relevant category table with its Domain, Summary, and Skills Used.
   - Append an entry to `d:\LLM-wiki\wiki\log.md` logging exactly what was ingested and when.

4. **Verify & Push**
// turbo
   - Once the local files are successfully created and modified, run `git add .` and `git commit -m "docs: agentic ingest for <Project Name>"`
// turbo
   - Run `git push` to sync the newly established knowledge up to the master repository.

5. **Report to User**
   - Notify the user that the Ingest protocol has finished and provide the local path view/link of the newly generated markdown documentation.
