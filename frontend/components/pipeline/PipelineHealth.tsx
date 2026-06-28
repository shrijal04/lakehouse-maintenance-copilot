import { pipelineHealth } from "@/data/pipeline";

export default function PipelineHealth() {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <h2 className="mb-6 text-xl font-semibold text-white">
        Pipeline Health
      </h2>

      <div className="space-y-6">
        {pipelineHealth.map((item) => (
          <div key={item.id}>
            <div className="mb-2 flex justify-between">
              <span className="text-slate-300">
                {item.title}
              </span>

              <span
                className={`${item.textColor} font-semibold`}
              >
                {item.percentage}%
              </span>
            </div>

            <div className="h-3 rounded-full bg-slate-700">
              <div
                className={`h-3 rounded-full ${item.color}`}
                style={{
                  width: `${item.percentage}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}