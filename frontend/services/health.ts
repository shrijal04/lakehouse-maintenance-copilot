import { TableHealth } from "@/types/health";

const API = "http://127.0.0.1:8000";

export async function getHealth(): Promise<TableHealth> {
  const response = await fetch(
    `${API}/lakehouse/orders/health`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch Orders health");
  }

  return response.json();
}

export async function getOrderItemsHealth(): Promise<TableHealth> {
  const response = await fetch(
    `${API}/lakehouse/order-items/health`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch Order Items health");
  }

  return response.json();
}