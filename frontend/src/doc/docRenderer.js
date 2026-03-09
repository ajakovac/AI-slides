// docRenderer.js
import { buildPayloadRegex } from "../lib/linkPayload";

export function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export function makeHtmlLink(line, { linkSeparator, itemSeparator }) {
  const s = String(line);
  const LINK_RE = buildPayloadRegex(linkSeparator, itemSeparator, { global: true });

  return s.replace(LINK_RE, (full, typeRaw, nameRaw, valueRaw) => {
    const type = String(typeRaw ?? "").trim();
    const name = String(nameRaw ?? "").trim();
    const value = String(valueRaw ?? "").trim();

    if (!type || !name || !value) {
      throw new Error(`Invalid link payload: ${full}`);
    }

    if (type === "keyword") {
      return (
        `<a class="inline-link" href="#" data-key="${escapeHtml(value)}">` +
          `${escapeHtml(name)}` +
        `</a>`
      );
    }

    if (type === "image") {
      return (
        `<a class="inline-image" href="#" data-image="${escapeHtml(value)}" data-alt="${escapeHtml(name)}">` +
          `${escapeHtml(name)}` +
        `</a>`
      );
    }

    if (type === "external-link") {
      return (
        `<a class="external-link" href="${escapeHtml(value)}" target="_blank" rel="noopener noreferrer">` +
          `${escapeHtml(name)}` +
        `</a>`
      );
    }

    throw new Error(`Unknown link type: ${type}`);
  });
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
    if (property === ">remark") {
      const remark = (propertyList || []).slice(1).map(escapeHtml).join(", ");
      if (remark) section.push(`<blockquote>${remark}</blockquote>`);
      continue;
    }

    if (property.startsWith("$")) continue;

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
