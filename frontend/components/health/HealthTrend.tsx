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
  run: number;
  recorded_at: string;
  snapshot_count: number;
  data_file_count: number;
  average_file_kb: number;
  total_size_mb: number;
  manifest_file_count: number;
  orphan_file_count: number;
}

interface Props {
  table: "orders" | "order-items";
  title: string;
}

export default function HealthTrend({
  table,
  title,
}: Props) {
  const [history, setHistory] = useState<HealthHistory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        setLoading(true);

        const response = await fetch(
          `${API}/lakehouse/${table}/history`
        );

        const data = await response.json();

        setHistory(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, [table]);

  const chartData = history.map((item) => ({
    run: `Run ${item.run}`,
    files: item.data_file_count,
  }));

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-2xl font-semibold text-white">
        {title}
      </h2>

      {loading ? (
        <p className="text-slate-400">Loading...</p>
      ) : (
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid stroke="#334155" />

              <XAxis
                dataKey="run"
                stroke="#94a3b8"
              />

              <YAxis stroke="#94a3b8" />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="files"
                stroke="#06b6d4"
                strokeWidth={4}
                dot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}