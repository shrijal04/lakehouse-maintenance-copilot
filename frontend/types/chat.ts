export interface ChatMessageType {
  id: number;

  sender: "user" | "assistant";

  message: string;

  time: string;

  pdf?: string;

  docx?: string;
}