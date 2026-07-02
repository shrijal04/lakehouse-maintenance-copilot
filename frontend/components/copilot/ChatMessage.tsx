import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";

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
          className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full ${
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

        {/* Message Bubble */}
        <div
          className={`rounded-2xl p-5 shadow-lg ${
            isAssistant
              ? "bg-slate-800 text-slate-200"
              : "bg-cyan-500 text-black"
          }`}
        >
          {isAssistant ? (
            <div className="whitespace-pre-wrap break-words">
              <ReactMarkdown
                components={{
                  h1: ({ children }) => (
                    <h1 className="mb-4 text-3xl font-bold text-white">
                      {children}
                    </h1>
                  ),

                  h2: ({ children }) => (
                    <h2 className="mb-3 mt-6 text-2xl font-semibold text-white">
                      {children}
                    </h2>
                  ),

                  h3: ({ children }) => (
                    <h3 className="mb-3 mt-5 text-xl font-semibold text-white">
                      {children}
                    </h3>
                  ),

                  p: ({ children }) => (
                    <p className="mb-4 leading-7 text-slate-200">
                      {children}
                    </p>
                  ),

                  ul: ({ children }) => (
                    <ul className="mb-4 list-disc space-y-2 pl-6 text-slate-200">
                      {children}
                    </ul>
                  ),

                  ol: ({ children }) => (
                    <ol className="mb-4 list-decimal space-y-2 pl-6 text-slate-200">
                      {children}
                    </ol>
                  ),

                  li: ({ children }) => (
                    <li>{children}</li>
                  ),

                  strong: ({ children }) => (
                    <strong className="font-bold text-white">
                      {children}
                    </strong>
                  ),

                  code: ({ children }) => (
                    <code className="rounded bg-slate-700 px-1 py-0.5 font-mono text-cyan-300">
                      {children}
                    </code>
                  ),

                  pre: ({ children }) => (
                    <pre className="mb-4 overflow-x-auto rounded-lg bg-slate-900 p-4">
                      {children}
                    </pre>
                  ),

                  blockquote: ({ children }) => (
                    <blockquote className="my-4 border-l-4 border-cyan-400 pl-4 italic text-slate-300">
                      {children}
                    </blockquote>
                  ),
                }}
              >
                {message}
              </ReactMarkdown>
            </div>
          ) : (
            <p className="whitespace-pre-wrap leading-7">
              {message}
            </p>
          )}

          <p
            className={`mt-4 text-xs ${
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