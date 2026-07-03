import { Bot, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
        className={`flex max-w-4xl gap-4 ${
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
            <Bot
              className="text-cyan-400"
              size={22}
            />
          ) : (
            <User
              className="text-violet-400"
              size={22}
            />
          )}
        </div>

        {/* Bubble */}
        <div
          className={`rounded-2xl p-5 shadow-lg ${
            isAssistant
              ? "bg-slate-800 text-slate-200"
              : "bg-cyan-500 text-black"
          }`}
        >
          {isAssistant ? (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => (
                  <h1 className="mb-4 text-3xl font-bold text-white">
                    {children}
                  </h1>
                ),

                h2: ({ children }) => (
                  <h2 className="mt-6 mb-3 text-2xl font-semibold text-white">
                    {children}
                  </h2>
                ),

                h3: ({ children }) => (
                  <h3 className="mt-5 mb-3 text-xl font-semibold text-white">
                    {children}
                  </h3>
                ),

                p: ({ children }) => (
                  <p className="mb-4 leading-7 text-slate-200">
                    {children}
                  </p>
                ),

                ul: ({ children }) => (
                  <ul className="mb-4 list-disc space-y-2 pl-6">
                    {children}
                  </ul>
                ),

                ol: ({ children }) => (
                  <ol className="mb-4 list-decimal space-y-2 pl-6">
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

                hr: () => (
                  <hr className="my-6 border-slate-600" />
                ),

                table: ({ children }) => (
                  <div className="my-6 overflow-x-auto rounded-lg border border-slate-700">
                    <table className="min-w-full border-collapse">
                      {children}
                    </table>
                  </div>
                ),

                thead: ({ children }) => (
                  <thead className="bg-slate-900">
                    {children}
                  </thead>
                ),

                tbody: ({ children }) => (
                  <tbody className="divide-y divide-slate-700">
                    {children}
                  </tbody>
                ),

                tr: ({ children }) => (
                  <tr className="hover:bg-slate-700/30">
                    {children}
                  </tr>
                ),

                th: ({ children }) => (
                  <th className="border border-slate-700 px-4 py-3 text-left font-semibold text-cyan-300">
                    {children}
                  </th>
                ),

                td: ({ children }) => (
                  <td className="border border-slate-700 px-4 py-3 text-slate-200">
                    {children}
                  </td>
                ),
              }}
            >
              {message}
            </ReactMarkdown>
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