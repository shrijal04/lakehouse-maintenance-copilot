import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string;
  description: string;
  icon: LucideIcon;
}

export default function MetricCard({
  title,
  value,
  description,
  icon: Icon,
}: MetricCardProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5 transition-all duration-300 hover:border-blue-500 hover:shadow-lg hover:shadow-blue-500/10">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">
            {title}
          </p>

          <h2 className="mt-3 text-3xl font-bold text-white">
            {value}
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            {description}
          </p>
        </div>

        <div className="rounded-xl bg-blue-600/20 p-4">
          <Icon className="h-8 w-8 text-blue-400" />
        </div>
      </div>
    </div>
  );
}