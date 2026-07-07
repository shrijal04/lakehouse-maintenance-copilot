"use client";

import { useEffect, useState } from "react";

import AppLayout from "@/components/layout/appLayout";

import HealthScore from "@/components/health/HealthScore";
import HealthCards from "@/components/health/HealthCards";
import HealthTrend from "@/components/health/HealthTrend";
import StorageMetadata from "@/components/health/StoreMetadata";
import IssuesTable from "@/components/health/IssuesTable";

import Overlay from "@/components/LoadingOverlay";

export default function HealthPage() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadPage() {
      try {
        // Give child components time to fetch their data.
        // Remove this timeout later if you centralize loading.
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
      {loading && <Overlay />}

      <AppLayout>
        <div className="space-y-10">
          {/* Header */}
          <div>
            <h1 className="text-4xl font-bold text-white">
              Lakehouse Health
            </h1>

            <p className="mt-2 text-slate-400">
              Monitor the overall health of your Iceberg lakehouse.
            </p>
          </div>

          {/* Overall Health Score */}
          <HealthScore />

          {/* Health Metrics */}
          <HealthCards />

          {/* Orders Trend */}
          <HealthTrend
            database="silver"
            table="orders"
            title="Orders File Count Trend"
          />

          {/* Order Items Trend */}
          <HealthTrend
            database="silver"
            table="order_items"
            title="Order Items File Count Trend"
          />

          {/* Storage & Metadata */}
          <StorageMetadata />

          {/* Active Issues */}
          <div className="grid gap-8 lg:grid-cols-12">
            <div className="lg:col-span-12">
              <IssuesTable />
            </div>
          </div>
        </div>
      </AppLayout>
    </>
  );
}