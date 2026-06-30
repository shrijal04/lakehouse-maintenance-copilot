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

const API = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

interface HealthHistory {
  checked_at: string;
  snapshot_count: number;
  data_file_count: number;
  average_file_kb: number;
}

export default function HealthTrend() {
  const [history, setHistory] = useState<HealthHistory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await fetch(
          `${API}/lakehouse/orders/history`
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
  }, []);

  const chartData = history.map((item) => ({
    time: new Date(item.checked_at).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
    files: item.data_file_count,
  }));

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-2xl font-semibold text-white">
        Health Trend
      </h2>

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