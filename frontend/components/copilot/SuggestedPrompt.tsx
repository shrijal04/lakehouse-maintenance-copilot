import { Sparkles } from "lucide-react";

import { suggestedPrompts } from "@/data/copilot";

interface Props {
  onSelect: (text: string) => void;
}

export default function SuggestedPrompts({
  onSelect,
}: Props) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-5 flex items-center gap-3">
        <Sparkles className="text-cyan-400" />

        <h2 className="text-xl font-semibold text-white">
          Suggested Prompts
        </h2>
      </div>

      <div className="flex flex-wrap gap-3">
        {suggestedPrompts.map((prompt) => (
          <button
            key={prompt.id}
            onClick={() => onSelect(prompt.text)}
            className="rounded-full border border-slate-700 bg-slate-800 px-5 py-2 text-sm text-slate-300 transition hover:border-cyan-500 hover:bg-cyan-500/10 hover:text-cyan-300"
          >
            {prompt.text}
          </button>
        ))}
      </div>
    </div>
  );
}