const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function fetchDetections() {
  const res = await fetch(`${API_BASE_URL}/detections/`);
  if (!res.ok) throw new Error("Failed to fetch detections");
  return res.json();
}

export async function fetchDetectionById(detectionId: string) {
  const res = await fetch(`${API_BASE_URL}/detections/${detectionId}`);
  if (!res.ok) throw new Error(`Failed to fetch detection for id: ${detectionId}`);
  return res.json();
}
