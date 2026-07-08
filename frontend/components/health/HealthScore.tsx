"use client";

import { useEffect, useState } from "react";
import { HeartPulse } from "lucide-react";

import { getHealth } from "@/services/health";
import { TableHealth } from "@/types/health";

export default function HealthScore() {
  const [tables, setTables] = useState<TableHealth[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await getHealth("silver", "both");

        if (Array.isArray(data)) {
          setTables(data);
        } else {
          setTables([data]);
        }
      } catch (err) {
        console.error(err);
      }
    }

    load();
  }, []);

  if (tables.length === 0) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-10 text-white">
        Loading...
      </div>
    );
  }

  // ----------------------------------
  // Overall Health Score
  // ----------------------------------

  const score = Math.round(
    tables.reduce(
      (sum, table) => sum + table.health_score,
      0
    ) / tables.length
  );

  // ----------------------------------
  // Health Status
  // ----------------------------------

  let status: "Healthy" | "Warning" | "Critical";

  if (score >= 80) {
    status = "Healthy";
  } else if (score >= 50) {
    status = "Warning";
  } else {
    status = "Critical";
  }

  const radius = 85;
  const stroke = 14;
  const circumference = 2 * Math.PI * radius;

  const offset =
    circumference - (score / 100) * circumference;

  const statusColor =
    status === "Healthy"
      ? "text-green-400"
      : status === "Warning"
      ? "text-yellow-400"
      : "text-red-400";

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 px-10 pt-12 pb-10">
      <div className="mb-10 flex items-center gap-3">
        <HeartPulse
          className="text-cyan-400"
          size={28}
        />

        <h2 className="text-2xl font-semibold text-white">
          Overall Lakehouse Health
        </h2>
      </div>

      <div className="flex justify-center">
        <div className="relative flex h-[220px] w-[220px] items-center justify-center">
          <svg
            width="220"
            height="220"
            className="-rotate-90"
          >
            <circle
              cx="110"
              cy="110"
              r={radius}
              stroke="#1e293b"
              strokeWidth={stroke}
              fill="transparent"
            />

            <circle
              cx="110"
              cy="110"
              r={radius}
              stroke="#06b6d4"
              strokeWidth={stroke}
              fill="transparent"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              className="transition-all duration-700"
            />
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <p className="text-6xl font-bold text-white">
              {score}%
            </p>

            <p
              className={`mt-2 text-lg font-medium ${statusColor}`}
            >
              {status}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}