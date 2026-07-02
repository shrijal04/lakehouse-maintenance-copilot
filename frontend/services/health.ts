import { TableHealth } from "@/types/health";

const API = "http://127.0.0.1:8000";

// =====================================================
// Get Health for Any Iceberg Table
// =====================================================

export async function getHealth(
  database: string,
  target: string
): Promise<TableHealth> {
  const response = await fetch(
    `${API}/lakehouse/health?database=${database}&target=${target}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch table health.");
  }

  return response.json();
}