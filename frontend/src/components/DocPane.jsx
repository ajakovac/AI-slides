import React, { useCallback, useEffect, useRef, useState } from "react";
import "katex/dist/katex.min.css";
import renderMathInElement from "katex/contrib/auto-render";

import { useSystem } from "../context/SystemContext";
import { fetchEntry } from "../api/database";
import { renderEntry, escapeHtml } from "../doc/docRenderer";

export default function DocPane({ initialKey, onNavigateKey }) {
  const [key, setKey] = useState(initialKey);
  const [html, setHtml] = useState("<div>Loading…</div>");
  const [isFading, setIsFading] = useState(false);

  const paneRef = useRef(null);
  const system = useSystem();

  // Track first load to avoid animating initial render
  const didInitRef = useRef(false);

  const loadKey = useCallback(
    async (nextKey, { animate = true } = {}) => {
      if (!system) return;
      if (!nextKey) return;

      setKey(nextKey);

      if (animate) {
        setIsFading(true);
        await new Promise((r) => setTimeout(r, 160));
      }

      try {
        const entry = await fetchEntry("item", nextKey);
        setHtml(renderEntry(nextKey, entry, system));
      } catch (e) {
        setHtml(`<div class="error">Error: ${escapeHtml(String(e))}</div>`);
      } finally {
        if (animate) requestAnimationFrame(() => setIsFading(false));
      }
    },
    [system]
  );

  // Load whenever parent changes the key (clicks OR back/forward)
  useEffect(() => {
    if (!system) return;

    const animate = didInitRef.current; // false on first load, true afterwards
    didInitRef.current = true;

    loadKey(initialKey, { animate });
  }, [initialKey, loadKey, system]);

  // Click delegation: tell parent to navigate (parent pushes history + updates activeKey)
  const onClick = useCallback(
    (e) => {
      const a = e.target.closest("[data-key]");
      if (!a) return;
      e.preventDefault();
      onNavigateKey?.(a.dataset.key);
    },
    [onNavigateKey]
  );

  // KaTeX render after HTML changes
  useEffect(() => {
    const el = paneRef.current;
    if (!el) return;

    renderMathInElement(el, {
      delimiters: [
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true },
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
      ],
      throwOnError: false,
      strict: "ignore",
    });
  }, [html]);

  if (!system) return <div className="doc-pane">Loading system…</div>;

  return (
    <div
      ref={paneRef}
      className={`doc-pane ${isFading ? "is-fading" : ""}`}
      onClick={onClick}
      data-current-key={key}
    >
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}
