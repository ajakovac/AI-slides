import React, { useCallback, useMemo, useRef, useState } from 'react';

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

export default function App() {
  const containerRef = useRef(null);
  const [headerHeight, setHeaderHeight] = useState(120);
  const [sidebarWidth, setSidebarWidth] = useState(280);
  const [mainSplit, setMainSplit] = useState(0.5);

  const minHeader = 60;
  const minBodyHeight = 180;
  const minSidebar = 220;
  const minMainPane = 240;

  const startDrag = useCallback((onMove, onEnd) => (event) => {
    event.preventDefault();
    const handleMove = (moveEvent) => onMove(moveEvent);
    const handleUp = () => {
      window.removeEventListener('pointermove', handleMove);
      window.removeEventListener('pointerup', handleUp);
      onEnd?.();
    };
    window.addEventListener('pointermove', handleMove);
    window.addEventListener('pointerup', handleUp);
  }, []);

  const onHeaderDrag = useMemo(() =>
    startDrag((event) => {
      const rect = containerRef.current?.getBoundingClientRect();
      if (!rect) return;
      const maxHeader = rect.height - minBodyHeight;
      const next = clamp(event.clientY - rect.top, minHeader, maxHeader);
      setHeaderHeight(next);
    }),
    [startDrag]
  );

  const onSidebarDrag = useMemo(() =>
    startDrag((event) => {
      const rect = containerRef.current?.getBoundingClientRect();
      if (!rect) return;
      const maxSidebar = rect.width - minMainPane * 2;
      const next = clamp(event.clientX - rect.left, minSidebar, maxSidebar);
      setSidebarWidth(next);
    }),
    [startDrag]
  );

  const onMainSplitDrag = useMemo(() =>
    startDrag((event) => {
      const mainRect = containerRef.current?.querySelector('.main-area')?.getBoundingClientRect();
      if (!mainRect) return;
      const usableWidth = mainRect.width;
      const raw = (event.clientX - mainRect.left) / usableWidth;
      const minFrac = minMainPane / usableWidth;
      const maxFrac = 1 - minMainPane / usableWidth;
      setMainSplit(clamp(raw, minFrac, maxFrac));
    }),
    [startDrag]
  );

  return (
    <div ref={containerRef} className="app">
      <header className="header" style={{ height: headerHeight }}>
        <div className="header-content">
          <div className="brand">AI Slides</div>
          <div className="meta">Resizable layout demo</div>
        </div>
      </header>
      <div className="splitter horizontal" onPointerDown={onHeaderDrag} />

      <div className="body" style={{ height: `calc(100% - ${headerHeight + 6}px)` }}>
        <aside className="sidebar" style={{ width: sidebarWidth }}>
          <h2>Sidebar</h2>
          <p>Left aligned, resizable.</p>
        </aside>
        <div className="splitter vertical" onPointerDown={onSidebarDrag} />
        <div className="main-area" style={{ width: `calc(100% - ${sidebarWidth + 6}px)` }}>
          <section className="pane left" style={{ width: `${mainSplit * 100}%` }}>
            <h2>Left pane</h2>
            <p>Put your primary content here.</p>
          </section>
          <div className="splitter vertical" onPointerDown={onMainSplitDrag} />
          <section className="pane right" style={{ width: `${(1 - mainSplit) * 100}%` }}>
            <h2>Right pane</h2>
            <p>Secondary content or tools.</p>
          </section>
        </div>
      </div>
    </div>
  );
}
