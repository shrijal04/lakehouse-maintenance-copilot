import { Wrench } from "lucide-react";

import { maintenanceRecommendations } from "@/data/iceberg";

export default function MaintenancePanel() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

      <div className="mb-6 flex items-center gap-3">
        <div className="rounded-lg bg-cyan-500/10 p-2">
          <Wrench className="text-cyan-400" size={22} />
        </div>

        <h2 className="text-xl font-semibold text-white">
          Recommendations
        </h2>
      </div>

      <div className="space-y-4">
        {maintenanceRecommendations.map((item) => (
          <div
            key={item.id}
            className="rounded-xl bg-slate-800 p-4"
          >
            <p className="font-medium text-white">
              {item.task}
            </p>

            <span
              className={`mt-3 inline-block rounded-full px-3 py-1 text-xs font-semibold ${
                item.priority === "High"
                  ? "bg-red-500/20 text-red-400"
                  : item.priority === "Medium"
                  ? "bg-yellow-500/20 text-yellow-400"
                  : "bg-green-500/20 text-green-400"
              }`}
            >
              {item.priority}
            </span>
          </div>
        ))}

        <button className="mt-4 w-full rounded-xl bg-cyan-500 py-3 font-semibold text-black transition hover:bg-cyan-400">
          Run Maintenance
        </button>
      </div>

    </div>
  );
}