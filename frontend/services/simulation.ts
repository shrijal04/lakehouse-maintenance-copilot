const API = "http://localhost:8000";

export async function runSimulation() {
  const response = await fetch(`${API}/simulation/start`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Simulation failed");
  }

  return response.json();
}