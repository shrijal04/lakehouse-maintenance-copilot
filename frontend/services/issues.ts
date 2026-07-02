const API =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export async function getIssues(
  database: string,
  target: string
) {
  const response = await fetch(
    `${API}/lakehouse/issues?database=${database}&target=${target}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch issues");
  }

  return response.json();
}