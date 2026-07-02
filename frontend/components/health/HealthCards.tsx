"use client";

import { useEffect, useState } from "react";
import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
} from "lucide-react";

import { TableHealth, HealthMetric } from "@/types/health";
import { getHealth } from "@/services/health";

const icons = {
  green: CheckCircle2,
  yellow: AlertTriangle,
  red: XCircle,
};

const colors = {
  green: "text-green-400",
  yellow: "text-yellow-400",
  red: "text-red-400",
};

function snapshotColor(count: number) {
  if (count <= 10) return "green";
  if (count <= 30) return "yellow";
  return "red";
}

function dataFileColor(count: number) {
  if (count <= 5) return "green";
  if (count <= 20) return "yellow";
  return "red";
}

function avgFileColor(size: number) {
  if (size >= 128) return "green";
  if (size >= 64) return "yellow";
  return "red";
}

function storageColor(size: number) {
  if (size < 500) return "green";
  if (size < 1000) return "yellow";
  return "red";
}

function buildMetrics(
  health: TableHealth
): HealthMetric[] {
  return [
    {
      id: 1,
      title: "Snapshots",
      value: health.snapshot_count,
      description: "Current snapshots",
      color: snapshotColor(health.snapshot_count),
    },
    {
      id: 2,
      title: "Data Files",
      value: health.data_file_count,
      description: "Current data files",
      color: dataFileColor(health.data_file_count),
    },
    {
      id: 3,
      title: "Average File KB",
      value: health.average_file_kb,
      description: "Average file size",
      color: avgFileColor(health.average_file_kb),
    },
    {
      id: 4,
      title: "Total Size MB",
      value: health.total_size_mb,
      description: "Total storage",
      color: storageColor(health.total_size_mb),
    },
  ];
}

export default function HealthCards() {
  const [healthTables, setHealthTables] = useState<
    TableHealth[]
  >([]);

  useEffect(() => {
    async function loadHealth() {
      try {
        const data = await getHealth(
          "lakehouse",
          "both"
        );

        if (Array.isArray(data)) {
          setHealthTables(data);
        } else {
          setHealthTables([data]);
        }
      } catch (err) {
        console.error(err);
      }
    }

    loadHealth();
  }, []);

  if (healthTables.length === 0) {
    return (
      <p className="text-slate-400">
        Loading...
      </p>
    );
  }

  return (
    <div className="space-y-10">
      {healthTables.map((table) => {
        const title = table.table
          .split(".")
          .pop()!
          .replace("_", " ")
          .replace(
            /\b\w/g,
            (c: string) => c.toUpperCase()
          );

        return (
          <div key={table.table}>
            <h2 className="mb-6 text-2xl font-bold text-white">
              {title}
            </h2>

            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
              {buildMetrics(table).map((metric) => {
                const Icon =
                  icons[
                    metric.color as keyof typeof icons
                  ];

                return (
                  <div
                    key={`${table.table}-${metric.id}`}
                    className="rounded-2xl border border-slate-800 bg-slate-900 p-5 transition hover:border-cyan-500"
                  >
                    <Icon
                      className={
                        colors[
                          metric.color as keyof typeof colors
                        ]
                      }
                      size={30}
                    />

                    <h3 className="mt-5 text-lg font-semibold text-white">
                      {metric.title}
                    </h3>

                    <p className="mt-4 text-4xl font-bold text-white">
                      {metric.value}
                    </p>

                    <p className="mt-2 text-slate-400">
                      {metric.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}