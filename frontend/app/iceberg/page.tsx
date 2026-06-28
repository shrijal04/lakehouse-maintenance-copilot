"use client";

import { useState } from "react";

import AppLayout from "@/components/layout/appLayout";

import IcebergStats from "@/components/iceberg/IcebergStats";
import IcebergTable from "@/components/iceberg/IcebergTable";
import TableDetails from "@/components/iceberg/TableDetails";
import MaintenancePanel from "@/components/iceberg/MaintenancePanel";
import { TableName } from "@/types/iceberg";

export default function IcebergPage() {
  // Selected table state
  const [selectedTable, setSelectedTable] =
  useState<TableName>("sales_orders");

  return (
    <AppLayout>
      <div className="space-y-10">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white">
              Iceberg Catalog
            </h1>

            <p className="mt-2 text-lg text-slate-400">
              Manage Apache Iceberg tables, metadata and maintenance.
            </p>
          </div>

          <div className="flex gap-3">
            <button className="rounded-xl border border-slate-700 bg-slate-900 px-5 py-3 text-white hover:bg-slate-800">
              Refresh
            </button>

            <button className="rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-black hover:bg-cyan-400">
              Scan Tables
            </button>
          </div>
        </div>

        <IcebergStats />

        <IcebergTable
          selectedTable={selectedTable}
          setSelectedTable={setSelectedTable}
        />

        <div className="grid gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <TableDetails
              selectedTable={selectedTable}
            />
          </div>

          <MaintenancePanel />
        </div>
      </div>
    </AppLayout>
  );
}