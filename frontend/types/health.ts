export interface HealthScore {
  score: number;
  status: "Healthy" | "Warning" | "Critical";
}

export type HealthColor =
  | "green"
  | "yellow"
  | "red"
  | "cyan";

export interface HealthMetric {
  id: number;
  title: string;
  value: number;
  description: string;
  color: HealthColor;
}

export interface HealthTrendPoint {
  day: string;
  score: number;
}

export interface StorageUsage {
  used: number;
  available: number;
  total: number;
}

export interface MetadataHealth {
  snapshots: number;
  manifestFiles: number;
  orphanFiles: number;
}

export interface Recommendation {
  id: number;
  title: string;
  priority: "Low" | "Medium" | "High";
}

export interface Issue {
  id: number;
  table: string;
  severity: "Healthy" | "Warning" | "Critical";
  issue: string;
  action: string;
}

export interface ResourceUsage {
  cpu: number;
  memory: number;
  disk: number;
}

export interface MaintenanceHistory {
  id: number;
  job: string;
  status: "Completed" | "Running" | "Failed";
  time: string;
}

export interface TableHealth {
  table: string;

  snapshot_count: number;
  data_file_count: number;

  average_file_kb: number;
  total_size_mb: number;

  manifest_file_count: number;
  orphan_file_count: number;
}