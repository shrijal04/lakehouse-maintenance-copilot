const API = "http://localhost:8000";

export async function getIssues() {
  const response = await fetch(`${API}/lakehouse/orders/issues`);

  if (!response.ok) {
    throw new Error("Failed to fetch issues");
  }

  return response.json();
}