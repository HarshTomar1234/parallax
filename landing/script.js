// List of all valid wiki pages (used for resolving [[wiki-links]])
const PGBase = '/wiki/';
const pages = [
  'index', 'overview', 'log',
  'projects/tennis-vision', 'projects/quanta-ai', 'projects/deepguard', 'projects/decifra', 'projects/molecuquest', 'projects/field-fusion', 'projects/histopathology', 'projects/rppg-heart-rate',
  'research/transformers-cv', 'research/vlmverse', 'research/lora-qlora', 'research/reasoning-llms', 'research/vision-transformer',
  'skills/computer-vision', 'skills/genai-agents', 'skills/mlops', 'skills/deep-learning',
  'concepts/attention-mechanisms', 'concepts/diffusion-models', 'concepts/rag-architectures', 'concepts/lora-theory', 'concepts/object-detection', 'concepts/multi-object-tracking',
  'career/ai-internship', 'career/community', 'career/open-source',
  'meta/knowledge-gaps', 'meta/connections'
];

function resolvePagePath(linkName) {
  const normalized = linkName.toLowerCase().replace(/\s+/g, '-');
  const exactMatch = pages.find(p => p === normalized);
  if (exactMatch) return exactMatch;
  const suffixMatch = pages.find(p => p.endsWith('/' + normalized));
  if (suffixMatch) return suffixMatch;
  return normalized; // fallback
}

// Convert [[link]] to standard html links
function processWikiLinks(markdown) {
  return markdown.replace(/\[\[(.*?)\]\]/g, (match, p1) => {
    const route = resolvePagePath(p1);
    return `<a href="#/${route}">${p1}</a>`;
  });
}

// Extract and format YAML frontmatter
function processFrontmatter(markdown) {
  const frontmatterRegex = /^---\n([\s\S]*?)\n---/;
  const match = markdown.match(frontmatterRegex);
  
  if (match) {
    const fmContent = match[1];
    const restOfDoc = markdown.slice(match[0].length).trim();
    
    // Parse basic yaml keys
    const lines = fmContent.split('\n');
    let fmHtml = '<div class="frontmatter">';
    lines.forEach(line => {
      if (!line.includes(':')) return;
      const [key, ...vals] = line.split(':');
      const val = vals.join(':').trim();
      fmHtml += `<div><strong>${key.trim()}:</strong> ${processWikiLinks(val)}</div>`;
    });
    fmHtml += '</div>';
    
    return fmHtml + restOfDoc;
  }
  return markdown;
}

// Render markdown to screen
async function loadPage(route) {
  if (!route) route = 'index';
  
  // Highlight active nav item
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const navItem = document.querySelector(`.nav-item[data-page="${route}"]`);
  if (navItem) navItem.classList.add('active');

  const container = document.getElementById('article-container');
  container.innerHTML = '<div style="color:var(--text-muted); padding: 2rem;">Loading...</div>';

  try {
    const res = await fetch(`../wiki/${route}.md`);
    if (!res.ok) {
      if (res.status === 404) {
        container.innerHTML = `<h1>404</h1><p>Page <code>${route}</code> not found.</p>`;
      } else {
        throw new Error('Failed to fetch');
      }
      return;
    }
    
    let markdown = await res.text();
    
    // Process custom syntax
    markdown = processFrontmatter(markdown);
    markdown = processWikiLinks(markdown);
    
    // Render using marked.js
    container.innerHTML = marked.parse(markdown);
    
    // Scroll to top
    document.getElementById('content').scrollTo(0,0);
    
  } catch (err) {
    console.error(err);
    container.innerHTML = `<h1>Error</h1><p>Could not load the page locally. Make sure the local python server is running.</p>`;
  }
}

// Router
function handleHashChange() {
  let hash = window.location.hash.replace('#/', '');
  loadPage(hash || 'index');
  
  // Close sidebar on mobile after nav
  document.getElementById('sidebar').classList.remove('open');
}

window.addEventListener('hashchange', handleHashChange);

// Sidebar Toggle
document.getElementById('sidebar-toggle').addEventListener('click', () => {
  document.getElementById('sidebar').classList.toggle('open');
});

// Setup click handlers for nav
document.querySelectorAll('.nav-item').forEach(el => {
  el.addEventListener('click', (e) => {
    e.preventDefault();
    const page = el.getAttribute('data-page');
    window.location.hash = `/${page}`;
  });
});
document.querySelector('.logo').addEventListener('click', (e) => {
  e.preventDefault();
  window.location.hash = `/index`;
});

// Initialize
window.addEventListener('DOMContentLoaded', () => {
  const hash = window.location.hash.replace('#/', '');
  loadPage(hash || 'index');
});
