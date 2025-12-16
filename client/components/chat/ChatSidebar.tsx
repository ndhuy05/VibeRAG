"use client";

import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Plus, MessageSquare, User } from "lucide-react";

interface ChatHistory {
  id: number;
  title: string;
  timestamp: string;
}

interface ChatSidebarProps {
  isOpen: boolean;
  chatHistory: ChatHistory[];
}

export function ChatSidebar({ isOpen, chatHistory }: ChatSidebarProps) {
  return (
    <div
      className={`${
        isOpen ? "w-64" : "w-0"
      } transition-all duration-300 bg-muted/50 flex flex-col h-screen overflow-hidden`}
    >
      <div className="p-3 shrink-0">
        <Button className="w-full justify-start gap-2 h-11" variant="outline">
          <Plus className="h-4 w-4" />
          Cuộc trò chuyện mới
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto overflow-x-hidden px-2 min-h-0">
        <div className="space-y-1 py-2">
          {chatHistory.map((chat) => (
            <Button
              key={chat.id}
              variant="ghost"
              className="w-full justify-start gap-3 h-auto py-2.5 px-3 hover:bg-muted/50"
            >
              <MessageSquare className="h-4 w-4 shrink-0 opacity-70" />
              <span className="text-sm truncate text-left">{chat.title}</span>
            </Button>
          ))}
        </div>
      </div>

      <div className="p-3 shrink-0 border-t bg-muted/20">
        <Button variant="ghost" className="w-full justify-start gap-3 h-11">
          <User className="h-4 w-4" />
          <span className="text-sm">Tài khoản</span>
        </Button>
      </div>
    </div>
  );
}

