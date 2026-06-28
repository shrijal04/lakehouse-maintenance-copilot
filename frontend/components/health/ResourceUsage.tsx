import { resources } from "@/data/health";

export default function ResourceUsage() {
  const bars = [
    {
      title: "CPU",
      value: resources.cpu,
    },
    {
      title: "Memory",
      value: resources.memory,
    },
    {
      title: "Disk",
      value: resources.disk,
    },
  ];

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">

      <h2 className="mb-6 text-2xl font-semibold text-white">
        Cluster Resources
      </h2>

      <div className="space-y-6">

        {bars.map((bar) => (

          <div key={bar.title}>

            <div className="mb-2 flex justify-between">

              <span className="text-white">
                {bar.title}
              </span>

              <span className="text-cyan-400">
                {bar.value}%
              </span>

            </div>

            <div className="h-3 rounded-full bg-slate-700">

              <div
                className="h-3 rounded-full bg-cyan-500"
                style={{
                  width: `${bar.value}%`,
                }}
              />

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}