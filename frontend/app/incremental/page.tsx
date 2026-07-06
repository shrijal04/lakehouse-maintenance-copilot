"use client";

import { useEffect, useState } from "react";
import AppLayout from "@/components/layout/appLayout";

import {
  runIncrementalLoad,
  simulateBusinessDay,
  getEtlHistory,
} from "@/services/etl";

import { simulateSmallFiles } from "@/services/maintenance";

import Overlay from "@/components/LoadingOverlay";

export default function IncrementalPage() {
  const [pageLoading, setPageLoading] = useState(true);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  const [showModal, setShowModal] = useState(false);
  const [simulating, setSimulating] = useState(false);

  const [simulationType, setSimulationType] = useState<
    "business" | "smallFiles"
  >("business");

  const [database, setDatabase] = useState("lakehouse");

  const [tableTarget, setTableTarget] = useState<
    "orders" | "order_items" | "both"
  >("both");

  const [batches, setBatches] = useState(100);
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
    async function loadPage() {
      try {
        await loadHistory();
      } finally {
        setPageLoading(false);
      }
    }

    loadPage();
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

      const data = await simulateSmallFiles({
        database,
        target: tableTarget,
        batches,
      });

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
    <>
      {pageLoading && <Overlay />}

      <AppLayout>
        <div className="space-y-10">
          {/* Header */}

          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white">
                Incremental Load
              </h1>

              <p className="mt-2 text-lg text-slate-400">
                Run incremental ETL and monitor execution history.
              </p>
            </div>

            <div className="flex flex-wrap gap-4">
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
            <div
              className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/70 p-4 sm:items-center"
              onClick={(e) => {
                // close when clicking the backdrop only
                if (e.target === e.currentTarget && !simulating) {
                  setShowModal(false);
                }
              }}
            >
              <div className="my-8 flex max-h-[90vh] w-full max-w-lg flex-col rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl">
                {/* Scrollable content area */}
                <div className="overflow-y-auto p-6 sm:p-8">
                  <h2 className="text-xl font-bold text-white sm:text-2xl">
                    {simulationType === "business"
                      ? "Simulate Business Day"
                      : "Simulate Small Files"}
                  </h2>

                  <p className="mt-4 text-sm text-slate-300 sm:text-base">
                    {simulationType === "business"
                      ? "This will generate new orders and update existing ones in PostgreSQL."
                      : "This will intentionally create hundreds of tiny files in BOTH Iceberg fact tables to simulate a fragmented Lakehouse."}
                  </p>

                  <div className="mt-6 rounded-xl border border-amber-500/40 bg-amber-500/10 p-4">
                    {simulationType === "business" ? (
                      <>
                        <p className="text-amber-300">
                          This does <strong>NOT</strong> update the Iceberg
                          tables.
                        </p>

                        <p className="mt-2 text-sm text-slate-400">
                          After the simulation completes, run the Incremental
                          Load to merge the new PostgreSQL data into Iceberg.
                        </p>
                      </>
                    ) : (
                      <>
                        <p className="text-red-300">
                          This will intentionally create many small files in
                          the selected Iceberg table(s).
                        </p>

                        <p className="mt-2 text-sm text-slate-400">
                          Choose which database and table(s) to simulate.
                        </p>

                        {/* Database */}

                        <div className="mt-6">
                          <label className="mb-2 block text-white">
                            Database
                          </label>

                          <select
                            value={database}
                            onChange={(e) => setDatabase(e.target.value)}
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-white"
                          >
                            <option value="lakehouse">lakehouse</option>

                            {/* Add more databases later */}
                          </select>
                        </div>

                        {/* Table */}

                        <div className="mt-4">
                          <label className="mb-2 block text-white">
                            Table
                          </label>

                          <select
                            value={tableTarget}
                            onChange={(e) =>
                              setTableTarget(
                                e.target.value as
                                  | "orders"
                                  | "order_items"
                                  | "both"
                              )
                            }
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-white"
                          >
                            <option value="orders">Orders</option>

                            <option value="order_items">Order Items</option>

                            <option value="both">Both</option>
                          </select>
                        </div>

                        {/* Batches */}

                        <div className="mt-4">
                          <label className="mb-2 block text-white">
                            Number of batches
                          </label>

                          <input
                            type="number"
                            min={1}
                            value={batches}
                            onChange={(e) =>
                              setBatches(Number(e.target.value))
                            }
                            className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-white"
                          />
                        </div>
                      </>
                    )}
                  </div>
                </div>

                {/* Sticky footer with actions - always visible, never clipped */}
                <div className="flex shrink-0 flex-col-reverse gap-3 border-t border-slate-800 p-4 sm:flex-row sm:justify-end sm:gap-4 sm:p-6">
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
    </>
  );
}
