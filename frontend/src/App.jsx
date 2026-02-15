import React, { useCallback, useEffect, useMemo, useState } from "react";
import ResizableLayout from "./components/ResizableLayout";
import Sidebar from "./components/Sidebar";
import DocPane from "./components/DocPane";
import { getKeyFromUrl, setUrlForKey } from "./lib/history";

import "./styles/app.css";
import "./styles/doc.css";

export default function App() {
  const defaultKey = "learning-in-the-ai-era";
  const [activeKey, setActiveKey] = useState(getKeyFromUrl() || defaultKey);

  const keys = useMemo(() => [
    "learning-in-the-ai-era",
    "transformers",
    "reinforcement-learning"
  ], []);

  // initial: ensure url matches
  useEffect(() => {
    setUrlForKey(activeKey, { replace: true });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // back/forward
  useEffect(() => {
    const onPop = (event) => {
      const key = event.state?.key || getKeyFromUrl();
      if (key) setActiveKey(key);
    };
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);

  const navigateKey = useCallback((key, { push = true } = {}) => {
    setActiveKey(key);
    if (push) setUrlForKey(key, { replace: false });
    else setUrlForKey(key, { replace: true });
  }, []);

  return (
    <ResizableLayout
      sidebar={<Sidebar keys={keys} onSelectKey={(k) => navigateKey(k, { push: true })} />}
      left={<DocPane initialKey={activeKey} onNavigateKey={(k) => navigateKey(k, { push: true })} />}
      right={
        <div style={{ padding: 12 }}>
          <h2>Tools</h2>
          <p>Put search, tags, or editing tools here.</p>
        </div>
      }
    />
  );
}
