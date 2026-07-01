const API = "http://127.0.0.1:8000";

export interface IcebergTable {
  table_name: string;
  full_name: string;
  health: {
    table: string;
    snapshot_count: number;
    data_file_count: number;
    average_file_kb: number;
    total_size_mb: number;
    manifest_file_count: number;
    orphan_file_count: number;
  };
}

export async function getIcebergTables(): Promise<IcebergTable[]> {
  const response = await fetch(`${API}/lakehouse/tables`);

  if (!response.ok) {
    throw new Error("Failed to fetch Iceberg tables");
  }

  return response.json();
}