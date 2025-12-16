"use client";

import { ChatMessage } from "./ChatMessage";
import { Loader2, ChefHat, Sparkles } from "lucide-react";

interface Message {
  id: number;
  role: "user" | "assistant";
  type?: "text" | "recipe" | "nutrition" | "video" | "image";
  content?: string;
  recipe?: any;
  nutrition?: any;
  video?: any;
  imageUrl?: string;
}

interface ChatMessagesProps {
  messages: Message[];
  isLoading?: boolean;
  onSuggestedQuery?: (query: string) => void;
}

export function ChatMessages({ messages, isLoading = false, onSuggestedQuery }: ChatMessagesProps) {
  return (
    <div className="flex-1 overflow-y-auto overflow-x-hidden min-h-0">
      <div className="max-w-3xl mx-auto w-full px-4 py-8 space-y-6">
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full min-h-[400px] text-center space-y-6">
            <div className="relative">
              <ChefHat className="h-20 w-20 text-muted-foreground/40" />
              <Sparkles className="h-8 w-8 text-primary absolute -top-2 -right-2" />
            </div>
            <div className="space-y-2">
              <h2 className="text-2xl font-semibold">Chào mừng đến với Meal RAG Chat AI</h2>
              <p className="text-muted-foreground max-w-md">
                Hỏi tôi về bất kỳ công thức nấu ăn nào! Tôi có thể giúp bạn tìm món ăn,
                nguyên liệu, hướng dẫn nấu ăn và video hướng dẫn.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl mt-8">
              <div
                className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
                onClick={() => onSuggestedQuery?.("Tìm món pasta Ý cho tôi")}
              >
                <p className="text-sm">🍝 "Tìm món pasta Ý cho tôi"</p>
              </div>
              <div
                className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
                onClick={() => onSuggestedQuery?.("Món gà nướng ngon nhất")}
              >
                <p className="text-sm">🍗 "Món gà nướng ngon nhất"</p>
              </div>
              <div
                className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
                onClick={() => onSuggestedQuery?.("Món ăn chay healthy")}
              >
                <p className="text-sm">🥗 "Món ăn chay healthy"</p>
              </div>
              <div
                className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors cursor-pointer"
                onClick={() => onSuggestedQuery?.("Cách làm bánh ngọt")}
              >
                <p className="text-sm">🍰 "Cách làm bánh ngọt"</p>
              </div>
            </div>
          </div>
        )}

        {messages.map((msg, index) => {
          // Check if this is the first message from assistant in a group
          const isFirstInGroup =
            msg.role === "assistant" &&
            (index === 0 || messages[index - 1].role !== "assistant");

          return (
            <ChatMessage
              key={msg.id}
              message={msg}
              isFirstInGroup={isFirstInGroup}
            />
          );
        })}

        {isLoading && (
          <div className="flex gap-4">
            <div className="w-8 shrink-0"></div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="text-sm">Đang suy nghĩ...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

