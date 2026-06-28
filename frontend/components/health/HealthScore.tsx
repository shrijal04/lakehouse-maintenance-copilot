import { HeartPulse } from "lucide-react";

import { healthScore } from "@/data/health";
import HealthTrend from "@/components/health/HealthTrend";
import StorageMetadata from "@/components/health/StoreMetadata";
import IssuesTable from "@/components/health/IssuesTable";
import ResourceUsage from "@/components/health/ResourceUsage";
import MaintenanceHistory from "@/components/health/MaintenanceHistory";
export default function HealthScore() {
  const radius = 85;
  const stroke = 14;

  const circumference = 2 * Math.PI * radius;

  const offset =
    circumference -
    (healthScore.score / 100) * circumference;

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 px-10 pt-12 pb-10">
      <div className="mb-10 flex items-center gap-3">
        <HeartPulse
          className="text-cyan-400"
          size={28}
        />

        <h2 className="text-2xl font-semibold text-white">
          Overall Health
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
              {healthScore.score}%
            </p>

            <p className="mt-2 text-lg font-medium text-green-400">
              {healthScore.status}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}