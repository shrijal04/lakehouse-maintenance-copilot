import { ChatMessageType } from "@/types/chat";

export const initialMessages: ChatMessageType[] = [
  {

  id: 1,
  sender: "assistant",
  message:
    "👋 Welcome to the Lakehouse Maintenance Copilot.\n\nI can help you:\n\n• Explain Apache Iceberg concepts\n• Analyze table health\n• Recommend maintenance operations\n• Interpret snapshots, manifests, and orphan files\n• Answer Spark and data lake questions\n\nWhat would you like to know?",
  time: new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  }),
}
  
];