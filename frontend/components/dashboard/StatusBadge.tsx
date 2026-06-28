interface Props {
  status: string;
}

export default function StatusBadge({ status }: Props) {
  const styles = {
    Success: "bg-green-500/20 text-green-400",
    Running: "bg-yellow-500/20 text-yellow-400",
    Failed: "bg-red-500/20 text-red-400",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ${
        styles[status as keyof typeof styles]
      }`}
    >
      {status}
    </span>
  );
}