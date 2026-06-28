import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  sender: "assistant" | "user";
  message: string;
  time: string;
}

export default function ChatMessage({
  sender,
  message,
  time,
}: ChatMessageProps) {
  const isAssistant = sender === "assistant";

  return (
    <div
      className={`mb-6 flex ${
        isAssistant ? "justify-start" : "justify-end"
      }`}
    >
      <div
        className={`flex max-w-3xl gap-4 ${
          isAssistant ? "" : "flex-row-reverse"
        }`}
      >
        {/* Avatar */}
        <div
          className={`flex h-12 w-12 items-center justify-center rounded-full ${
            isAssistant
              ? "bg-cyan-500/20"
              : "bg-violet-500/20"
          }`}
        >
          {isAssistant ? (
            <Bot className="text-cyan-400" size={22} />
          ) : (
            <User className="text-violet-400" size={22} />
          )}
        </div>

        {/* Bubble */}
        <div
          className={`rounded-2xl p-5 shadow-lg ${
            isAssistant
              ? "bg-slate-800"
              : "bg-cyan-500 text-black"
          }`}
        >
          <p
            className={`leading-7 ${
              isAssistant ? "text-slate-200" : ""
            }`}
          >
            {message}
          </p>

          <p
            className={`mt-3 text-xs ${
              isAssistant
                ? "text-slate-500"
                : "text-slate-800"
            }`}
          >
            {time}
          </p>
        </div>
      </div>
    </div>
  );
}