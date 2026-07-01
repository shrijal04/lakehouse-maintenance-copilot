const API = "http://127.0.0.1:8000";

export async function runIncrementalLoad() {
  const response = await fetch(`${API}/etl/run`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to run incremental load.");
  }

  return response.json();
}

export async function simulateBusinessDay() {
  const response = await fetch(`${API}/etl/simulate`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to simulate business day.");
  }

  return response.json();
}

export async function getEtlHistory() {
  const response = await fetch(`${API}/etl/history`);

  if (!response.ok) {
    throw new Error("Failed to load ETL history.");
  }

  return response.json();
}