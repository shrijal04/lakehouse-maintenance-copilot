"use client";

import { useEffect, useState } from "react";
import { HardDrive, Database } from "lucide-react";

import { getHealth } from "@/services/health";
import { TableHealth } from "@/types/health";

export default function StorageMetadata() {
  const [tables, setTables] = useState<TableHealth[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const data = await getHealth(
          "lakehouse",
          "both"
        );

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
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {tables.map((table) => {
        const title = table.table
          .split(".")
          .pop()!
          .replace("_", " ")
          .replace(/\b\w/g, (c: string) =>
            c.toUpperCase()
          );

        return (
          <>
            {/* Storage */}
            <div
              key={`${table.table}-storage`}
              className="rounded-3xl border border-slate-800 bg-slate-900 p-6"
            >
              <div className="mb-5 flex items-center gap-3">
                <HardDrive className="text-cyan-400" />

                <h2 className="text-xl font-semibold text-white">
                  {title} Storage
                </h2>
              </div>

              <div className="space-y-4">
                <p className="text-white">
                  Total Size :
                  <span className="ml-2 font-bold">
                    {table.total_size_mb} MB
                  </span>
                </p>

                <p className="text-white">
                  Data Files :
                  <span className="ml-2 font-bold">
                    {table.data_file_count}
                  </span>
                </p>

                <p className="text-white">
                  Average File Size :
                  <span className="ml-2 font-bold">
                    {table.average_file_kb} KB
                  </span>
                </p>
              </div>
            </div>

            {/* Metadata */}
            <div
              key={`${table.table}-metadata`}
              className="rounded-3xl border border-slate-800 bg-slate-900 p-6"
            >
              <div className="mb-5 flex items-center gap-3">
                <Database className="text-cyan-400" />

                <h2 className="text-xl font-semibold text-white">
                  {title} Metadata
                </h2>
              </div>

              <div className="space-y-4">
                <p className="text-white">
                  Snapshots :
                  <span className="ml-2 font-bold">
                    {table.snapshot_count}
                  </span>
                </p>

                <p className="text-white">
                  Manifest Files :
                  <span className="ml-2 font-bold">
                    {table.manifest_file_count}
                  </span>
                </p>

                <p className="text-white">
                  Orphan Files :
                  <span className="ml-2 font-bold">
                    {table.orphan_file_count}
                  </span>
                </p>
              </div>
            </div>
          </>
        );
      })}
    </div>
  );
}