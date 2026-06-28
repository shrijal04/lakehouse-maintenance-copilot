"use client";

import { useState } from "react";

import AppLayout from "@/components/layout/appLayout";

import ChatWindow from "@/components/copilot/ChatWindow";
import ChatInput from "@/components/copilot/ChatInput";
import SuggestedPrompts from "@/components/copilot/SuggestedPrompt";

import { initialMessages } from "@/data/copilot";
import { ChatMessageType } from "@/types/chat";

export default function CopilotPage() {
  const [messages, setMessages] =
    useState<ChatMessageType[]>(initialMessages);

  const [isThinking, setIsThinking] =
    useState(false);

  const sendMessage = (text: string) => {
    if (!text.trim()) return;

    const newMessage: ChatMessageType = {
      id: Date.now(),
      sender: "user",
      message: text,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, newMessage]);

    setIsThinking(true);

    setTimeout(() => {
      const aiMessage: ChatMessageType = {
        id: Date.now() + 1,
        sender: "assistant",
        message:
          "This is a mock AI response. Later this will come from FastAPI + OpenAI.",
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, aiMessage]);

      setIsThinking(false);
    }, 1500);
  };

  return (
    <AppLayout>
      <div className="mx-auto max-w-6xl space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-white">
            Lakehouse Maintenance Copilot
          </h1>

          <p className="mt-2 text-slate-400">
            Ask anything about your Iceberg lakehouse.
          </p>
        </div>

        {/* Chat Window */}
        <ChatWindow
          messages={messages}
          isThinking={isThinking}
        />

        {/* Suggested Prompts */}
        <SuggestedPrompts
          onSelect={sendMessage}
        />

        {/* Chat Input */}
        <ChatInput
          onSend={sendMessage}
        />
      </div>
    </AppLayout>
  );
}