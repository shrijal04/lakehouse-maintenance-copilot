"use client";

import { useState } from "react";

import AppLayout from "@/components/layout/appLayout";

import { runSimulation } from "@/services/simulation";

import SimulationHeader from "@/components/simulation/SimulationHeader";
import SimulationControls from "@/components/simulation/SimulationControls";
import SimulationStatus from "@/components/simulation/SimulationStatus";
import SimulationTimeline from "@/components/simulation/SimulationTimeline";
import SimulationLogs from "@/components/simulation/SimulationLogs";

export interface SimulationResponse {
  status: string;
  conflict: boolean;
  message: string;
  logs: string[];
  sessionA: string;
  sessionB: string;
}

export default function SimulationPage() {
  const [loading, setLoading] = useState(false);

  const [result, setResult] =
    useState<SimulationResponse | null>(null);

  const startSimulation = async () => {
    try {
      setLoading(true);
      setResult(null);

      const data = await runSimulation();

      setResult(data);
    } catch (error) {
      console.error(error);

      setResult({
        status: "failed",
        conflict: false,
        message: "Unable to connect to backend.",
        logs: ["Connection failed."],
        sessionA: "-",
        sessionB: "-",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout>

      <div className="space-y-8">

        <SimulationHeader />

        <SimulationControls
          loading={loading}
          onRun={startSimulation}
        />

        <SimulationStatus
          loading={loading}
          result={result}
        />

        <SimulationTimeline
          loading={loading}
          result={result}
        />

        <SimulationLogs
          logs={result?.logs ?? []}
        />

      </div>

    </AppLayout>
  );
}