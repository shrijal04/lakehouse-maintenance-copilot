import { Search, Filter, Eye } from "lucide-react";

import { icebergTables } from "@/data/iceberg";

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
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-white">
          Iceberg Tables
        </h2>

        <div className="flex gap-3">
          <div className="relative">
            <Search
              size={18}
              className="absolute left-3 top-3 text-slate-500"
            />

            <input
              placeholder="Search..."
              className="rounded-xl border border-slate-700 bg-slate-950 py-2 pl-10 pr-4 text-white"
            />
          </div>

          <button className="flex items-center gap-2 rounded-xl border border-slate-700 bg-slate-950 px-4 py-2 text-white">
            <Filter size={18} />
            Filter
          </button>
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
            {icebergTables.map((table) => (
              <tr
                key={table.id}
                onClick={() => setSelectedTable(table.table)}
                className={`cursor-pointer border-b border-slate-800 transition ${
                  selectedTable === table.table
                    ? "bg-cyan-500/10"
                    : "hover:bg-slate-800/40"
                }`}
              >
                <td className="py-5 font-medium text-white">
                  {table.table}
                </td>

                <td>{table.namespace}</td>

                <td>{table.files}</td>

                <td>{table.size}</td>

                <td>
                  <span
                    className={`rounded-full px-3 py-1 text-sm ${
                      table.status === "Healthy"
                        ? "bg-green-500/20 text-green-400"
                        : table.status === "Warning"
                        ? "bg-yellow-500/20 text-yellow-400"
                        : "bg-red-500/20 text-red-400"
                    }`}
                  >
                    {table.status}
                  </span>
                </td>

                <td className="text-center">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedTable(table.table);
                    }}
                    className="rounded-lg bg-cyan-500/10 p-2 text-cyan-400 hover:bg-cyan-500 hover:text-black"
                  >
                    <Eye size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}