export interface ChatMessageType {
  id: number;
  sender: "assistant" | "user";
  message: string;
  time: string;
}