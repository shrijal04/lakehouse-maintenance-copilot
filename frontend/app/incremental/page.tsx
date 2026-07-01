"use client";

import { useEffect, useState } from "react";
import AppLayout from "@/components/layout/appLayout";

import {
  runIncrementalLoad,
  simulateBusinessDay,
  getEtlHistory,
} from "@/services/etl";

import { simulateSmallFiles } from "@/services/maintenance";

export default function IncrementalPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  const [showModal, setShowModal] = useState(false);
  const [simulating, setSimulating] = useState(false);

  const [simulationType, setSimulationType] = useState<
    "business" | "smallFiles"
  >("business");

  // ==========================================
  // Load ETL History
  // ==========================================

  async function loadHistory() {
    try {
      const data = await getEtlHistory();
      setHistory(data);
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  // ==========================================
  // Run Incremental Load
  // ==========================================

  async function handleRunIncremental() {
    try {
      setLoading(true);

      const data = await runIncrementalLoad();

      setResult(data);

      await loadHistory();
    } catch (error) {
      console.error(error);
      alert("Failed to run Incremental Load.");
    } finally {
      setLoading(false);
    }
  }

  // ==========================================
  // Simulate Business Day
  // ==========================================

  async function handleSimulation() {
    try {
      setSimulating(true);

      const data = await simulateBusinessDay();

      alert(
        `${data.new_orders} new orders created\n${data.updated_orders} existing orders updated`
      );

      setShowModal(false);
    } catch (error) {
      console.error(error);
      alert("Simulation failed.");
    } finally {
      setSimulating(false);
    }
  }

  async function handleSmallFileSimulation() {
    try {
      setSimulating(true);

      const data = await simulateSmallFiles();

      alert(
        `${data.batches_written} batches written.\nSmall files successfully created in the Iceberg table.`
      );

      setShowModal(false);
    } catch (error) {
      console.error(error);
      alert("Failed to simulate small files.");
    } finally {
      setSimulating(false);
    }
  }

  return (
    <AppLayout>
      <div className="space-y-10">
        {/* Header */}

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white">
              Incremental Load
            </h1>

            <p className="mt-2 text-lg text-slate-400">
              Run incremental ETL and monitor execution history.
            </p>
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => {
                setSimulationType("business");
                setShowModal(true);
              }}
              className="rounded-xl bg-amber-500 px-6 py-3 font-semibold text-black hover:bg-amber-400"
            >
              Simulate Business Day
            </button>

            <button
              onClick={() => {
                setSimulationType("smallFiles");
                setShowModal(true);
              }}
              className="rounded-xl bg-red-500 px-6 py-3 font-semibold text-white hover:bg-red-400"
            >
              Simulate Small Files
            </button>

            <button
              onClick={handleRunIncremental}
              disabled={loading}
              className="rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-black hover:bg-cyan-400 disabled:bg-slate-500"
            >
              {loading ? "Running..." : "Run Incremental Load"}
            </button>

        </div>
        </div> 

        {/* Latest Result */}

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-6 text-2xl font-semibold text-white">
            Latest Result
          </h2>

          {result ? (
            <div className="grid grid-cols-2 gap-6 lg:grid-cols-4">
              <div>
                <p className="text-slate-400">Status</p>

                <p className="mt-2 text-xl font-bold text-green-400">
                  {result.status}
                </p>
              </div>

              <div>
                <p className="text-slate-400">Orders Merged</p>

                <p className="mt-2 text-xl font-bold text-white">
                  {result.orders_merged}
                </p>
              </div>

              <div>
                <p className="text-slate-400">Order Items Merged</p>

                <p className="mt-2 text-xl font-bold text-white">
                  {result.order_items_merged}
                </p>
              </div>

              <div>
                <p className="text-slate-400">Previous Last Run</p>

                <p className="mt-2 text-white">{result.last_run}</p>
              </div>
            </div>
          ) : (
            <p className="text-slate-400">
              No incremental load has been run during this session.
            </p>
          )}
        </div>

        {/* ETL History */}

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="mb-6 text-2xl font-semibold text-white">
            ETL History
          </h2>

          <div className="overflow-x-auto">
            <table className="min-w-full text-left">
              <thead className="border-b border-slate-700 text-slate-400">
                <tr>
                  <th className="pb-3">Pipeline</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3">Orders</th>
                  <th className="pb-3">Items</th>
                  <th className="pb-3">Start Time</th>
                  <th className="pb-3">End Time</th>
                </tr>
              </thead>

              <tbody>
                {history.map((row) => (
                  <tr
                    key={row.id}
                    className="border-b border-slate-800"
                  >
                    <td className="py-4 text-white">
                      {row.pipeline_name}
                    </td>

                    <td className="py-4">
                      <span className="rounded-lg bg-green-500/20 px-3 py-1 text-green-400">
                        {row.status}
                      </span>
                    </td>

                    <td className="py-4 text-white">
                      {row.orders_processed}
                    </td>

                    <td className="py-4 text-white">
                      {row.order_items_processed}
                    </td>

                    <td className="py-4 text-slate-300">
                      {row.start_time}
                    </td>

                    <td className="py-4 text-slate-300">
                      {row.end_time}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Confirmation Modal */}

        {showModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
            <div className="w-full max-w-lg rounded-2xl border border-slate-700 bg-slate-900 p-8 shadow-2xl">
              <h2 className="text-2xl font-bold text-white">
                {simulationType === "business"
                  ? "Simulate Business Day"
                  : "Simulate Small Files"}
              </h2>

              <p className="mt-4 text-slate-300">
                {simulationType === "business"
                  ? "This will generate new orders and update existing ones in PostgreSQL."
                  : "This will intentionally create hundreds of tiny files in BOTH Iceberg fact tables to simulate a fragmented Lakehouse."}
              </p>

              <div className="mt-6 rounded-xl border border-amber-500/40 bg-amber-500/10 p-4">
                {simulationType === "business" ? (
                <>
                  <p className="text-amber-300">
                    This does <strong>NOT</strong> update the Iceberg tables.
                  </p>

                  <p className="mt-2 text-sm text-slate-400">
                    After the simulation completes, run the Incremental Load to merge the
                    new PostgreSQL data into Iceberg.
                  </p>
                </>
              ) : (
                <>
                  <p className="text-red-300">
                    This WILL intentionally create hundreds of tiny files in both Iceberg
                    fact tables.
                  </p>

                  <p className="mt-2 text-sm text-slate-400">
                    This action is only used to demonstrate Lakehouse fragmentation before
                    running maintenance.
                  </p>
                </>
              )}

              </div>

              <div className="mt-8 flex justify-end gap-4">
                <button
                  onClick={() => setShowModal(false)}
                  disabled={simulating}
                  className="rounded-xl border border-slate-600 px-5 py-2 text-white hover:bg-slate-800"
                >
                  Cancel
                </button>

                <button
                  onClick={
                    simulationType === "business"
                      ? handleSimulation
                      : handleSmallFileSimulation
                  }
                  disabled={simulating}
                  className="rounded-xl bg-amber-500 px-5 py-2 font-semibold text-black hover:bg-amber-400 disabled:bg-slate-600"
                >
                  {simulating
                    ? "Simulating..."
                    : simulationType === "business"
                    ? "Yes, Simulate Business Day"
                    : "Yes, Create Small Files"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}