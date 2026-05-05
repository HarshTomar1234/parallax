// List of all valid wiki pages (used for resolving [[wiki-links]])
const PGBase = '/wiki/';
const pages = [
  'projects/insureml-pipeline',
  'index', 'overview', 'log',
  // AGENT_INJECT_PAGES_START
  'learning/machine-and-deep-learning-nlp', 'learning/agentforge', 'learning/pytorch-lora-qlora',

  'projects/travel-planner', 'projects/tennis-vision', 'projects/quanta-ai', 'projects/deepguard', 'projects/decifra', 'projects/molecuquest', 'projects/field-fusion', 'projects/histopathology', 'projects/rppg-heart-rate',
  'research/transformers-cv', 'research/vlmverse', 'research/lora-qlora', 'research/reasoning-llms', 'research/vision-transformer',
  'skills/computer-vision', 'skills/genai-agents', 'skills/mlops', 'skills/deep-learning',
  'concepts/attention-mechanisms', 'concepts/diffusion-models', 'concepts/rag-architectures', 'concepts/lora-theory', 'concepts/object-detection', 'concepts/multi-object-tracking',
  'career/ai-internship', 'career/community', 'career/open-source', 'career/writing',
  'meta/knowledge-gaps', 'meta/connections', 'meta/synthesis'
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

  // Reset progress bar and render breadcrumb immediately
  resetProgressBar();
  renderBreadcrumb(route);

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

    // Extract confidence before processing frontmatter
    const confMatch = markdown.match(/^confidence:\s*([\d.]+)/m);
    const confidence = confMatch ? confMatch[1] : null;

    // Process custom syntax
    markdown = processFrontmatter(markdown);
    markdown = processWikiLinks(markdown);

    // Render using marked.js
    const badge = renderConfidenceBadge(confidence);
    container.innerHTML = (badge ? badge : '') + marked.parse(markdown);

    // Scroll to top
    document.getElementById('content').scrollTo(0, 0);

    // Update shareable URL: ?page=slug + #/slug (skip for index to keep root URL clean)
    if (route && route !== 'index') {
      history.replaceState(null, '', `?page=${route}#/${route}`);
    } else {
      history.replaceState(null, '', window.location.pathname);
    }

  } catch (err) {
    console.error(err);
    container.innerHTML = `<h1>Error</h1><p>Could not load the page locally. Make sure the local python server is running.</p>`;
  }
}

// Router
function handleHashChange() {
  let hash = window.location.hash.replace('#/', '');
  loadPage(hash || 'index');
  closeMobileSidebar();
}

window.addEventListener('hashchange', handleHashChange);

// Sidebar Toggle — desktop collapse + mobile slide
const layout = document.getElementById('layout');
const sidebar = document.getElementById('sidebar');

// Restore desktop collapsed state
if (localStorage.getItem('sidebar-collapsed') === 'true') {
  layout.classList.add('sidebar-collapsed');
}

const sidebarBackdrop = document.getElementById('sidebar-backdrop');

function closeMobileSidebar() {
  sidebar.classList.remove('open');
  sidebarBackdrop.classList.remove('visible');
}

document.getElementById('sidebar-toggle').addEventListener('click', () => {
  if (window.innerWidth <= 768) {
    const isOpen = sidebar.classList.toggle('open');
    sidebarBackdrop.classList.toggle('visible', isOpen);
  } else {
    const collapsed = layout.classList.toggle('sidebar-collapsed');
    localStorage.setItem('sidebar-collapsed', collapsed);
  }
});

