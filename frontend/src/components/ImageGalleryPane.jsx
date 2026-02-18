import React, { useEffect, useMemo, useRef, useState } from "react";
import ImagePane from "./ImagePane";

export default function ImageGalleryPane({
  images,
  selectedImageName = null,
  baseUrl = "http://localhost:8000/image",
  className = "",
}) {
  const list = useMemo(() => (Array.isArray(images) ? images : []), [images]);

  const itemRefs = useRef(new Map());
  const containerRef = useRef(null);

  const [flashName, setFlashName] = useState(null);
  const [containerWidth, setContainerWidth] = useState(600);

  // Observe container width for responsive height
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const ro = new ResizeObserver((entries) => {
      const w = entries?.[0]?.contentRect?.width;
      if (typeof w === "number" && w > 0) setContainerWidth(w);
    });

    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const imageHeight = Math.max(220, Math.min(620, Math.round(containerWidth * 0.6)));

  // Scroll to selected image
  useEffect(() => {
    if (!selectedImageName) return;

    const el = itemRefs.current.get(selectedImageName);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });

      setFlashName(selectedImageName);
      const t = window.setTimeout(() => setFlashName(null), 900);
      return () => window.clearTimeout(t);
    }
  }, [selectedImageName, list]);

  return (
    <div
      ref={containerRef}
      className={className}
      style={{
        height: "100%",
        overflow: "auto",
        padding: 8,
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      {/* <h2 style={{ margin: 0, padding: 8 }}>Images</h2> */}

      {list.length === 0 ? (
        <div style={{ opacity: 0.7 }}>No images in this entry.</div>
      ) : (
        list.map(([alt, name], idx) => {
          const safeName = String(name ?? "");
          const safeAlt = String(alt ?? "").trim();
          const label = safeAlt || safeName;

          const isSelected = selectedImageName === safeName;
          console.log("isSelected:", selectedImageName, safeName, isSelected);

          const isFlash = flashName === safeName;

          return (
            <div
              key={`${safeName}-${idx}`}
              ref={(node) => {
                if (!safeName) return;
                if (node) itemRefs.current.set(safeName, node);
                else itemRefs.current.delete(safeName);
              }}
              style={{
                border: isSelected
                  ? "2px solid rgba(0,0,0,0.8)"   // ✅ darker border when selected
                  : "1px solid rgba(0,0,0,0.15)",
                borderRadius: 10,
                padding: 10,
                boxShadow: isFlash
                  ? "0 0 0 3px rgba(0,0,0,0.18)"
                  : "none",
                transition: "border 150ms ease, box-shadow 200ms ease",
              }}
            >
              <div style={{ marginBottom: 8, fontWeight: 600, opacity: 0.9 }}>
                {label}
              </div>

              <div style={{ width: "100%", height: imageHeight }}>
                <ImagePane imageName={safeName} alt={label} baseUrl={baseUrl} />
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}
