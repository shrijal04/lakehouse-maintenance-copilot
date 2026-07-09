interface SimulationLogsProps {
  logs: string[];
}

export default function SimulationLogs({
  logs,
}: SimulationLogsProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900">

      {/* Header */}

      <div className="border-b border-slate-800 p-5">

        <h2 className="text-xl font-semibold text-white">
          Simulation Logs
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Live output from both Spark sessions.
        </p>

      </div>

      {/* Terminal */}

      <div
        className="
          h-[420px]
          overflow-y-auto
          bg-[#0d1117]
          p-5
          font-mono
          text-sm
        "
      >

        {logs.length === 0 ? (

          <div className="text-slate-500">
            Waiting for simulation...
          </div>

        ) : (

          logs.map((log, index) => {

            let color = "text-green-400";

            if (
              log.toLowerCase().includes("error") ||
              log.toLowerCase().includes("failed") ||
              log.toLowerCase().includes("conflict")
            ) {
              color = "text-red-400";
            } else if (
              log.toLowerCase().includes("sleep") ||
              log.toLowerCase().includes("reading") ||
              log.toLowerCase().includes("trying")
            ) {
              color = "text-yellow-400";
            } else if (
              log.toLowerCase().includes("committed") ||
              log.toLowerCase().includes("success")
            ) {
              color = "text-green-400";
            }

            return (
              <div
                key={index}
                className={`${color} mb-2 break-words`}
              >
                <span className="mr-2 text-slate-600">$</span>
                {log}
              </div>
            );
          })

        )}

      </div>

    </div>
  );
}