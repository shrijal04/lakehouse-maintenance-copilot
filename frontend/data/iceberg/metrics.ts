import {
  Database,
  HardDrive,
  AlertTriangle,
  CheckCircle,
} from "lucide-react";

export const icebergMetrics = [
  {
    id: 1,
    title: "Total Tables",
    value: 24,
    description: "Iceberg tables",
    icon: Database,
  },
  {
    id: 2,
    title: "Healthy",
    value: 21,
    description: "Tables in good condition",
    icon: CheckCircle,
  },
  {
    id: 3,
    title: "Needs Maintenance",
    value: 3,
    description: "Optimization required",
    icon: AlertTriangle,
  },
  {
    id: 4,
    title: "Storage Used",
    value: "145 GB",
    description: "Total storage",
    icon: HardDrive,
  },
];