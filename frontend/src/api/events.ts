const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function fetchEvents() {
  const res = await fetch(`${API_BASE_URL}/events/`);
  if (!res.ok) throw new Error("Failed to fetch events");
  return res.json();
}

export async function fetchEventById(eventId: string) {
    const res = await fetch(`${API_BASE_URL}/events/${eventId}`);
    if (!res.ok) throw new Error(`Failed to fetch event for eventId:${eventId}`);
    return res.json();
}
