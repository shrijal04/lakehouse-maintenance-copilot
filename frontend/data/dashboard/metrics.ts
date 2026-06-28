import {
  Database,
  Camera,
  HardDrive,
  HeartPulse,
} from "lucide-react";

export const metrics = [
  {
    title: "Iceberg Tables",
    value: "24",
    description: "Managed tables",
    icon: Database,
  },
  {
    title: "Snapshots",
    value: "138",
    description: "Active snapshots",
    icon: Camera,
  },
  {
    title: "Storage Used",
    value: "1.8 TB",
    description: "Total storage",
    icon: HardDrive,
  },
  {
    title: "Health Score",
    value: "98%",
    description: "Overall lakehouse health",
    icon: HeartPulse,
  },
];