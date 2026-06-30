const API = "http://127.0.0.1:8000";

export async function requestMaintenance() {
  const response = await fetch(
    `${API}/lakehouse/orders/maintenance/request`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to request maintenance.");
  }

  return response.json();
}

export async function confirmMaintenance(
  confirmationId: string,
  confirm: boolean
) {
  const response = await fetch(
    `${API}/lakehouse/orders/maintenance/confirm`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        confirmation_id: confirmationId,
        confirm,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Maintenance failed.");
  }

  return response.json();
}