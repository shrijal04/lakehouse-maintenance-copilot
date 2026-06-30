import AppLayout from "@/components/layout/appLayout";

import MaintenanceCard from "@/components/maintenance/MaintenanceCard";

export default function MaintenancePage() {
  return (
    <AppLayout>
      <div className="space-y-10">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-white">
            Lakehouse Maintenance
          </h1>

          <p className="mt-2 text-slate-400">
            Optimize your Apache Iceberg tables by running maintenance tasks.
          </p>
        </div>

        <MaintenanceCard />
      </div>
    </AppLayout>
  );
}