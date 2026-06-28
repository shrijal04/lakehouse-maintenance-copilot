import ChatMessage from "./ChatMessage";
import TypingIndicator from "./TypingIndicator";

import { ChatMessageType } from "@/types/chat";

interface Props {
  messages: ChatMessageType[];
  isThinking: boolean;
}

export default function ChatWindow({
  messages,
  isThinking,
}: Props) {
  return (
    <div className="h-[550px] overflow-y-auto rounded-3xl border border-slate-800 bg-slate-900 p-8">
      {messages.map((msg) => (
        <ChatMessage
          key={msg.id}
          sender={msg.sender}
          message={msg.message}
          time={msg.time}
        />
      ))}

      {isThinking && <TypingIndicator />}
    </div>
  );
}