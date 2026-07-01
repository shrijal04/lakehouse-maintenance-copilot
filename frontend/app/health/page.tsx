import AppLayout from "@/components/layout/appLayout";

import HealthScore from "@/components/health/HealthScore";
import HealthCards from "@/components/health/HealthCards";
import HealthTrend from "@/components/health/HealthTrend";
import StorageMetadata from "@/components/health/StoreMetadata";
import IssuesTable from "@/components/health/IssuesTable";



export default function HealthPage() {
  return (
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

        <HealthScore />

        <HealthCards />

        <HealthTrend
            table="orders"
            title="Orders File Count Trend"
        />

        <HealthTrend
            table="order-items"
            title="Order Items File Count Trend"
        />

        <StorageMetadata />

        {/* Issues + Resources */}
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-8">
            <IssuesTable />
          </div>


        </div>

      </div>
    </AppLayout>
  );
}