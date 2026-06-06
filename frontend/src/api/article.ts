const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function fetchArticles() {
  const res = await fetch(`${API_BASE_URL}/articles/`);
  if (!res.ok) throw new Error("Failed to fetch articles");
  return res.json();
}

export async function fetchArticleById(articleId: string) {
  const res = await fetch(`${API_BASE_URL}/articles/${articleId}`);
  if (!res.ok) throw new Error(`Failed to fetch article for id: ${articleId}`);
  return res.json();
}

export async function fetchArticlesByEvent(eventId: string) {
  const url = new URL(`${API_BASE_URL}/articles`);
  url.searchParams.set("event_id", eventId);

  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch articles for event: ${eventId}`);
  return res.json();
}
