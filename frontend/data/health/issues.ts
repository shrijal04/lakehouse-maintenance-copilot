import { Issue } from "@/types/health";

export const issues: Issue[] = [
  {
    id: 1,
    table: "inventory",
    severity: "Critical",
    issue: "Too many small files",
    action: "Optimize",
  },
  {
    id: 2,
    table: "sales_orders",
    severity: "Warning",
    issue: "Old snapshots",
    action: "Expire",
  },
];