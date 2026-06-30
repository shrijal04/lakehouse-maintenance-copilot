import {HealthHistory} from "@/types/history"

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export async function getHealthHistory(): Promise<HealthHistory[]> {
  const response = await fetch(
    `${API}/lakehouse/orders/history`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch history");
  }

  return response.json();
}