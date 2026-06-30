const API = "http://127.0.0.1:8000";

export async function getDashboardMetrics() {
  const response = await fetch(
    `${API}/lakehouse/dashboard`
  );

  if (!response.ok) {
    throw new Error("Failed to load dashboard.");
  }

  return response.json();
}