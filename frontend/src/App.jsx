import React, { useCallback, useEffect, useMemo, useState } from "react";
import ResizableLayout from "./components/ResizableLayout";
import Sidebar from "./components/Sidebar";
import DocPane from "./components/DocPane";
import ImageGalleryPane from "./components/ImageGalleryPane";
import { getKeyFromUrl, setUrlForKey } from "./lib/history";
import { fetchEntry } from "./api/database";
import { useSystem } from "./context/SystemContext";
import { parsePayload } from "./lib/linkPayload";

function normalizeContentsToKeys(data, system) {
  if (!data || typeof data !== "object" || Array.isArray(data)) return [];

  const linkSeparator = system?.link_separator;
  const itemSeparator = system?.item_separator;
  if (!linkSeparator || !itemSeparator) return [];

  return Object.entries(data)
    .map(([key, value]) => {
      if (String(key).startsWith("$")) return null;
      if (!Array.isArray(value) || value.length < 2) return null;

      const label = String(value[0] ?? "").trim();
      const linkInfo = String(value[1] ?? "");

      const parsed = parsePayload(linkInfo, { linkSeparator, itemSeparator });
      if (!parsed) return null;

      return [label || parsed.name || key, parsed.value];
    })
    .filter(Boolean);
}

export default function App() {
  const system = useSystem();
  const urlKey = getKeyFromUrl();

  const fallbackKeys = useMemo(() => [
    ["Contents", "lecture-contents"],
  ], []);

  const contentsItemName =
    import.meta.env.VITE_CONTENTS_ITEM ||
    new URLSearchParams(window.location.search).get("lecture-contents") ||
    "lecture-contents";

  const [keys, setKeys] = useState(fallbackKeys);
  const [activeKey, setActiveKey] = useState(urlKey || null);

  const [imagesFromEntry, setImagesFromEntry] = useState([]);
  const [selectedImageName, setSelectedImageName] = useState(null);

  useEffect(() => {
    let cancelled = false;

    if (!system) return;

    (async () => {
      try {
        const data = await fetchEntry("item", contentsItemName);
        const loadedKeys = normalizeContentsToKeys(data, system);

        if (!cancelled && loadedKeys.length > 0) {
          setKeys(loadedKeys);

          if (!urlKey) {
            const firstKey = loadedKeys[0][1];
            setActiveKey(firstKey);
            setUrlForKey(firstKey, { replace: true });
          }
        } else if (!cancelled && urlKey) {
          setUrlForKey(urlKey, { replace: true });
        }
      } catch (e) {
        console.error("Failed to fetch contents keys:", e);

        if (!cancelled) {
          const fallbackDefault = fallbackKeys[0]?.[1];
          if (!activeKey && fallbackDefault) {
            setActiveKey(fallbackDefault);
            setUrlForKey(fallbackDefault, { replace: true });
          }
        }
      }
    })();

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contentsItemName, system]);

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

  const safeActiveKey = activeKey || fallbackKeys?.[0]?.[1];

  return (
    <ResizableLayout
      sidebar={<Sidebar keys={keys} onSelectKey={(k) => navigateKey(k, { push: true })} />}
      left={<DocPane
        initialKey={safeActiveKey}
        onNavigateKey={(k) => navigateKey(k, { push: true })}
        onImagesChange={setImagesFromEntry}
        onSelectImage={setSelectedImageName}
      />}
      right={<ImageGalleryPane
        images={imagesFromEntry}
        selectedImageName={selectedImageName}
      />}
    />
  );
}