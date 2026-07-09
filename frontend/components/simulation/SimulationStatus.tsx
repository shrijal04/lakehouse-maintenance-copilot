import {
  AlertCircle,
  CheckCircle2,
  Clock,
} from "lucide-react";

import { SimulationResponse } from "@/app/simulation/page";

interface SimulationStatusProps {
  loading: boolean;
  result: SimulationResponse | null;
}

export default function SimulationStatus({
  loading,
  result,
}: SimulationStatusProps) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">

      {/* Status Card */}

      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <h2 className="mb-6 text-xl font-semibold text-white">
          Simulation Status
        </h2>

        {loading ? (

          <div className="flex items-center gap-3 text-yellow-400">

            <Clock className="h-6 w-6 animate-pulse" />

            <span className="text-lg font-semibold">
              Simulation Running...
            </span>

          </div>

        ) : result ? (

          result.conflict ? (

            <div className="flex items-center gap-3 text-red-400">

              <AlertCircle className="h-6 w-6" />

              <span className="text-lg font-semibold">
                OCC Conflict Detected
              </span>

            </div>

          ) : (

            <div className="flex items-center gap-3 text-green-400">

              <CheckCircle2 className="h-6 w-6" />

              <span className="text-lg font-semibold">
                Simulation Completed Successfully
              </span>

            </div>

          )

        ) : (

          <p className="text-slate-400">
            Click <strong>Run Simulation</strong> to start.
          </p>

        )}

      </div>

      {/* Result Card */}

      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

        <h2 className="mb-6 text-xl font-semibold text-white">
          Result
        </h2>

        {result ? (

          <div className="space-y-5">

            {/* Session A */}

            <div className="flex items-center justify-between rounded-xl border border-slate-700 bg-slate-800 p-4">

              <span className="font-medium text-white">
                Session A
              </span>

              <span
                className={`rounded-full px-4 py-1 text-sm font-semibold ${
                  result.sessionA === "Committed"
                    ? "bg-green-500/20 text-green-400"
                    : "bg-red-500/20 text-red-400"
                }`}
              >
                {result.sessionA}
              </span>

            </div>

            {/* Session B */}

            <div className="flex items-center justify-between rounded-xl border border-slate-700 bg-slate-800 p-4">

              <span className="font-medium text-white">
                Session B
              </span>

              <span
                className={`rounded-full px-4 py-1 text-sm font-semibold ${
                  result.sessionB === "Committed"
                    ? "bg-green-500/20 text-green-400"
                    : "bg-red-500/20 text-red-400"
                }`}
              >
                {result.sessionB}
              </span>

            </div>

            {/* Message */}

            <div className="rounded-xl border border-slate-700 bg-slate-800 p-4">

              <h3 className="mb-2 font-semibold text-white">
                Message
              </h3>

              <p className="text-slate-300">
                {result.message}
              </p>

            </div>

          </div>

        ) : (

          <p className="text-slate-400">
            Run the simulation to see the result.
          </p>

        )}

      </div>

    </div>
  );
}