"use client";

import { useState } from "react";

import AppLayout from "@/components/layout/appLayout";

import ChatWindow from "@/components/copilot/ChatWindow";
import ChatInput from "@/components/copilot/ChatInput";
import SuggestedPrompts from "@/components/copilot/SuggestedPrompt";

import { initialMessages } from "@/data/copilot";
import { ChatMessageType } from "@/types/chat";

const API =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export default function CopilotPage() {
  const [messages, setMessages] =
    useState<ChatMessageType[]>(initialMessages);

  const [isThinking, setIsThinking] =
    useState(false);

  const sendMessage = async (text: string) => {
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

    try {
      const response = await fetch(
        `${API}/copilot/chat`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get AI response");
      }

      const data = await response.json();

      const aiMessage: ChatMessageType = {
        id: Date.now() + 1,
        sender: "assistant",
        message: data.answer,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);

      const errorMessage: ChatMessageType = {
        id: Date.now() + 1,
        sender: "assistant",
        message:
          "Sorry, I couldn't connect to the AI service. Please try again.",
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        }),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsThinking(false);
    }
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