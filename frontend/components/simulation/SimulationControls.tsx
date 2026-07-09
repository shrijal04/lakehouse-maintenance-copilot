"use client";

import { Loader2, Play } from "lucide-react";

interface SimulationControlsProps {
  loading: boolean;
  onRun: () => void;
}

export default function SimulationControls({
  loading,
  onRun,
}: SimulationControlsProps) {
  return (
    <div className="flex justify-end">

      <button
        onClick={onRun}
        disabled={loading}
        className="
          flex
          items-center
          gap-2
          rounded-xl
          bg-blue-600
          px-6
          py-3
          font-semibold
          text-white
          shadow-lg
          transition-all
          duration-200
          hover:bg-blue-700
          hover:scale-[1.02]
          disabled:cursor-not-allowed
          disabled:opacity-60
        "
      >
        {loading ? (
          <>
            <Loader2 className="h-5 w-5 animate-spin" />
            Running Simulation...
          </>
        ) : (
          <>
            <Play className="h-5 w-5" />
            Run Simulation
          </>
        )}
      </button>

    </div>
  );
}