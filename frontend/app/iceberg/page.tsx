"use client";

import { useEffect, useState } from "react";

import AppLayout from "@/components/layout/appLayout";

import IcebergStats from "@/components/iceberg/IcebergStats";
import IcebergTable from "@/components/iceberg/IcebergTable";
import TableDetails from "@/components/iceberg/TableDetails";
import MaintenancePanel from "@/components/iceberg/MaintenancePanel";

import LoadingOverlay from "@/components/LoadingOverlay";

import { TableName } from "@/types/iceberg";

export default function IcebergPage() {
  const [loading, setLoading] = useState(true);

  const [selectedTable, setSelectedTable] =
    useState<TableName>("orders");

  useEffect(() => {
    async function loadPage() {
      try {
        // Temporary loading overlay
        // Remove this later when using real loading state
        await new Promise((resolve) =>
          setTimeout(resolve, 1200)
        );
      } finally {
        setLoading(false);
      }
    }

    loadPage();
  }, []);

  return (
    <>
      {loading && <LoadingOverlay />}

      <AppLayout>
        <div className="space-y-10">
          <div>
            <h1 className="text-4xl font-bold text-white">
              Iceberg Catalog
            </h1>

            <p className="mt-2 text-lg text-slate-400">
              Browse Apache Iceberg tables and inspect their
              storage, metadata, and health.
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
    </>
  );
}