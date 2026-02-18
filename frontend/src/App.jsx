import React, { useCallback, useEffect, useMemo, useState } from "react";
import ResizableLayout from "./components/ResizableLayout";
import Sidebar from "./components/Sidebar";
import DocPane from "./components/DocPane";
import ImageGalleryPane from "./components/ImageGalleryPane";
import { getKeyFromUrl, setUrlForKey } from "./lib/history";


export default function App() {
  const defaultKey = "content-of-the-ai-course";
  const [activeKey, setActiveKey] = useState(getKeyFromUrl() || defaultKey);
  const [imagesFromEntry, setImagesFromEntry] = useState([]);
  const [selectedImageName, setSelectedImageName] = useState(null);

  const keys = useMemo(() => [
    ["Contents", "content-of-the-ai-course"],
    ["About the course", "about-the-introduction-to-ai-course"],
    ["Learning in the AI era", "learning-in-the-ai-era"],
    ["Introduction","general-facts-about-ai"],
    ["Social aspects","social-and-ethical-aspects-of-artificial-intelligence"],
    ["History","a-brief-history-of-artificial-intelligence"]
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
      left={<DocPane
        initialKey={activeKey}
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
