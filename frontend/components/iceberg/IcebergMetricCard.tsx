import { LucideIcon } from "lucide-react";

interface IcebergMetricCardProps {
  title: string;
  value: string | number;
  description: string;
  icon: LucideIcon;
}

export default function IcebergMetricCard({
  title,
  value,
  description,
  icon: Icon,
}: IcebergMetricCardProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 transition-all hover:border-cyan-500 hover:shadow-lg hover:shadow-cyan-500/10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">
            {title}
          </p>

          <h2 className="mt-2 text-3xl font-bold text-white">
            {value}
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            {description}
          </p>
        </div>

        <div className="rounded-xl bg-cyan-500/10 p-3">
          <Icon className="text-cyan-400" size={28} />
        </div>
      </div>
    </div>
  );
}