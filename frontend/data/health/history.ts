import { MaintenanceHistory } from "@/types/health";

export const maintenanceHistory: MaintenanceHistory[] = [
  {
    id: 1,
    job: "Optimize inventory",
    status: "Completed",
    time: "Today",
  },
  {
    id: 2,
    job: "Expire Snapshots",
    status: "Completed",
    time: "Yesterday",
  },
  {
    id: 3,
    job: "Remove Orphan Files",
    status: "Completed",
    time: "2 days ago",
  },
];