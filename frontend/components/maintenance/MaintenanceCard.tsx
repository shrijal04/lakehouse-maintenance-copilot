"use client";

import { useState } from "react";

import {
  requestMaintenance,
  confirmMaintenance,
} from "@/services/maintenance";

import ConfirmationModal from "./ConfirmationModal";

export default function MaintenanceCard() {
  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState("");

  const [open, setOpen] = useState(false);

  const [confirmationId, setConfirmationId] = useState("");

  const [message, setMessage] = useState("");

  // -----------------------------------------
  // New State
  // -----------------------------------------

  const [database, setDatabase] = useState("lakehouse");

  const [target, setTarget] = useState<
    "orders" | "order_items" | "both"
  >("both");

  // -----------------------------------------
  // Step 1: Request Maintenance
  // -----------------------------------------

  async function runMaintenance() {
    try {
      setLoading(true);

      const response = await requestMaintenance({
        database,
        target,
      });

      setConfirmationId(response.confirmation_id);

      setMessage(response.message);

      setOpen(true);
    } catch (error) {
      console.error(error);
      setResult("Failed to request maintenance.");
    } finally {
      setLoading(false);
    }
  }

  // -----------------------------------------
  // Step 2: Confirm Maintenance
  // -----------------------------------------

  async function handleConfirm() {
    try {
      setLoading(true);

      const response = await confirmMaintenance(
        confirmationId,
        true,
        database,
        target
      );

      setResult(
        response.message ??
          "Maintenance completed successfully."
      );

      setOpen(false);
    } catch (error) {
      console.error(error);
      setResult("Maintenance failed.");
    } finally {
      setLoading(false);
    }
  }

  // -----------------------------------------
  // Cancel
  // -----------------------------------------

  function handleCancel() {
    setOpen(false);
  }

  return (
    <>
      <div className="rounded-3xl border border-slate-800 bg-slate-900 p-8">
        <h2 className="text-2xl font-semibold text-white">
          Run Maintenance
        </h2>

        <p className="mt-3 text-slate-400">
          Running maintenance will optimize your Apache Iceberg table by:
        </p>

        <ul className="mt-6 list-disc space-y-2 pl-6 text-slate-300">
          <li>Rewrite small data files</li>
          <li>Rewrite manifest files</li>
          <li>Expire old snapshots</li>
          <li>Remove orphan files</li>
        </ul>

        {/* Database */}

        <div className="mt-8">
          <label className="mb-2 block text-sm text-slate-300">
            Database
          </label>

          <select
            value={database}
            onChange={(e) => setDatabase(e.target.value)}
            className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white"
          >
            <option value="lakehouse">lakehouse</option>
          </select>
        </div>

        {/* Table */}

        <div className="mt-6">
          <label className="mb-2 block text-sm text-slate-300">
            Table
          </label>

          <select
            value={target}
            onChange={(e) =>
              setTarget(
                e.target.value as
                  | "orders"
                  | "order_items"
                  | "both"
              )
            }
            className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white"
          >
            <option value="orders">Orders</option>

            <option value="order_items">
              Order Items
            </option>

            <option value="both">
              Both Tables
            </option>
          </select>
        </div>

        <button
          onClick={runMaintenance}
          disabled={loading}
          className="mt-8 rounded-xl bg-cyan-600 px-6 py-3 font-semibold text-white hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Running..." : "Run Maintenance"}
        </button>

        {result && (
          <div className="mt-6 rounded-xl bg-slate-800 p-4 text-white">
            {result}
          </div>
        )}
      </div>

      <ConfirmationModal
        open={open}
        message={message}
        onConfirm={handleConfirm}
        onCancel={handleCancel}
      />
    </>
  );
}