const API = "http://127.0.0.1:8000";

// ======================================================
// Generate AI Report
// ======================================================

export async function generateReport() {
  const response = await fetch(
    `${API}/lakehouse/report`
  );

  if (!response.ok) {
    throw new Error("Failed to generate report.");
  }

  return response.json();
}