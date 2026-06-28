import { Recommendation } from "@/types/health";

export const recommendations: Recommendation[] = [
  {
    id: 1,
    title: "Run Snapshot Expiration",
    priority: "High",
  },
  {
    id: 2,
    title: "Compact inventory table",
    priority: "Medium",
  },
  {
    id: 3,
    title: "Clean orphan files",
    priority: "Low",
  },
];