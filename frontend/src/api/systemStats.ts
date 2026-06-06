const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function fetchSystemStats() {
  const res = await fetch(`${API_BASE_URL}/article/stats`);
  if (!res.ok) throw new Error(`Failed to fetch system stats`);
  return res.json();
}