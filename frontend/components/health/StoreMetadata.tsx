"use client";

import { useEffect, useState } from "react";
import { HardDrive, Database } from "lucide-react";

import {
  getHealth,
  getOrderItemsHealth,
} from "@/services/health";

import { TableHealth } from "@/types/health";

export default function StorageMetadata() {
  const [orders, setOrders] = useState<TableHealth | null>(null);
  const [orderItems, setOrderItems] = useState<TableHealth | null>(null);

  useEffect(() => {
    getHealth().then(setOrders);
    getOrderItemsHealth().then(setOrderItems);
  }, []);

  if (!orders || !orderItems) {
    return (
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">

      {/* Orders Storage */}
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
        <div className="mb-5 flex items-center gap-3">
          <HardDrive className="text-cyan-400" />
          <h2 className="text-xl font-semibold text-white">
            Orders Storage
          </h2>
        </div>

        <div className="space-y-4">
          <p className="text-white">
            Total Size :
            <span className="ml-2 font-bold">
              {orders.total_size_mb} MB
            </span>
          </p>

          <p className="text-white">
            Data Files :
            <span className="ml-2 font-bold">
              {orders.data_file_count}
            </span>
          </p>

          <p className="text-white">
            Average File Size :
            <span className="ml-2 font-bold">
              {orders.average_file_kb} KB
            </span>
          </p>
        </div>
      </div>

      {/* Order Items Storage */}
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
        <div className="mb-5 flex items-center gap-3">
          <HardDrive className="text-cyan-400" />
          <h2 className="text-xl font-semibold text-white">
            Order Items Storage
          </h2>
        </div>

        <div className="space-y-4">
          <p className="text-white">
            Total Size :
            <span className="ml-2 font-bold">
              {orderItems.total_size_mb} MB
            </span>
          </p>

          <p className="text-white">
            Data Files :
            <span className="ml-2 font-bold">
              {orderItems.data_file_count}
            </span>
          </p>

          <p className="text-white">
            Average File Size :
            <span className="ml-2 font-bold">
              {orderItems.average_file_kb} KB
            </span>
          </p>
        </div>
      </div>

      {/* Orders Metadata */}
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
        <div className="mb-5 flex items-center gap-3">
          <Database className="text-cyan-400" />
          <h2 className="text-xl font-semibold text-white">
            Orders Metadata
          </h2>
        </div>

        <div className="space-y-4">
          <p className="text-white">
            Snapshots :
            <span className="ml-2 font-bold">
              {orders.snapshot_count}
            </span>
          </p>

          <p className="text-white">
            Manifest Files :
            <span className="ml-2 font-bold">
              {orders.manifest_file_count}
            </span>
          </p>

          <p className="text-white">
            Orphan Files :
            <span className="ml-2 font-bold">
              {orders.orphan_file_count}
            </span>
          </p>
        </div>
      </div>

      {/* Order Items Metadata */}
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
        <div className="mb-5 flex items-center gap-3">
          <Database className="text-cyan-400" />
          <h2 className="text-xl font-semibold text-white">
            Order Items Metadata
          </h2>
        </div>

        <div className="space-y-4">
          <p className="text-white">
            Snapshots :
            <span className="ml-2 font-bold">
              {orderItems.snapshot_count}
            </span>
          </p>

          <p className="text-white">
            Manifest Files :
            <span className="ml-2 font-bold">
              {orderItems.manifest_file_count}
            </span>
          </p>

          <p className="text-white">
            Orphan Files :
            <span className="ml-2 font-bold">
              {orderItems.orphan_file_count}
            </span>
          </p>
        </div>
      </div>

    </div>
  );
}