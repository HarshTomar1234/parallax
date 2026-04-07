// List of all valid wiki pages (used for resolving [[wiki-links]])
const PGBase = '/wiki/';
const pages = [
  'projects/insureml-pipeline',
  'index', 'overview', 'log',
  // AGENT_INJECT_PAGES_START
  'projects/travel-planner', 'projects/tennis-vision', 'projects/quanta-ai', 'projects/deepguard', 'projects/decifra', 'projects/molecuquest', 'projects/field-fusion', 'projects/histopathology', 'projects/rppg-heart-rate',
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

// Determine correct base path for wiki files depending on environment
const wikiBase = window.location.pathname.includes('/landing') ? '../wiki/' : 'wiki/';

// Convert [[link]] to standard html links
function processWikiLinks(markdown) {
  return markdown.replace(/\[\[(.*?)\]\]/g, (match, p1) => {
    const route = resolvePagePath(p1);
    return `<a href="#/${route}">${p1}</a>`;
  });
}

// Extract and format YAML frontmatter
function processFrontmatter(markdown) {
  const frontmatterRegex = /^---\r?\n([\s\S]*?)\r?\n---/;
  const match = markdown.match(frontmatterRegex);
  
  let lastUpdatedHtml = '';

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
      
      let displayVal = processWikiLinks(val);
      // Auto-link any URLs
      displayVal = displayVal.replace(/(https?:\/\/[^\s\]]+)/g, '<a href="$1" target="_blank" style="color:var(--text-accent);text-decoration:underline;">$1</a>');
      
      fmHtml += `<div><strong>${key.trim()}:</strong> ${displayVal}</div>`;
      
      if (key.trim() === 'last_updated') {
        const dateStr = val.replace(/['"]/g, '');
        const dDate = new Date(dateStr);
        if (!isNaN(dDate)) {
           let days = Math.floor((new Date() - dDate) / (1000 * 60 * 60 * 24));
           if (days < 0) days = 0; // Fix negative timestamp diff due to timezone bounds
           const dayText = days === 0 ? 'today' : days === 1 ? 'yesterday' : `${days} days ago`;
           lastUpdatedHtml = `\n\n<div class="last-updated">Last modified: ${dayText} (${dateStr})</div>`;
        } else {
           lastUpdatedHtml = `\n\n<div class="last-updated">Last modified: ${dateStr}</div>`;
        }
      }
    });
    fmHtml += '</div>';
    
    return fmHtml + '\n\n' + restOfDoc + lastUpdatedHtml;
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
    const res = await fetch(`${wikiBase}${route}.md`);
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

// --- COMMAND PALETTE LOGIC ---
const searchIndex = [];
let searchDataLoaded = false;

async function buildSearchIndex() {
  if (searchDataLoaded) return;
  for (const page of pages) {
    try {
      const res = await fetch(`${wikiBase}${page}.md`);
      if (res.ok) {
        const text = await res.text();
        searchIndex.push({ path: page, content: text });
      }
    } catch(e) {}
  }
  searchDataLoaded = true;
}

const cpBackdrop = document.getElementById('command-palette-backdrop');
const cpInput = document.getElementById('cp-search-input');
const cpResults = document.getElementById('cp-results');
const cpCloseBtn = document.getElementById('cp-close');
const searchTriggerBtn = document.getElementById('search-trigger');
let activeResultIndex = -1;

function toggleCommandPalette(forceState) {
  const isHidden = cpBackdrop.classList.contains('hidden');
  const show = forceState !== undefined ? forceState : isHidden;
  
  if (show) {
    cpBackdrop.classList.remove('hidden');
    cpInput.focus();
    buildSearchIndex();
  } else {
    cpBackdrop.classList.add('hidden');
    cpInput.value = '';
    cpResults.innerHTML = '<div class="cp-empty">Type to search your wiki...</div>';
  }
}

// Event Listeners
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    toggleCommandPalette();
  }
  if (e.key === 'Escape' && !cpBackdrop.classList.contains('hidden')) {
    toggleCommandPalette(false);
  }
  
  // Navigation
  if (!cpBackdrop.classList.contains('hidden')) {
    const items = cpResults.querySelectorAll('.cp-item');
    if (items.length > 0) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeResultIndex = (activeResultIndex + 1) % items.length;
        updateActiveHover(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeResultIndex = (activeResultIndex - 1 + items.length) % items.length;
        updateActiveHover(items);
      } else if (e.key === 'Enter' && activeResultIndex >= 0) {
        e.preventDefault();
        const href = items[activeResultIndex].getAttribute('href');
        if (href) {
          toggleCommandPalette(false);
          window.location.href = href;
          // Fallback to force load if already on the same hash
          loadPage(href.replace('#/', ''));
        }
      }
    }
  }
});

function updateActiveHover(items) {
  items.forEach((item, idx) => {
    if (idx === activeResultIndex) {
      item.classList.add('active');
      item.scrollIntoView({ block: 'nearest' });
    } else {
      item.classList.remove('active');
    }
  });
}

cpBackdrop.addEventListener('click', (e) => {
  if (e.target === cpBackdrop) toggleCommandPalette(false);
});
cpCloseBtn.addEventListener('click', () => toggleCommandPalette(false));
if (searchTriggerBtn) searchTriggerBtn.addEventListener('click', () => toggleCommandPalette(true));

cpInput.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  if (!query) {
    cpResults.innerHTML = '<div class="cp-empty">Type to search your wiki...</div>';
    return;
  }
  if (!searchDataLoaded) {
    // If not loaded, trigger load and show loading message
    buildSearchIndex();
    cpResults.innerHTML = '<div class="cp-empty">Fetching index... please type again in a moment.</div>';
    return;
  }
  
  const results = [];
  for (const item of searchIndex) {
    const textLower = item.content.toLowerCase();
    const idx = textLower.indexOf(query);
    if (idx !== -1) {
      // Find a snippet around the match
      const start = Math.max(0, idx - 40);
      const end = Math.min(item.content.length, idx + query.length + 60);
      let snippet = item.content.substring(start, end).replace(/\n/g, ' ');
      
      // Highlight the keyword
      const regex = new RegExp(`(${query})`, 'gi');
      snippet = snippet.replace(regex, '<mark>$1</mark>');
      
      // Clean up title
      const titleName = item.path.split('/').pop().replace(/-/g, ' ');
      
      results.push({
        path: item.path,
        title: titleName.charAt(0).toUpperCase() + titleName.slice(1),
        snippet: `...${snippet}...`
      });
    }
  }
  
  if (results.length === 0) {
    cpResults.innerHTML = '<div class="cp-empty">No results found for "' + e.target.value + '"</div>';
  } else {
    activeResultIndex = 0;
    cpResults.innerHTML = results.map((r, i) => `
      <a href="#/${r.path}" class="cp-item ${i === 0 ? 'active' : ''}" onclick="toggleCommandPalette(false)">
        <div class="cp-item-title">${r.title} <span class="cp-item-path">/${r.path}</span></div>
        <div class="cp-item-snippet">${r.snippet}</div>
      </a>
    `).join('');
  }
});

// Initialize
window.addEventListener('DOMContentLoaded', () => {
  const hash = window.location.hash.replace('#/', '');
  loadPage(hash || 'index');
  // Pre-load wiki files in background for instant search
  if (window.requestIdleCallback) {
    window.requestIdleCallback(buildSearchIndex);
  } else {
    setTimeout(buildSearchIndex, 2000);
  }
});
