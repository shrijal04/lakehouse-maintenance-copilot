"use client";

import { useEffect, useState } from "react";

import AppLayout from "@/components/layout/appLayout";
import MetricCard from "@/components/dashboard/MetricCard";
import PipelineChart from "@/components/dashboard/PipelineChart";
import RecentJobs from "@/components/dashboard/RecentJobs";
import Recommendations from "@/components/dashboard/Recommendations";
import QuickActions from "@/components/dashboard/QuickActions";
import HealthSummary from "@/components/dashboard/HealthSummary";

import {
  recentJobs,
  recommendations,
} from "@/data/dashboard";

import {
  Database,
  Camera,
  HardDrive,
  HeartPulse,
} from "lucide-react";

import { getDashboardMetrics } from "@/services/dashboard";

export default function DashboardPage() {

  const [metrics, setMetrics] = useState<any[]>([]);
  const [pipeline, setPipeline] = useState<any[]>([]);

  useEffect(() => {

    async function load() {

      try {

        const data = await getDashboardMetrics();

        setMetrics([
          {
            title: "Iceberg Tables",
            value: data.metrics.tables.toString(),
            description: "Managed tables",
            icon: Database,
          },
          {
            title: "Snapshots",
            value: data.metrics.snapshots.toString(),
            description: "Active snapshots",
            icon: Camera,
          },
          {
            title: "Storage Used",
            value: `${data.metrics.storage} MB`,
            description: "Total storage",
            icon: HardDrive,
          },
          {
            title: "Health Score",
            value: `${data.metrics.healthScore}%`,
            description: "Overall lakehouse health",
            icon: HeartPulse,
          },
        ]);

        setPipeline(data.pipelineActivity);

      } catch (error) {

        console.error("Failed to load dashboard.", error);

      }

    }

    load();

  }, []);

  return (
    <AppLayout>

      <div className="space-y-10">

        <div>

          <h1 className="text-4xl font-bold text-white">
            Dashboard
          </h1>

          <p className="mt-2 text-slate-400">
            Monitor your Iceberg lakehouse and maintenance jobs.
          </p>

        </div>

        <div className="grid gap-8 md:grid-cols-2 xl:grid-cols-4">

          {metrics.map((metric) => (

            <MetricCard
              key={metric.title}
              title={metric.title}
              value={metric.value}
              description={metric.description}
              icon={metric.icon}
            />

          ))}

        </div>

        <PipelineChart data={pipeline} />

        <RecentJobs jobs={recentJobs} />

        <Recommendations recommendations={recommendations} />

        <QuickActions />

        <HealthSummary />

      </div>

    </AppLayout>
  );
}