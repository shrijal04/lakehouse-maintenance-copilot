import { Bot } from "lucide-react";

export default function TypingIndicator() {
  return (
    <div className="mt-6 flex items-center gap-4">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-cyan-500/20">
        <Bot className="text-cyan-400" size={22} />
      </div>

      <div className="rounded-2xl bg-slate-800 px-5 py-4">
        <div className="flex gap-2">
          <div className="h-2 w-2 animate-bounce rounded-full bg-cyan-400"></div>
          <div className="h-2 w-2 animate-bounce rounded-full bg-cyan-400 [animation-delay:0.15s]"></div>
          <div className="h-2 w-2 animate-bounce rounded-full bg-cyan-400 [animation-delay:0.3s]"></div>
        </div>

        <p className="mt-2 text-xs text-slate-400">
          Copilot is thinking...
        </p>
      </div>
    </div>
  );
}