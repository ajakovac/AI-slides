import React, { useCallback, useMemo, useRef, useState } from "react";
import { clamp, startDrag } from "../lib/drag";
import { BASE_URL } from "../api/client";

export default function ResizableLayout({ layout, theme, onThemeChange, sidebar, left, right }) {
  const containerRef = useRef(null);
  const [headerHeight, setHeaderHeight] = useState(120);
  const [sidebarWidth, setSidebarWidth] = useState(200);
  const [mainSplit, setMainSplit] = useState(0.7);

  const minHeader = 60;
  const minBodyHeight = 180;
  const minSidebar = 120;
  const minMainPane = 240;

  const onHeaderDrag = useMemo(
    () =>
      startDrag((event) => {
        const rect = containerRef.current?.getBoundingClientRect();
        if (!rect) return;
        const maxHeader = rect.height - minBodyHeight;
        const next = clamp(event.clientY - rect.top, minHeader, maxHeader);
        setHeaderHeight(next);
      }),
    []
  );

  const onSidebarDrag = useMemo(
    () =>
      startDrag((event) => {
        const rect = containerRef.current?.getBoundingClientRect();
        if (!rect) return;
        const maxSidebar = rect.width - minMainPane * 2;
        const next = clamp(event.clientX - rect.left, minSidebar, maxSidebar);
        setSidebarWidth(next);
      }),
    []
  );

  const onMainSplitDrag = useMemo(
    () =>
      startDrag((event) => {
        const mainRect = containerRef.current
          ?.querySelector(".main-area")
          ?.getBoundingClientRect();
        if (!mainRect) return;
        const usableWidth = mainRect.width;
        const raw = (event.clientX - mainRect.left) / usableWidth;
        const minFrac = minMainPane / usableWidth;
        const maxFrac = 1 - minMainPane / usableWidth;
        setMainSplit(clamp(raw, minFrac, maxFrac));
      }),
    []
  );

  return (
    <div ref={containerRef} className="app">
      <header className="header" style={{ height: headerHeight }}>
        <div className="header-content">
          {layout?.logo && <img src={`${BASE_URL}${layout.logo}`} alt="Logo" className="logo" />}
          <div className="title-section">
            {layout?.title && <div className="title">{layout.title}</div>}
            {layout?.subtitle && <div className="subtitle">{layout.subtitle}</div>}
          </div>
          <div className="meta-section">
            {layout?.author && <div className="author">{layout.author}</div>}
            {layout?.date && <div className="date">{layout.date}</div>}
          </div>
        </div>
      </header>

      <div className="splitter horizontal" onPointerDown={onHeaderDrag} />

      <div className="body" style={{ height: `calc(100% - ${headerHeight + 6}px)` }}>
        <aside className="sidebar" style={{ width: sidebarWidth }}>
          {sidebar}
        </aside>

        <div className="splitter vertical" onPointerDown={onSidebarDrag} />

        <div className="main-area" style={{ width: `calc(100% - ${sidebarWidth + 6}px)` }}>
          <section className="pane left" style={{ width: `${mainSplit * 100}%` }}>
            {left}
          </section>

          <div className="splitter vertical" onPointerDown={onMainSplitDrag} />

          <section className="pane right" style={{ width: `${(1 - mainSplit) * 100}%` }}>
            {right}
          </section>
        </div>
      </div>
    </div>
  );
}