sidebarBackdrop.addEventListener('click', closeMobileSidebar);

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
  try {
    // Fast path: single fetch of pre-built index (generated by CI)
    const res = await fetch(`${wikiBase}search-index.json`);
    if (res.ok) {
      const data = await res.json();
      searchIndex.push(...data);
      searchDataLoaded = true;
      return;
    }
  } catch(e) {}
  // Fallback: fetch individual .md files (local dev without generated index)
  for (const page of pages) {
    try {
      const res = await fetch(`${wikiBase}${page}.md`);
      if (res.ok) {
        const text = await res.text();
        const slug = page.split('/').pop().replace(/-/g, ' ');
        searchIndex.push({
          path: page,
          title: slug.charAt(0).toUpperCase() + slug.slice(1),
          content: text,
        });
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
  
  // Strip markdown for clean snippet display
  function cleanSnippet(raw) {
    return raw
      .replace(/^---[\s\S]*?---\n/, '')      // frontmatter
      .replace(/\[\[([^\]]+)\]\]/g, '$1')     // [[wikilinks]] → text
      .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1') // [text](url) → text
      .replace(/^#{1,6}\s+/gm, '')            // headings
      .replace(/\*\*([^*]+)\*\*/g, '$1')      // bold
      .replace(/\*([^*]+)\*/g, '$1')          // italic
      .replace(/`[^`]+`/g, '')               // inline code
      .replace(/^\|.*\|$/gm, '')             // table rows
      .replace(/^[-*]\s+/gm, '')             // list markers
      .replace(/^---+$/gm, '')               // hr
      .replace(/\n{2,}/g, ' ')               // collapse newlines
      .replace(/\s{2,}/g, ' ')               // collapse spaces
      .trim();
  }

  const results = [];
  for (const item of searchIndex) {
    const textLower = item.content.toLowerCase();
    const idx = textLower.indexOf(query);
    if (idx !== -1) {
      const start = Math.max(0, idx - 40);
      const end = Math.min(item.content.length, idx + query.length + 60);
      let raw = item.content.substring(start, end);
      let snippet = cleanSnippet(raw);

      // Highlight the keyword
      const regex = new RegExp(`(${query})`, 'gi');
      snippet = snippet.replace(regex, '<mark>$1</mark>');

      results.push({
        path: item.path,
        title: item.title || (item.path.split('/').pop().replace(/-/g, ' ').replace(/^\w/, c => c.toUpperCase())),
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

// --- THEME TOGGLE (F4) ---
const themeToggleBtn  = document.getElementById('theme-toggle');
const themeIconMoon   = document.getElementById('theme-icon-moon');
const themeIconSun    = document.getElementById('theme-icon-sun');

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const isLight = theme === 'light';
  themeIconMoon.style.display = isLight ? 'none'  : '';
  themeIconSun.style.display  = isLight ? ''      : 'none';
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  applyTheme(next);
  localStorage.setItem('parallax-theme', next);
}

themeToggleBtn.addEventListener('click', toggleTheme);
// Restore saved preference on load
applyTheme(localStorage.getItem('parallax-theme') || 'dark');


// --- READING PROGRESS BAR (F1) ---
const progressBar = document.getElementById('progress-bar');
const contentEl   = document.getElementById('content');

contentEl.addEventListener('scroll', () => {
  const scrollTop    = contentEl.scrollTop;
  const scrollHeight = contentEl.scrollHeight - contentEl.clientHeight;
  const pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
  progressBar.style.width = pct + '%';
});

function resetProgressBar() {
  progressBar.style.width = '0%';
}


// --- BREADCRUMB (F2) ---
const breadcrumbEl = document.getElementById('breadcrumb');
const BREADCRUMB_HIDE = new Set(['index', 'overview']);

function renderBreadcrumb(route) {
  if (!route || BREADCRUMB_HIDE.has(route)) {
    breadcrumbEl.classList.add('hidden');
    return;
  }
  const parts = route.split('/');
  let html = `<a href="#/index">Home</a>`;
  if (parts.length === 2) {
    const domain  = parts[0].charAt(0).toUpperCase() + parts[0].slice(1);
    const pageName = parts[1].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    html += `<span class="breadcrumb-sep">/</span><span>${domain}</span>`;
    html += `<span class="breadcrumb-sep">/</span><span class="breadcrumb-current">${pageName}</span>`;
  } else {
    const pageName = parts[0].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    html += `<span class="breadcrumb-sep">/</span><span class="breadcrumb-current">${pageName}</span>`;
  }
  breadcrumbEl.innerHTML = html;
  breadcrumbEl.classList.remove('hidden');
}


// --- CONFIDENCE BADGE (F3) ---
function renderConfidenceBadge(confidence) {
  if (confidence === null || confidence === undefined) return '';
  const val = parseFloat(confidence);
  if (isNaN(val)) return '';
  let cls, label, dot;
  if      (val >= 0.9) { cls = 'verified'; label = 'Verified';    dot = '●'; }
  else if (val >= 0.7) { cls = 'high';     label = 'High';        dot = '●'; }
  else if (val >= 0.5) { cls = 'medium';   label = 'Medium';      dot = '●'; }
  else                 { cls = 'low';      label = 'Speculative';  dot = '○'; }
  return `<span class="confidence-badge ${cls}" title="Confidence score: ${val}">${dot} ${label} (${val})</span>`;
}


// --- KNOWLEDGE GRAPH ---
const DOMAIN_COLORS = {
  projects:  '#3b82f6',
  research:  '#8b5cf6',
  skills:    '#10b981',
  concepts:  '#f59e0b',
  career:    '#ec4899',
  learning:  '#06b6d4',
  meta:      '#6b7280',
};

const graphOverlay  = document.getElementById('graph-overlay');
const graphTrigger  = document.getElementById('graph-trigger');
const graphClose    = document.getElementById('graph-close');
const graphLegend   = document.getElementById('graph-legend');
const graphMetaEl   = document.getElementById('graph-meta');
const graphTooltip  = document.getElementById('graph-tooltip');

let graphLoaded     = false;
let graphSimulation = null;

function toggleGraph(show) {
  const isHidden = graphOverlay.classList.contains('hidden');
  if (show === undefined) show = isHidden;
  if (show) {
    graphOverlay.classList.remove('hidden');
    // Wait for overlay to paint before reading dimensions — fixes mobile centering
    requestAnimationFrame(() => {
      if (!graphLoaded) {
        loadKnowledgeGraph();
      } else if (graphSimulation) {
        const w = graphOverlay.clientWidth;
        const h = graphOverlay.clientHeight - 52;
        d3.select('#graph-svg').attr('width', w).attr('height', h);
        graphSimulation.force('center', d3.forceCenter(w / 2, h / 2)).alpha(0.3).restart();
      }
    });
  } else {
    graphOverlay.classList.add('hidden');
    graphTooltip.classList.add('hidden');
  }
}

graphTrigger.addEventListener('click', () => toggleGraph(true));
graphClose.addEventListener('click',   () => toggleGraph(false));

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !graphOverlay.classList.contains('hidden')) {
    toggleGraph(false);
  }
});

async function loadKnowledgeGraph() {
  try {
    const res = await fetch(`${wikiBase}graph.json`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    graphMetaEl.textContent = `${data.meta.total_nodes} nodes · ${data.meta.total_edges} edges`;

    // Build legend
    const domains = [...new Set(data.nodes.map(n => n.domain))].sort();
    graphLegend.innerHTML = domains.map(d =>
      `<div class="legend-item">
        <span class="legend-dot" style="background:${DOMAIN_COLORS[d] || '#888'}"></span>
        <span>${d}</span>
       </div>`
    ).join('');

    renderGraph(data.nodes, data.edges);
    graphLoaded = true;
  } catch (err) {
    graphMetaEl.textContent = 'unavailable';
    const svg = document.getElementById('graph-svg');
    svg.innerHTML = `<text x="50%" y="50%" fill="#555" text-anchor="middle"
      font-family="Inter,sans-serif" font-size="14">
      graph.json not found — run: python _agents/scripts/generate_exports.py
    </text>`;
  }
}

function nodeRadius(d) {
  return Math.min(20, 5 + (d.inbound_count || 0) * 2);
}

function renderGraph(nodes, rawEdges) {
  const svgEl = document.getElementById('graph-svg');
  const width  = graphOverlay.clientWidth  || window.innerWidth;
  const height = (graphOverlay.clientHeight || window.innerHeight) - 52;

  const svg = d3.select(svgEl)
    .attr('width',  width)
    .attr('height', height);

  svg.selectAll('*').remove();

  // Zoom + pan
  const g = svg.append('g');
  svg.call(
    d3.zoom().scaleExtent([0.15, 5])
      .on('zoom', event => g.attr('transform', event.transform))
  );

  // Deep-copy edges so D3 doesn't mutate graph.json data
  const edges = rawEdges.map(e => ({ source: e.source, target: e.target }));

  const sim = d3.forceSimulation(nodes)
    .force('link',      d3.forceLink(edges).id(d => d.id).distance(90).strength(0.4))
    .force('charge',    d3.forceManyBody().strength(-250))
    .force('center',    d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(d => nodeRadius(d) + 6));

  graphSimulation = sim;

  // Edges
  const link = g.append('g')
    .selectAll('line')
    .data(edges)
    .enter().append('line')
    .attr('stroke', '#333')
    .attr('stroke-width', 1)
    .attr('stroke-opacity', 0.55);

  // Node groups
  const node = g.append('g')
    .selectAll('g')
    .data(nodes)
    .enter().append('g')
    .attr('cursor', 'pointer')
    .call(
      d3.drag()
        .on('start', (event, d) => {
          if (!event.active) sim.alphaTarget(0.3).restart();
          d.fx = d.x; d.fy = d.y;
        })
        .on('drag',  (event, d) => { d.fx = event.x; d.fy = event.y; })
        .on('end',   (event, d) => {
          if (!event.active) sim.alphaTarget(0);
          d.fx = null; d.fy = null;
        })
    );

  // Circles
  node.append('circle')
    .attr('r',              nodeRadius)
    .attr('fill',           d => DOMAIN_COLORS[d.domain] || '#6b7280')
    .attr('fill-opacity',   0.85)
    .attr('stroke',         d => DOMAIN_COLORS[d.domain] || '#6b7280')
    .attr('stroke-width',   1.5)
    .attr('stroke-opacity', 0.35);

  // Labels for high-traffic nodes
  node.filter(d => (d.inbound_count || 0) >= 3)
    .append('text')
    .text(d => d.title.length > 18 ? d.title.slice(0, 16) + '…' : d.title)
    .attr('x', d => nodeRadius(d) + 5)
    .attr('y', 4)
    .attr('fill', '#c4c4c4')
    .attr('font-size', '11px')
    .attr('font-family', 'Inter, sans-serif')
    .attr('pointer-events', 'none');

  // Hover + click
  node
    .on('mouseenter', (event, d) => {
      const color = DOMAIN_COLORS[d.domain] || '#888';
      graphTooltip.classList.remove('hidden');
      graphTooltip.innerHTML = `
        <div class="tt-title" style="color:${color}">${d.title}</div>
        <div class="tt-meta">${d.domain} &middot; ${d.inbound_count || 0} inbound links</div>
        ${d.summary ? `<div class="tt-summary">${d.summary.slice(0, 100)}&hellip;</div>` : ''}
      `;
    })
    .on('mousemove', event => {
      graphTooltip.style.left = (event.clientX + 14) + 'px';
      graphTooltip.style.top  = (event.clientY - 12) + 'px';
    })
    .on('mouseleave', () => graphTooltip.classList.add('hidden'))
    .on('click', (event, d) => {
      toggleGraph(false);
      window.location.hash = `/${d.id}`;
      loadPage(d.id);
    });

  // Tick
  sim.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);
    node.attr('transform', d => `translate(${d.x},${d.y})`);
  });
}

// Re-center graph on window resize
window.addEventListener('resize', () => {
  if (graphLoaded && graphSimulation && !graphOverlay.classList.contains('hidden')) {
    const w = window.innerWidth;
    const h = window.innerHeight - 52;
    d3.select('#graph-svg').attr('width', w).attr('height', h);
    graphSimulation.force('center', d3.forceCenter(w / 2, h / 2)).alpha(0.1).restart();
  }
});

// Initialize
window.addEventListener('DOMContentLoaded', () => {
  // Deep-link: ?page= takes priority, then hash, then default index
  const params = new URLSearchParams(window.location.search);
  const pageParam = params.get('page');
  const hash = window.location.hash.replace('#/', '');
  const initial = pageParam || hash || 'index';
  loadPage(initial);
  // Pre-load search index in background for instant Ctrl+K
  if (window.requestIdleCallback) {
    window.requestIdleCallback(buildSearchIndex);
  } else {
    setTimeout(buildSearchIndex, 2000);
  }
});
