const API = "http://localhost:8000";
let currentKey = null;

// ---------- helpers ----------
function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function makeSegments(line) {
  const parts = String(line).split("__");
  if (parts.length % 2 === 0) {
    throw new Error(`Unmatched __ in line: ${line}`);
  }
  return parts;
}

/**
 * Inside __ __ we expect: "Visible text, link-<number>, <resolvedKey>"
 * We render it as: <a href="#" data-key="resolvedKey">Visible text</a>
 */
function makeHtmlLink(line) {
  const segments = makeSegments(line);
  const out = [];

  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i];

    if (i % 2 === 0) {
      out.push(escapeHtml(segment));
      continue;
    }

    const m = segment.match(/^(.*),\s*link-(.*),\s*(.*)$/);
    if (!m) throw new Error(`Invalid link format in segment: ${segment}`);

    const s = m[1];
    const resolvedKey = m[3];

    out.push(
      `<a class="inline-link" href="#" data-key="${escapeHtml(resolvedKey)}">` +
      `${escapeHtml(s)}` +
      `</a>`
    );
  }

  return out.join("");
}

/**
 * Render ONE fetched entry as a nice HTML card.
 * "Referenced by" uses only refKey (no keyword_name lookup).
 */
function renderEntry(key, entry) {
  const section = [];

  section.push(`<section class="card" data-entry-key="${escapeHtml(key)}">`);
  section.push(`<h2>${escapeHtml(entry["$keyword_name"] ?? key)}</h2>`);

  for (const [property, propertyList] of Object.entries(entry)) {
    if (property === "$links" || property === "$keyword_name") continue;

    if (property === "$remark") {
      const remark = (propertyList || []).slice(1).map(escapeHtml).join(", ");
      if (remark) section.push(`<blockquote>${remark}</blockquote>`);
      continue;
    }

    if (!propertyList || propertyList.length === 0) continue;

    section.push(`<div class="topic">`);
    section.push(`<h3>${escapeHtml(propertyList[0])}</h3>`);
    section.push(`<ul>`);
    for (const line of propertyList.slice(1)) {
      section.push(`<li>${makeHtmlLink(line)}</li>`);
    }
    section.push(`</ul>`);
    section.push(`</div>`);
  }

  const links = entry["$links"];
  if (Array.isArray(links) && links.length > 0) {
    section.push(`<div class="references">`);
    section.push(`<h3>Referenced by</h3>`);
    section.push(`<ul>`);

    for (const link of links) {
      const via = link?.[1] ?? "";
      const refKey = link?.[2];
      if (!refKey) continue;

      section.push(
        `<li>` +
          `<a class="back-link" href="#" data-key="${escapeHtml(refKey)}">` +
            `${escapeHtml(refKey)}` +
          `</a>` +
          (via ? ` via ${escapeHtml(via)}` : ``) +
        `</li>`
      );
    }

    section.push(`</ul>`);
    section.push(`</div>`);
  }

  section.push(`</section>`);
  return section.join("\n");
}

// ---------- fetch + replace ----------
async function renderKeyIntoBlock(key, blockId = "block") {
  const block = document.getElementById(blockId);
  if (!block) throw new Error(`Missing element with id="${blockId}"`);

  block.textContent = "Loading…";

  try {
    const resp = await fetch(`${API}/item/${encodeURIComponent(key)}`);
    if (!resp.ok) {
      block.textContent = `Error ${resp.status}`;
      return;
    }

    const entry = await resp.json();
    block.innerHTML = renderEntry(key, entry);
  } catch (e) {
    block.textContent = `Network error: ${e}`;
  }
}

// One handler for ALL elements with data-key (nav + inline links + back-links)
document.addEventListener("click", (e) => {
  const el = e.target.closest("[data-key]");
  if (!el) return;

  e.preventDefault();
  const key = el.dataset.key;

  history.pushState({ key }, "", `?key=${encodeURIComponent(key)}`);

  renderKeyIntoBlockAnimated(key, "block");
});


window.addEventListener("popstate", (event) => {
  const key = event.state?.key;
  if (key) {
    renderKeyIntoBlockAnimated(key, "block");
  }
});


document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const key = params.get("key");

  if (key) {
    currentKey = key;
    renderKeyIntoBlock(key, "block");  // no animation on first load
    history.replaceState({ key }, "", window.location.href);
  }
});


function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function renderKeyIntoBlockAnimated(key, blockId = "block") {
  const block = document.getElementById(blockId);
  if (!block) throw new Error(`Missing element with id="${blockId}"`);

  // 🚫 Do nothing if same key
  if (key === currentKey) return;

  currentKey = key;

  // fade out
  block.classList.add("is-fading");
  await wait(90);

  // render new content
  await renderKeyIntoBlock(key, blockId);

  // fade in
  requestAnimationFrame(() => {
    block.classList.remove("is-fading");
  });
  //block.scrollIntoView({ behavior: "smooth", block: "start" });

}

