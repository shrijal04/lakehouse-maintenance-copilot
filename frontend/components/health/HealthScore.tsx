"use client";

import { useEffect, useState } from "react";
import { HeartPulse } from "lucide-react";

import {
  getHealth,
  getOrderItemsHealth,
} from "@/services/health";

import { TableHealth } from "@/types/health";

export default function HealthScore() {
  const [orders, setOrders] = useState<TableHealth | null>(null);
  const [orderItems, setOrderItems] = useState<TableHealth | null>(null);

  useEffect(() => {
    async function load() {
      const [ordersHealth, orderItemsHealth] = await Promise.all([
        getHealth(),
        getOrderItemsHealth(),
      ]);

      setOrders(ordersHealth);
      setOrderItems(orderItemsHealth);
    }

    load();
  }, []);

  if (!orders || !orderItems) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-10 text-white">
        Loading...
      </div>
    );
  }

  // ----------------------------------
  // Combined Lakehouse Metrics
  // ----------------------------------

  const snapshotCount =
    orders.snapshot_count + orderItems.snapshot_count;

  const dataFileCount =
    orders.data_file_count + orderItems.data_file_count;

  const averageFileKB =
    (orders.average_file_kb + orderItems.average_file_kb) / 2;

  // ----------------------------------
  // Health Score
  // ----------------------------------

  let score = 100;

  if (snapshotCount > 100) {
    score -= 30;
  } else if (snapshotCount > 40) {
    score -= 15;
  }

  if (averageFileKB < 64) {
    score -= 30;
  } else if (averageFileKB < 128) {
    score -= 15;
  }

  if (dataFileCount > 40) {
    score -= 20;
  }

  score = Math.max(score, 0);

  let status: "Healthy" | "Warning" | "Critical";

  if (score >= 80) {
    status = "Healthy";
  } else if (score >= 50) {
    status = "Warning";
  } else {
    status = "Critical";
  }

  const radius = 85;
  const stroke = 14;
  const circumference = 2 * Math.PI * radius;

  const offset =
    circumference - (score / 100) * circumference;

  const statusColor =
    status === "Healthy"
      ? "text-green-400"
      : status === "Warning"
      ? "text-yellow-400"
      : "text-red-400";

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 px-10 pt-12 pb-10">
      <div className="mb-10 flex items-center gap-3">
        <HeartPulse
          className="text-cyan-400"
          size={28}
        />

        <h2 className="text-2xl font-semibold text-white">
          Overall Lakehouse Health
        </h2>
      </div>

      <div className="flex justify-center">
        <div className="relative flex h-[220px] w-[220px] items-center justify-center">
          <svg
            width="220"
            height="220"
            className="-rotate-90"
          >
            <circle
              cx="110"
              cy="110"
              r={radius}
              stroke="#1e293b"
              strokeWidth={stroke}
              fill="transparent"
            />

            <circle
              cx="110"
              cy="110"
              r={radius}
              stroke="#06b6d4"
              strokeWidth={stroke}
              fill="transparent"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              className="transition-all duration-700"
            />
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <p className="text-6xl font-bold text-white">
              {score}%
            </p>

            <p className={`mt-2 text-lg font-medium ${statusColor}`}>
              {status}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}