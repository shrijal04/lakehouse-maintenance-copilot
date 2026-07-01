"use client";

import { useEffect, useState } from "react";
import { Database } from "lucide-react";

import { getIcebergTables, IcebergTable } from "@/services/iceberg";
import { TableName } from "@/types/iceberg";

interface Props {
  selectedTable: TableName;
}

export default function TableDetails({
  selectedTable,
}: Props) {
  const [table, setTable] = useState<IcebergTable | null>(null);

  useEffect(() => {
    async function loadTable() {
      const tables = await getIcebergTables();

      const selected = tables.find(
        (t) => t.table_name === selectedTable
      );

      if (selected) {
        setTable(selected);
      }
    }

    loadTable();
  }, [selectedTable]);

  if (!table) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-white">
        Loading table details...
      </div>
    );
  }

  const items = [
    ["Table", table.table_name],
    ["Namespace", "local.lakehouse"],
    ["Snapshots", table.health.snapshot_count],
    ["Manifest Files", table.health.manifest_file_count],
    ["Data Files", table.health.data_file_count],
    ["Average File Size", `${table.health.average_file_kb} KB`],
    ["Storage", `${table.health.total_size_mb} MB`],
    ["Orphan Files", table.health.orphan_file_count],
  ];

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-6 flex items-center gap-3">
        <div className="rounded-lg bg-cyan-500/10 p-2">
          <Database
            className="text-cyan-400"
            size={22}
          />
        </div>

        <div>
          <h2 className="text-xl font-semibold text-white">
            Table Details
          </h2>

          <p className="text-slate-400">
            {table.full_name}
          </p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {items.map(([label, value]) => (
          <div
            key={label}
            className="rounded-xl bg-slate-800 p-4"
          >
            <p className="text-sm text-slate-400">
              {label}
            </p>

            <p className="mt-2 text-lg font-semibold text-white">
              {value}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}