import { pipelineMetrics } from "@/data/pipeline";

export default function PipelineStats() {
  return (
    <div className="grid gap-6 md:grid-cols-4">
      {pipelineMetrics.map((item) => (
        <div
          key={item.id}
          className="rounded-2xl border border-slate-800 bg-slate-900 p-6"
        >
          <p className="text-slate-400">{item.title}</p>

          <h2 className="mt-4 text-4xl font-bold text-white">
            {item.value}
          </h2>
        </div>
      ))}
    </div>
  );
}