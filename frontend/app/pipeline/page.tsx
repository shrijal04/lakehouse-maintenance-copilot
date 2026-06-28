import AppLayout from "@/components/layout/appLayout";

import PipelineStats from "@/components/pipeline/PipelineStats";
import JobTable from "@/components/pipeline/JobTable";
import PipelineTimeline from "@/components/pipeline/PipelineTimeline";
import PipelineHealth from "@/components/pipeline/PipelineHealth";
import PipelineFlow from "@/components/pipeline/PipelineFlow";

export default function PipelinePage() {
  return (
    <AppLayout>
      <div className="space-y-10">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white">
              Pipeline Operations
            </h1>

            <p className="mt-2 text-slate-400 text-lg">
              Monitor ETL pipelines and Iceberg maintenance workflows.
            </p>
          </div>

          <div className="flex gap-3">
            <button className="rounded-xl border border-slate-700 bg-slate-900 px-5 py-3 text-white transition hover:bg-slate-800">
              Refresh
            </button>

            <button className="rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-black transition hover:bg-cyan-400">
              Run Maintenance
            </button>
          </div>
        </div>

        <PipelineStats />

        <JobTable />

        <div className="grid gap-8 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <PipelineTimeline />
          </div>

          <PipelineHealth />
        </div>

        <PipelineFlow />

      </div>
    </AppLayout>
  );
}