const API = "http://localhost:8000";

export async function getIssues() {
  const response = await fetch(`${API}/lakehouse/orders/issues`);

  if (!response.ok) {
    throw new Error("Failed to fetch issues");
  }

  return response.json();
}

export async function getOrderItemsIssues() {
  const response = await fetch(
    `${API}/lakehouse/order-items/issues`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch order item issues");
  }

  return response.json();
}