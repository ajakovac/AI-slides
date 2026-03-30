export const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function apiFetch(path) {
  const resp = await fetch(`${BASE_URL}${path}`); // no credentials

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`HTTP ${resp.status}: ${text}`);
  }

  return resp.json();
}