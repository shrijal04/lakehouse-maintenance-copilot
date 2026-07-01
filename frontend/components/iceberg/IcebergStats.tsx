"use client";

import { useEffect, useState } from "react";

import IcebergMetricCard from "./IcebergMetricCard";

import {
  Database,
  HardDrive,
  Files,
  Layers,
} from "lucide-react";

import { getIcebergTables } from "@/services/iceberg";

export default function IcebergStats() {
  const [metrics, setMetrics] = useState<
    {
      id: number;
      title: string;
      value: string | number;
      description: string;
      icon: any;
    }[]
  >([]);

  useEffect(() => {
    async function loadStats() {
      const tables = await getIcebergTables();

      const totalTables = tables.length;

      const totalSnapshots = tables.reduce(
        (sum, table) => sum + table.health.snapshot_count,
        0
      );

      const totalFiles = tables.reduce(
        (sum, table) => sum + table.health.data_file_count,
        0
      );

      const totalStorage = tables.reduce(
        (sum, table) => sum + table.health.total_size_mb,
        0
      );

      setMetrics([
        {
          id: 1,
          title: "Iceberg Tables",
          value: totalTables,
          description: "Tables in catalog",
          icon: Database,
        },
        {
          id: 2,
          title: "Snapshots",
          value: totalSnapshots,
          description: "Across all tables",
          icon: Layers,
        },
        {
          id: 3,
          title: "Data Files",
          value: totalFiles,
          description: "Across all tables",
          icon: Files,
        },
        {
          id: 4,
          title: "Storage",
          value: `${totalStorage.toFixed(2)} MB`,
          description: "Total Iceberg size",
          icon: HardDrive,
        },
      ]);
    }

    loadStats();
  }, []);

  if (metrics.length === 0) {
    return (
      <p className="text-slate-400">
        Loading Iceberg statistics...
      </p>
    );
  }

  return (
    <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => (
        <IcebergMetricCard
          key={metric.id}
          title={metric.title}
          value={metric.value}
          description={metric.description}
          icon={metric.icon}
        />
      ))}
    </div>
  );
}