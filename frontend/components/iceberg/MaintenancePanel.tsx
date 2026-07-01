"use client";

import { Wrench } from "lucide-react";

export default function MaintenancePanel() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-6 flex items-center gap-3">
        <div className="rounded-lg bg-cyan-500/10 p-2">
          <Wrench className="text-cyan-400" size={22} />
        </div>

        <h2 className="text-xl font-semibold text-white">
          Maintenance
        </h2>
      </div>

      <div className="space-y-4">
        <div className="rounded-xl bg-slate-800 p-4">
          <p className="font-semibold text-white">
            Iceberg Maintenance
          </p>

          <p className="mt-2 text-sm text-slate-400">
            Run maintenance from the Maintenance page to rewrite
            data files, rewrite manifests, expire snapshots and
            remove orphan files.
          </p>
        </div>

        <button
          disabled
          className="w-full rounded-xl bg-slate-700 py-3 font-semibold text-slate-400"
        >
          Maintenance is available from the Maintenance page
        </button>
      </div>
    </div>
  );
}