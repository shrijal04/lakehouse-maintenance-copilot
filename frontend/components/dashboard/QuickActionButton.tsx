import { ArrowRight } from "lucide-react";

interface Props {
  title: string;
  description: string;
}

export default function QuickActionButton({
  title,
  description,
}: Props) {
  return (
    <button
      className="
      w-full
      rounded-xl
      border
      border-slate-800
      bg-slate-900
      p-5
      text-left
      transition-all
      duration-300
      hover:border-blue-500
      hover:bg-slate-800
      "
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-white font-semibold">
            {title}
          </h3>

          <p className="text-slate-400 text-sm mt-2">
            {description}
          </p>
        </div>

        <ArrowRight className="text-blue-400" />
      </div>
    </button>
  );
}