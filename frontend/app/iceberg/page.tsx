"use client";

import { useState } from "react";

import AppLayout from "@/components/layout/appLayout";

import IcebergStats from "@/components/iceberg/IcebergStats";
import IcebergTable from "@/components/iceberg/IcebergTable";
import TableDetails from "@/components/iceberg/TableDetails";
import MaintenancePanel from "@/components/iceberg/MaintenancePanel";

import { TableName } from "@/types/iceberg";

export default function IcebergPage() {
  const [selectedTable, setSelectedTable] =
    useState<TableName>("orders");

  return (
    <AppLayout>
      <div className="space-y-10">
        <div>
          <h1 className="text-4xl font-bold text-white">
            Iceberg Catalog
          </h1>

          <p className="mt-2 text-lg text-slate-400">
            Browse Apache Iceberg tables and inspect their storage,
            metadata, and health.
          </p>
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