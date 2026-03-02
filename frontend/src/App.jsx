import React, { useCallback, useEffect, useMemo, useState } from "react";
import ResizableLayout from "./components/ResizableLayout";
import Sidebar from "./components/Sidebar";
import DocPane from "./components/DocPane";
import ImageGalleryPane from "./components/ImageGalleryPane";
import { getKeyFromUrl, setUrlForKey } from "./lib/history";
import { fetchEntry } from "./api/database";

function normalizeContentsToKeys(data) {
  // Expected: { "Lecture 1": ["link-to-lecture-1"], ... }
  // Return:   [ ["Lecture 1","link-to-lecture-1"], ... ]
  if (!data || typeof data !== "object" || Array.isArray(data)) return [];

  return Object.entries(data)
    .map(([label, value]) => {
      const v =
        Array.isArray(value) ? value[0] :
        typeof value === "string" ? value :
        "";
      return [String(v), String(label) ];
    })
    .filter(([key, label]) =>
      label &&
      key &&
      !label.startsWith("$")   // 👈 ignore system / hidden entries
    );
}

export default function App() {
  const urlKey = getKeyFromUrl();

  // Fallback keys (your current hard-coded list)
  const fallbackKeys = useMemo(() => [
    ["Contents", "lecture-contents"],
  ], []);

  // Which item to fetch from `/item/<name>`
  // default: "contents"
  const contentsItemName =
    import.meta.env.VITE_CONTENTS_ITEM ||
    new URLSearchParams(window.location.search).get("lecture-contents") ||
    "lecture-contents";

  const [keys, setKeys] = useState(fallbackKeys);
  const [activeKey, setActiveKey] = useState(urlKey || null);

  const [imagesFromEntry, setImagesFromEntry] = useState([]);
  const [selectedImageName, setSelectedImageName] = useState(null);

  // Fetch keys on mount (and whenever contentsItemName changes)
  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const data = await fetchEntry("item", contentsItemName);
        const loadedKeys = normalizeContentsToKeys(data);

        if (!cancelled && loadedKeys.length > 0) {
          setKeys(loadedKeys);

          // choose default if no URL key was provided
          if (!urlKey) {
            const firstKey = loadedKeys[0][1];
            setActiveKey(firstKey);
            setUrlForKey(firstKey, { replace: true });
          }
        } else if (!cancelled && urlKey) {
          // ensure URL is reflected (even if keys empty)
          setUrlForKey(urlKey, { replace: true });
        }
      } catch (e) {
        console.error("Failed to fetch contents keys:", e);
        // fallback stays in place
        if (!cancelled) {
          const fallbackDefault = fallbackKeys[0]?.[1];
          if (!activeKey && fallbackDefault) {
            setActiveKey(fallbackDefault);
            setUrlForKey(fallbackDefault, { replace: true });
          }
        }
      }
    })();

    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contentsItemName]);

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

  // If activeKey is still null for some reason, avoid rendering DocPane with null
  // const safeActiveKey = activeKey || keys?.[0]?.[1] || fallbackKeys?.[0]?.[1];
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