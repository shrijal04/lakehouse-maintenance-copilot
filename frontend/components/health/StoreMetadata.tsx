"use client";

import { useEffect, useState } from "react";
import { HardDrive, Database } from "lucide-react";

import { getHealth } from "@/services/health";
import { TableHealth } from "@/types/health";

export default function StorageMetadata() {
  const [health, setHealth] = useState<TableHealth | null>(null);

  useEffect(() => {
    getHealth().then(setHealth);
  }, []);

  if (!health) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">

      {/* Storage Information */}

      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">

        <div className="mb-5 flex items-center gap-3">
          <HardDrive className="text-cyan-400" />

          <h2 className="text-xl font-semibold text-white">
            Storage
          </h2>
        </div>

        <div className="space-y-4">

          <p className="text-white">
            Total Size :
            <span className="ml-2 font-bold">
              {health.total_size_mb} MB
            </span>
          </p>

          <p className="text-white">
            Data Files :
            <span className="ml-2 font-bold">
              {health.data_file_count}
            </span>
          </p>

          <p className="text-white">
            Average File Size :
            <span className="ml-2 font-bold">
              {health.average_file_kb} KB
            </span>
          </p>

        </div>

      </div>

      {/* Metadata */}

      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">

        <div className="mb-5 flex items-center gap-3">
          <Database className="text-cyan-400" />

          <h2 className="text-xl font-semibold text-white">
            Metadata Health
          </h2>
        </div>

        <div className="space-y-4">

          <p className="text-white">
            Snapshots :
            <span className="ml-2 font-bold">
              {health.snapshot_count}
            </span>
          </p>

          <p className="text-white">
            Manifest Files :
            <span className="ml-2 font-bold">
              {health.manifest_file_count}
            </span>
          </p>

          <p className="text-white">
            Orphan Files :
            <span className="ml-2 font-bold">
              {health.orphan_file_count}
            </span>
          </p>

        </div>

      </div>

    </div>
  );
}