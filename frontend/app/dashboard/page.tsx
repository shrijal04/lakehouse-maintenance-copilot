import AppLayout from "@/components/layout/appLayout";
import MetricCard from "@/components/dashboard/MetricCard";
import { metrics, pipelineActivity, recentJobs,recommendations, } from "@/data/dashboard";
import PipelineChart from "@/components/dashboard/PipelineChart";
import RecentJobs from "@/components/dashboard/RecentJobs";
import Recommendations from "@/components/dashboard/Recommendations";
import QuickActions from "@/components/dashboard/QuickActions";
import HealthSummary from "@/components/dashboard/HealthSummary";

export default function DashboardPage() {
  return (
    <AppLayout>
      <div className="space-y-10">
        <div>
          <h1 className="text-4xl font-bold text-white">
            Dashboard
          </h1>

          <p className="mt-2 text-slate-400">
            Monitor your Iceberg lakehouse and maintenance jobs.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-4">
          {metrics.map((metric) => (
            <MetricCard
              key={metric.title}
              title={metric.title}
              value={metric.value}
              description={metric.description}
              icon={metric.icon}
            />
            
          ))}
        </div>
        <PipelineChart data={pipelineActivity}/>
        <RecentJobs jobs={recentJobs} />
        <Recommendations recommendations={recommendations} />
        <QuickActions />
        <HealthSummary />
      </div>
    </AppLayout>
  );
}