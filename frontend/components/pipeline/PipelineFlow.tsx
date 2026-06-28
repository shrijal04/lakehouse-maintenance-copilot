import { ArrowRight } from "lucide-react";

import { workflowSteps } from "@/data/pipeline";

export default function PipelineFlow() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

      <h2 className="mb-8 text-xl font-semibold text-white">
        ETL Workflow
      </h2>

      <div className="flex flex-wrap items-center justify-between gap-4">

        {workflowSteps.map((step, index) => (
          <div
            key={step.name}
            className="flex items-center"
          >
            <div className="rounded-xl bg-slate-800 px-8 py-6 text-center">

              <p className="font-semibold text-white">
                {step.name}
              </p>

            </div>

            {index !== workflowSteps.length - 1 && (
              <ArrowRight
                className="mx-4 text-slate-500"
              />
            )}

          </div>
        ))}

      </div>

    </div>
  );
}