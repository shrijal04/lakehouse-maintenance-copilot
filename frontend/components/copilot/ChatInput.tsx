"use client";

import { useState } from "react";

import {
  Paperclip,
  Mic,
  SendHorizontal,
} from "lucide-react";

interface Props {
  onSend: (text: string) => void;
}

export default function ChatInput({
  onSend,
}: Props) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;

    onSend(text);

    setText("");
  };

  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-5">
      <div className="flex items-center gap-4">
        <button className="rounded-xl p-3 text-slate-400 hover:bg-slate-800">
          <Paperclip size={20} />
        </button>

        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) =>
            e.key === "Enter" && handleSend()
          }
          placeholder="Ask your Lakehouse Copilot..."
          className="flex-1 bg-transparent text-white outline-none placeholder:text-slate-500"
        />

        <button className="rounded-xl p-3 text-slate-400 hover:bg-slate-800">
          <Mic size={20} />
        </button>

        <button
          onClick={handleSend}
          className="rounded-xl bg-cyan-500 p-3 text-black hover:bg-cyan-400"
        >
          <SendHorizontal size={20} />
        </button>
      </div>
    </div>
  );
}