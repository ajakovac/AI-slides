import React, { useEffect, useMemo, useState } from "react";

/**
 * Fetches an image from `GET {baseUrl}/{imageName}` and renders it.
 * - Uses blob + objectURL so it works even if the server doesn't set perfect caching headers.
 * - Aborts fetch on unmount / change.
 * - Revokes object URLs to avoid memory leaks.
 */
export default function ImagePane({
  imageName,
  alt = "",
  baseUrl = "http://localhost:8000/image",
  className = "",
}) {
  const [src, setSrc] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | ready | error
  const [error, setError] = useState("");

  const url = useMemo(() => {
    if (!imageName) return null;
    // IMPORTANT: encode imageName in case it has spaces, #, ?, etc.
    return `${baseUrl}/${encodeURIComponent(imageName)}`;
  }, [baseUrl, imageName]);

  useEffect(() => {
    let objectUrl = null;
    const ac = new AbortController();

    async function run() {
      if (!url) {
        setSrc(null);
        setStatus("idle");
        setError("");
        return;
      }

      setStatus("loading");
      setError("");
      setSrc(null);

      try {
        const res = await fetch(url, {
          method: "GET",
          signal: ac.signal,
          // credentials: "include", // enable if your backend needs cookies
        });

        if (!res.ok) {
          throw new Error(`Image fetch failed: ${res.status} ${res.statusText}`);
        }

        const blob = await res.blob();
        objectUrl = URL.createObjectURL(blob);
        setSrc(objectUrl);
        setStatus("ready");
      } catch (e) {
        if (ac.signal.aborted) return;
        setStatus("error");
        setError(e?.message ?? String(e));
      }
    }

    run();

    return () => {
      ac.abort();
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [url]);

  if (!imageName) {
    return (
      <div className={`image-pane ${className}`} style={{ padding: 12, opacity: 0.7 }}>
        No image selected.
      </div>
    );
  }

  if (status === "loading") {
    return (
      <div className={`image-pane ${className}`} style={{ padding: 12 }}>
        Loading <code>{imageName}</code>…
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className={`image-pane ${className}`} style={{ padding: 12 }}>
        <div style={{ fontWeight: 600, marginBottom: 8 }}>Could not load image</div>
        <div style={{ marginBottom: 8 }}>
          <code>{imageName}</code>
        </div>
        <div style={{ whiteSpace: "pre-wrap", opacity: 0.85 }}>{error}</div>
      </div>
    );
  }

  return (
    <div className={`image-pane ${className}`} style={{ padding: 8, height: "100%" }}>
      <img
        src={src}
        alt={alt || imageName}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "contain",
          display: "block",
          borderRadius: 8,
        }}
      />
    </div>
  );
}
