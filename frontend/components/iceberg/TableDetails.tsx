import { Database } from "lucide-react";

import { tableDetails } from "@/data/iceberg";

import { TableName } from "@/types/iceberg";

interface Props {
  selectedTable: TableName;
}

export default function TableDetails({
  selectedTable,
}: Props) {

  const detail = tableDetails[selectedTable];

  const items = [
    ["Format Version", detail.formatVersion],
    ["Partition Spec", detail.partitionSpec],
    ["Snapshots", detail.snapshots],
    ["Manifest Files", detail.manifestFiles],
    ["Data Files", detail.dataFiles],
    ["Storage", detail.storage],
    ["Compression", detail.compression],
    ["Last Optimized", detail.optimized],
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
            {detail.tableName}
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