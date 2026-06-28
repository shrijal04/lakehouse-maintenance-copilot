import { HealthMetric } from "@/types/health";

export const healthMetrics: HealthMetric[] = [
  {
    id: 1,
    title: "Healthy Tables",
    value: 21,
    description: "Operating normally",
    color: "green",
  },
  {
    id: 2,
    title: "Warnings",
    value: 2,
    description: "Need attention",
    color: "yellow",
  },
  {
    id: 3,
    title: "Critical",
    value: 1,
    description: "Immediate action",
    color: "red",
  },
  {
    id: 4,
    title: "Maintenance Jobs",
    value: 43,
    description: "Completed today",
    color: "cyan",
  },
];