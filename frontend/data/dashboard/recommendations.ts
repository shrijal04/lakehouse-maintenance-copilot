import {
  Database,
  Camera,
  HardDrive,
  HeartPulse,
} from "lucide-react";

export const recommendations = [
  {
    id: 1,
    title: "Optimize Orders Table",
    description:
      "The Orders table has accumulated many small files. Running OPTIMIZE can improve query performance.",
    priority: "High",
  },
  {
    id: 2,
    title: "Expire Old Snapshots",
    description:
      "138 snapshots detected. Remove snapshots older than 30 days to save storage.",
    priority: "Medium",
  },
  {
    id: 3,
    title: "Rewrite Manifests",
    description:
      "Manifest files are outdated and should be rewritten for faster metadata access.",
    priority: "Low",
  },
];
