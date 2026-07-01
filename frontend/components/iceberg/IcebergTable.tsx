"use client";

import { useEffect, useState } from "react";
import { Search, Eye } from "lucide-react";

import { getIcebergTables, IcebergTable as IcebergTableType } from "@/services/iceberg";
import { TableName } from "@/types/iceberg";

interface IcebergTableProps {
  selectedTable: TableName;
  setSelectedTable: React.Dispatch<
    React.SetStateAction<TableName>
  >;
}

export default function IcebergTable({
  selectedTable,
  setSelectedTable,
}: IcebergTableProps) {
  const [tables, setTables] = useState<IcebergTableType[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    getIcebergTables().then(setTables);
  }, []);

  const filteredTables = tables.filter((table) =>
    table.table_name.toLowerCase().includes(search.toLowerCase())
  );

  function getStatus(table: IcebergTableType) {
    const health = table.health;

    if (
      health.average_file_kb < 128 ||
      health.manifest_file_count > 100
    ) {
      return "Warning";
    }

    return "Healthy";
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-white">
          Iceberg Tables
        </h2>

        <div className="relative">
          <Search
            size={18}
            className="absolute left-3 top-3 text-slate-500"
          />

          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search tables..."
            className="rounded-xl border border-slate-700 bg-slate-950 py-2 pl-10 pr-4 text-white"
          />
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-800 text-left text-slate-400">
              <th className="pb-4">Table</th>
              <th className="pb-4">Namespace</th>
              <th className="pb-4">Files</th>
              <th className="pb-4">Size</th>
              <th className="pb-4">Status</th>
              <th className="pb-4 text-center">Action</th>
            </tr>
          </thead>

          <tbody>
            {filteredTables.map((table) => {
              const status = getStatus(table);

              return (
                <tr
                  key={table.table_name}
                  onClick={() =>
                    setSelectedTable(table.table_name as TableName)
                  }
                  className={`cursor-pointer border-b border-slate-800 transition ${
                    selectedTable === table.table_name
                      ? "bg-cyan-500/10"
                      : "hover:bg-slate-800/40"
                  }`}
                >
                  <td className="py-5 font-medium text-white">
                    {table.table_name}
                  </td>

                  <td className="text-slate-300">
                    local.lakehouse
                  </td>

                  <td className="text-white">
                    {table.health.data_file_count}
                  </td>

                  <td className="text-white">
                    {table.health.total_size_mb.toFixed(2)} MB
                  </td>

                  <td>
                    <span
                      className={`rounded-full px-3 py-1 text-sm ${
                        status === "Healthy"
                          ? "bg-green-500/20 text-green-400"
                          : "bg-yellow-500/20 text-yellow-400"
                      }`}
                    >
                      {status}
                    </span>
                  </td>

                  <td className="text-center">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedTable(
                          table.table_name as TableName
                        );
                      }}
                      className="rounded-lg bg-cyan-500/10 p-2 text-cyan-400 hover:bg-cyan-500 hover:text-black"
                    >
                      <Eye size={18} />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}