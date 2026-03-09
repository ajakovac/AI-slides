// src/lib/linkPayload.js

export function escapeRegex(str) {
  return String(str).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function buildPayloadRegex(linkSeparator, itemSeparator, { global = false, anchored = false } = {}) {
  const ls = escapeRegex(linkSeparator);
  const is = escapeRegex(itemSeparator);

  const body = `${ls}(.*?)${is}(.*?)${is}(.*?)${ls}`;
  const pattern = anchored ? `^${body}$` : body;
  const flags = global ? "g" : "";

  return new RegExp(pattern, flags);
}

export function parsePayload(payload, { linkSeparator, itemSeparator }) {
  const re = buildPayloadRegex(linkSeparator, itemSeparator, { anchored: true });
  const match = String(payload ?? "").match(re);

  if (!match) return null;

  return {
    type: String(match[1] ?? "").trim(),
    name: String(match[2] ?? "").trim(),
    value: String(match[3] ?? "").trim(),
  };
}