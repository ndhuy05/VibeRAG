"use client";

import { ChatMessage } from "./ChatMessage";

interface Message {
  id: number;
  role: "user" | "assistant";
  type?: "text" | "recipe" | "nutrition" | "video";
  content?: string;
  recipe?: any;
  nutrition?: any;
  video?: any;
}

interface ChatMessagesProps {
  messages: Message[];
}

export function ChatMessages({ messages }: ChatMessagesProps) {
  return (
    <div className="flex-1 overflow-y-auto overflow-x-hidden min-h-0">
      <div className="max-w-3xl mx-auto w-full px-4 py-8 space-y-6">
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
      </div>
    </div>
  );
}

