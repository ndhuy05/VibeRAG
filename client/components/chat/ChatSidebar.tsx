"use client";

import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Plus, MessageSquare, User, Trash2 } from "lucide-react";

interface ChatHistory {
  id: string;
  title: string;
  timestamp: string;
}

interface ChatSidebarProps {
  isOpen: boolean;
  chatHistory: ChatHistory[];
  onNewChat?: () => void;
  onSelectChat?: (id: string) => void;
  onDeleteChat?: (id: string) => void;
  currentChatId?: string | null;
}

export function ChatSidebar({
  isOpen,
  chatHistory,
  onNewChat,
  onSelectChat,
  onDeleteChat,
  currentChatId
}: ChatSidebarProps) {
  return (
    <div
      className={`${
        isOpen ? "w-64" : "w-0"
      } transition-all duration-300 bg-muted/50 flex flex-col h-screen overflow-hidden`}
    >
      <div className="p-3 shrink-0">
        <Button
          className="w-full justify-start gap-2 h-11"
          variant="outline"
          onClick={onNewChat}
        >
          <Plus className="h-4 w-4" />
          Cuộc trò chuyện mới
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto overflow-x-hidden px-2 min-h-0">
        <div className="space-y-1 py-2">
          {chatHistory.map((chat) => (
            <div
              key={chat.id}
              className={`group relative flex items-center gap-2 w-full rounded-md ${
                currentChatId === chat.id ? 'bg-muted' : ''
              }`}
            >
              <Button
                variant="ghost"
                className="flex-1 justify-start gap-3 h-auto py-2.5 px-3 hover:bg-muted/50"
                onClick={() => onSelectChat?.(chat.id)}
              >
                <MessageSquare className="h-4 w-4 shrink-0 opacity-70" />
                <div className="flex-1 text-left overflow-hidden">
                  <p className="text-sm truncate">{chat.title}</p>
                  <p className="text-xs text-muted-foreground">{chat.timestamp}</p>
                </div>
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity mr-2"
                onClick={(e) => {
                  e.stopPropagation();
                  onDeleteChat?.(chat.id);
                }}
              >
                <Trash2 className="h-4 w-4 text-destructive" />
              </Button>
            </div>
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

