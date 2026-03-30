import { apiFetch } from "./client";

export function fetchEntry(section, key) {
  return apiFetch(
    `/${encodeURIComponent(section)}/${encodeURIComponent(key)}`
  );
}

export function fetchLayout() {
  return apiFetch("/layout");
}
