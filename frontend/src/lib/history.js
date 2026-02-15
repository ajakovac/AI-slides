export function getKeyFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("key");
}

export function setUrlForKey(key, { replace = false } = {}) {
  const url = `?key=${encodeURIComponent(key)}`;
  const state = { key };
  if (replace) window.history.replaceState(state, "", url);
  else window.history.pushState(state, "", url);
}
