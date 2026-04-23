import React, { useCallback, useEffect, useMemo, useState } from "react";
import ResizableLayout from "./components/ResizableLayout";
import Sidebar from "./components/Sidebar";
import DocPane from "./components/DocPane";
import ImageGalleryPane from "./components/ImageGalleryPane";
import GlobalMenu from "./components/GlobalMenu";
import { getKeyFromUrl, setUrlForKey } from "./lib/history";
import { fetchLayout } from "./api/database";

const THEME_STYLE_SLOTS = ["layout", "app", "doc"];
const THEME_STORAGE_KEY = "frontend-theme";
const DEFAULT_THEME = "pastel";

const themeStyleModules = import.meta.glob("./styles/*/*.css", {
  eager: true,
  query: "?url",
  import: "default",
});

const THEME_STYLES = Object.entries(themeStyleModules).reduce((acc, [path, url]) => {
  const match = path.match(/\.\/styles\/([^/]+)\/([^/]+)\.css$/);
  if (!match) return acc;

  const [, themeName, slotName] = match;
  if (!THEME_STYLE_SLOTS.includes(slotName)) return acc;

  if (!acc[themeName]) {
    acc[themeName] = {};
  }

  acc[themeName][slotName] = url;
  return acc;
}, {});

function toThemeLabel(themeName) {
  return String(themeName)
    .replace(/[-_]+/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function getAvailableThemes() {
  const folderThemes = Object.keys(THEME_STYLES).filter((themeName) =>
    THEME_STYLE_SLOTS.every((slotName) => THEME_STYLES[themeName]?.[slotName])
  );

  if (folderThemes.length > 0) {
    return folderThemes;
  }

  if (THEME_STYLES[DEFAULT_THEME]) {
    return [DEFAULT_THEME];
  }

  return [];
}

function normalizeTheme(theme, availableThemes) {
  const safeThemes = Array.isArray(availableThemes) ? availableThemes : [];
  return safeThemes.includes(theme) ? theme : safeThemes[0] || DEFAULT_THEME;
}

export default function App() {
  const urlKey = getKeyFromUrl();

  const fallbackKeys = useMemo(() => [["Contents", "lecture-contents"]], []);
  const availableThemes = useMemo(() => getAvailableThemes(), []);
  const themeOptions = useMemo(
    () =>
      availableThemes.map((themeName) => ({
        value: themeName,
        label: toThemeLabel(themeName),
      })),
    [availableThemes]
  );

  const [keys, setKeys] = useState(fallbackKeys);
  const [sidebarTitle, setSidebarTitle] = useState("Contents");
  const [startingSlide, setStartingSlide] = useState("lecture-contents");
  const [layout, setLayout] = useState(null);
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_STORAGE_KEY) || DEFAULT_THEME);
  const [activeKey, setActiveKey] = useState(urlKey || null);

  const [imagesFromEntry, setImagesFromEntry] = useState([]);
  const [selectedImageName, setSelectedImageName] = useState(null);

  useEffect(() => {
    setTheme((currentTheme) => normalizeTheme(currentTheme, availableThemes));
  }, [availableThemes]);

  useEffect(() => {
    const activeTheme = normalizeTheme(theme, availableThemes);
    const styleUrls = THEME_STYLE_SLOTS.map((slotName) => THEME_STYLES[activeTheme]?.[slotName]);

    document.documentElement.setAttribute("data-theme", activeTheme);
    localStorage.setItem(THEME_STORAGE_KEY, activeTheme);

    const createdLinks = [];

    THEME_STYLE_SLOTS.forEach((slot, index) => {
      const selector = `link[data-theme-style="${slot}"]`;
      let link = document.head.querySelector(selector);

      if (!link) {
        link = document.createElement("link");
        link.rel = "stylesheet";
        link.dataset.themeStyle = slot;
        document.head.appendChild(link);
        createdLinks.push(link);
      }

      if (styleUrls[index]) {
        link.href = styleUrls[index];
      }
    });

    return () => {
      createdLinks.forEach((link) => {
        if (link.parentNode) {
          link.parentNode.removeChild(link);
        }
      });
    };
  }, [theme, availableThemes]);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      try {
        const layoutData = await fetchLayout();
        setLayout(layoutData);
        const contents = layoutData.contents;

        if (contents) {
          const title = contents.$keyword_name || "Contents";
          setSidebarTitle(title);

          const starting = layoutData.starting_slide || "lecture-contents";
          setStartingSlide(starting);

          const loadedKeys = Object.entries(contents)
            .filter(([key]) => !key.startsWith("$"))
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
  }, [urlKey]);

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
    <>
      <GlobalMenu
        theme={theme}
        onThemeChange={(nextTheme) => setTheme(normalizeTheme(nextTheme, availableThemes))}
        themeOptions={themeOptions}
      />
      <ResizableLayout
        layout={layout}
        theme={theme}
        onThemeChange={(nextTheme) => setTheme(normalizeTheme(nextTheme, availableThemes))}
        sidebar={<Sidebar keys={keys} title={sidebarTitle} onSelectKey={(k) => navigateKey(k, { push: true })} />}
        left={
          <DocPane
            initialKey={safeActiveKey}
            onNavigateKey={(k) => navigateKey(k, { push: true })}
            onImagesChange={setImagesFromEntry}
            onSelectImage={setSelectedImageName}
          />
        }
        right={<ImageGalleryPane images={imagesFromEntry} selectedImageName={selectedImageName} />}
      />
    </>
  );
}
