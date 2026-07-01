"use client";

import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

const API =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

interface HealthHistory {
  day: string;
  snapshot_count: number;
  data_file_count: number;
  average_file_kb: number;
}

type TableType = "orders" | "order_items";

export default function HealthTrend() {
  const [selectedTable, setSelectedTable] =
    useState<TableType>("orders");

  const [history, setHistory] = useState<HealthHistory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        setLoading(true);

        const response = await fetch(
          `${API}/lakehouse/${selectedTable}/history`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch history");
        }

        const data: HealthHistory[] = await response.json();

        setHistory(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, [selectedTable]);

  const chartData = history.map((item) => ({
    time: new Date(item.day).toLocaleDateString([], {
      month: "short",
      day: "numeric",
    }),
    files: item.data_file_count,
  }));

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-semibold text-white">
          Health Trend
        </h2>

        <select
          value={selectedTable}
          onChange={(e) =>
            setSelectedTable(e.target.value as TableType)
          }
          className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-white"
        >
          <option value="orders">Orders</option>
          <option value="order_items">Order Items</option>
        </select>
      </div>

      {loading ? (
        <p className="text-slate-400">Loading...</p>
      ) : (
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid stroke="#334155" />

              <XAxis
                dataKey="time"
                stroke="#94a3b8"
              />

              <YAxis stroke="#94a3b8" />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="files"
                stroke="#06b6d4"
                strokeWidth={4}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}