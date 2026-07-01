"use client";

import { useState } from "react";
import {
  simulateBusinessDay,
  runIncrementalLoad,
} from "@/services/etl";

interface Props {
  onRefresh: () => void;
}

export default function ActionButtons({
  onRefresh,
}: Props) {
  const [loading, setLoading] = useState(false);

  async function handleSimulate() {
    try {
      setLoading(true);

      const result = await simulateBusinessDay();

      alert(
        `Simulation Complete\n\n` +
        `New Orders: ${result.new_orders}\n` +
        `Updated Orders: ${result.updated_orders}`
      );

      onRefresh();

    } catch (error) {
      console.error(error);
      alert("Simulation failed.");
    } finally {
      setLoading(false);
    }
  }

  async function handleIncremental() {
    try {
      setLoading(true);

      const result = await runIncrementalLoad();

      alert(
        `Incremental Load Complete\n\n` +
        `Orders Loaded: ${result.orders_merged}\n` +
        `Order Items Loaded: ${result.order_items_merged}`
      );

      onRefresh();

    } catch (error) {
      console.error(error);
      alert("Incremental load failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex gap-4">

      <button
        onClick={handleSimulate}
        disabled={loading}
        className="rounded-xl bg-amber-500 px-5 py-3 font-semibold text-black hover:bg-amber-400 disabled:opacity-50"
      >
        {loading ? "Please wait..." : "Simulate Business Day"}
      </button>

      <button
        onClick={handleIncremental}
        disabled={loading}
        className="rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-black hover:bg-cyan-400 disabled:opacity-50"
      >
        {loading ? "Please wait..." : "Run Incremental Load"}
      </button>

    </div>
  );
}