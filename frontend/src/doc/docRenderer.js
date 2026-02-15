// docRenderer.js

export function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export function makeHtmlLink(line, { linkSeparator, itemSeparator }) {
  const parts = String(line).split(linkSeparator);
  if (parts.length % 2 === 0) {
    throw new Error(`Unmatched linkSeparator in line: ${line}`);
  }

  const out = [];
  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];

    // even indices: normal text
    if (i % 2 === 0) {
      out.push(escapeHtml(part));
      continue;
    }

    // odd indices: link payload "TEXT<itemSep>KEY"
    const [text, key, ...rest] = part.split(itemSeparator);
    if (rest.length > 0 || text == null || key == null) {
      throw new Error(`Invalid link payload: ${part}`);
    }

    out.push(
      `<a class="inline-link" href="#" data-key="${escapeHtml(key.trim())}">` +
        `${escapeHtml(text.trim())}` +
      `</a>`
    );
  }

  return out.join("");
}

export function renderEntry(key, entry, system) {
  const linkSeparator = system?.link_separator;
  const itemSeparator = system?.item_separator;

  if (!linkSeparator || !itemSeparator) {
    throw new Error("renderEntry: system config missing link_separator or item_separator");
  }

  const section = [];
  section.push(`<section class="card" data-entry-key="${escapeHtml(key)}">`);
  section.push(`<h2>${escapeHtml(entry?.["$keyword_name"] ?? key)}</h2>`);

  for (const [property, propertyList] of Object.entries(entry ?? {})) {
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
      section.push(`<li>${makeHtmlLink(line, { linkSeparator, itemSeparator })}</li>`);
    }
    section.push(`</ul>`);
    section.push(`</div>`);
  }

  const links = entry?.["$links"];
  if (Array.isArray(links) && links.length > 0) {
    section.push(`<div class="references">`);
    section.push(`<h3>Referenced by</h3>`);
    section.push(`<ul>`);
    for (const link of links) {
      if (!Array.isArray(link) || link.length < 2) continue;
      const [name, linkname, via] = link;

      section.push(
        `<li>` +
          `<a class="back-link" href="#" data-key="${escapeHtml(linkname)}">` +
            `${escapeHtml(name ?? linkname)}` +
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
