import React, { useCallback, useEffect, useMemo, useState } from "react";
import ResizableLayout from "./components/ResizableLayout";
import Sidebar from "./components/Sidebar";
import DocPane from "./components/DocPane";
import ImageGalleryPane from "./components/ImageGalleryPane";
import { getKeyFromUrl, setUrlForKey } from "./lib/history";
import { fetchLayout } from "./api/database";
import { useSystem } from "./context/SystemContext";

export default function App() {
  const system = useSystem();
  const urlKey = getKeyFromUrl();

  const fallbackKeys = useMemo(() => [
    ["Contents", "lecture-contents"],
  ], []);

  const [keys, setKeys] = useState(fallbackKeys);
  const [sidebarTitle, setSidebarTitle] = useState("Contents");
  const [startingSlide, setStartingSlide] = useState("lecture-contents");
  const [layout, setLayout] = useState(null);
  const [activeKey, setActiveKey] = useState(urlKey || null);

  const [imagesFromEntry, setImagesFromEntry] = useState([]);
  const [selectedImageName, setSelectedImageName] = useState(null);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const layoutData = await fetchLayout();
        setLayout(layoutData);
        const contents = layoutData.contents;
        
        if (contents) {
          // Set the sidebar title
          const title = contents.$keyword_name || "Contents";
          setSidebarTitle(title);
          
          // Set the starting slide
          const starting = layoutData.starting_slide || "lecture-contents";
          setStartingSlide(starting);
          
          // Extract the navigation keys (excluding $keyword_name)
          const loadedKeys = Object.entries(contents)
            .filter(([key]) => !key.startsWith('$'))
            .map(([key, value]) => {
              if (Array.isArray(value) && value.length >= 2) {
                return [String(value[0] || key), String(value[1] || key)];
              }
              return [String(key), String(key)];
            });

          if (!cancelled && loadedKeys.length > 0) {
            setKeys(loadedKeys);

            if (!urlKey) {
              setActiveKey(starting);
              setUrlForKey(starting, { replace: true });
            }
          } else if (!cancelled && urlKey) {
            setUrlForKey(urlKey, { replace: true });
          }
        }
      } catch (e) {
        console.error("Failed to fetch layout:", e);

        if (!cancelled) {
          const fallbackDefault = startingSlide || fallbackKeys[0]?.[1];
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
  }, [urlKey]); // Removed system dependency

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
      layout={layout}
      sidebar={<Sidebar keys={keys} title={sidebarTitle} onSelectKey={(k) => navigateKey(k, { push: true })} />}
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