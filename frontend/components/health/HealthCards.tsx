import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Wrench,
} from "lucide-react";

import { healthMetrics } from "@/data/health";

const icons = {
  green: CheckCircle2,
  yellow: AlertTriangle,
  red: XCircle,
  cyan: Wrench,
};

const colors = {
  green: "text-green-400",
  yellow: "text-yellow-400",
  red: "text-red-400",
  cyan: "text-cyan-400",
};

export default function HealthCards() {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {healthMetrics.map((metric) => {
        const Icon = icons[metric.color];

        return (
          <div
            key={metric.id}
            className="rounded-2xl border border-slate-800 bg-slate-900 p-5 transition hover:border-cyan-500"
          >
            <Icon
              className={colors[metric.color]}
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
  );
}