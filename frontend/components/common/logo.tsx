import { DatabaseZap } from "lucide-react";

export default function Logo() {
  return (
    <div className="flex items-center gap-3 px-2">
      <div className="rounded-xl bg-blue-600 p-2">
        <DatabaseZap className="h-6 w-6 text-white" />
      </div>

      <div>
        <h1 className="text-lg font-bold tracking-tight text-white">
          Lakehouse
        </h1>

        <p className="text-xs text-slate-400">
          Maintenance Copilot
        </p>
      </div>
    </div>
  );
}