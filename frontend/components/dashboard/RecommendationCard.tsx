import { Sparkles } from "lucide-react";

interface Props {
  title: string;
  description: string;
  priority: string;
}

export default function RecommendationCard({
  title,
  description,
  priority,
}: Props) {
  const colors = {
    High: "text-red-400",
    Medium: "text-yellow-400",
    Low: "text-green-400",
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-5 hover:border-blue-500 transition">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Sparkles className="text-blue-400" size={18} />
          <h3 className="font-semibold text-white">
            {title}
          </h3>
        </div>

        <span
          className={`text-sm font-semibold ${
            colors[priority as keyof typeof colors]
          }`}
        >
          {priority}
        </span>
      </div>

      <p className="text-slate-400 text-sm leading-6">
        {description}
      </p>
    </div>
  );
}