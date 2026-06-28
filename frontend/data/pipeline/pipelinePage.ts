export const pipelineStats = [
  {
    id: 1,
    title: "Running Jobs",
    value: 3,
  },
  {
    id: 2,
    title: "Queued",
    value: 4,
  },
  {
    id: 3,
    title: "Completed Today",
    value: 18,
  },
  {
    id: 4,
    title: "Failed",
    value: 1,
  },
];

export const jobs = [
  {
    id: 101,
    name: "Daily Snapshot Cleanup",
    status: "Running",
    duration: "5m",
    lastRun: "10:20 AM",
  },
  {
    id: 102,
    name: "Compaction",
    status: "Completed",
    duration: "12m",
    lastRun: "9:30 AM",
  },
  {
    id: 103,
    name: "Orphan File Removal",
    status: "Queued",
    duration: "--",
    lastRun: "--",
  },
  {
    id: 104,
    name: "Metadata Refresh",
    status: "Failed",
    duration: "3m",
    lastRun: "Yesterday",
  },
];