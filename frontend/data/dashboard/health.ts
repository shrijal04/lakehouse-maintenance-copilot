import {
  CheckCircle,
  AlertTriangle,
  Database,
} from "lucide-react";
{}
export const healthSummary = [
  {
    id: 1,
    title: "Healthy Tables",
    value: 21,
    color: "text-green-400",
    icon: CheckCircle,
  },
  {
    id: 2,
    title: "Warnings",
    value: 2,
    color: "text-yellow-400",
    icon: AlertTriangle,
  },
  {
    id: 3,
    title: "Maintenance Pending",
    value: 1,
    color: "text-blue-400",
    icon: Database,
  },
];