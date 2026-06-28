import {
  HardDrive,
  Database,
} from "lucide-react";

import {
  storageUsage,
  metadataHealth,
} from "@/data/health";

export default function StorageMetadata() {
  return (
    <div className="grid gap-6 lg:grid-cols-2">

      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">

        <div className="mb-5 flex items-center gap-3">
          <HardDrive className="text-cyan-400" />

          <h2 className="text-xl font-semibold text-white">
            Storage Usage
          </h2>
        </div>

        <div className="space-y-4">

          <div>
            <div className="mb-2 flex justify-between">
              <span className="text-slate-300">
                Used
              </span>

              <span className="text-white">
                {storageUsage.used}%
              </span>
            </div>

            <div className="h-3 rounded-full bg-slate-700">

              <div
                className="h-3 rounded-full bg-cyan-500"
                style={{
                  width: `${storageUsage.used}%`,
                }}
              />

            </div>

          </div>

          <p className="text-slate-400">
            Available : {storageUsage.available}%
          </p>

        </div>

      </div>

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
              {metadataHealth.snapshots}
            </span>
          </p>

          <p className="text-white">
            Manifest Files :
            <span className="ml-2 font-bold">
              {metadataHealth.manifestFiles}
            </span>
          </p>

          <p className="text-white">
            Orphan Files :
            <span className="ml-2 font-bold">
              {metadataHealth.orphanFiles}
            </span>
          </p>

        </div>

      </div>

    </div>
  );
}