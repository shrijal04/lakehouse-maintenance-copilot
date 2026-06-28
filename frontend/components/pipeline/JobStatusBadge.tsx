interface Props {
  status: string;
}

export default function JobStatusBadge({ status }: Props) {
  const colors = {
    Running: "bg-blue-500/20 text-blue-400",
    Completed: "bg-green-500/20 text-green-400",
    Queued: "bg-yellow-500/20 text-yellow-400",
    Failed: "bg-red-500/20 text-red-400",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-sm ${
        colors[status as keyof typeof colors]
      }`}
    >
      {status}
    </span>
  );
}