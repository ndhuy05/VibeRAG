"use client";

import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import { PanelLeft, PanelLeftClose, Sun, Moon, ChevronDown, Pin, Edit2, Share2, Trash2 } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface ChatHeaderProps {
  sidebarOpen: boolean;
  onToggleSidebar: () => void;
  conversationTitle?: string;
  conversationId?: string | null;
  onPinChat?: (id: string) => void;
  onRenameChat?: (id: string) => void;
  onShareChat?: (id: string) => void;
  onDeleteChat?: (id: string) => void;
}

export function ChatHeader({
  sidebarOpen,
  onToggleSidebar,
  conversationTitle,
  conversationId,
  onPinChat,
  onRenameChat,
  onShareChat,
  onDeleteChat,
}: ChatHeaderProps) {
  const { theme, setTheme } = useTheme();

  return (
    <div className="h-12 flex items-center px-3 gap-2 shrink-0">
      <Button
        variant="ghost"
        size="icon"
        onClick={onToggleSidebar}
        className="h-9 w-9"
      >
        {sidebarOpen ? (
          <PanelLeftClose className="h-5 w-5" />
        ) : (
          <PanelLeft className="h-5 w-5" />
        )}
        <span className="sr-only">Toggle sidebar</span>
      </Button>

      <div className="flex-1 flex items-center justify-center">
        {conversationTitle && conversationId && (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-9 gap-2 max-w-md">
                <h1 className="text-sm font-semibold truncate">
                  {conversationTitle}
                </h1>
                <ChevronDown className="h-4 w-4 opacity-50" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="center" className="w-48">
              <DropdownMenuItem onClick={() => onShareChat?.(conversationId)}>
                <Share2 className="mr-2 h-4 w-4" />
                <span>Chia sẻ cuộc trò chuyện</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onPinChat?.(conversationId)}>
                <Pin className="mr-2 h-4 w-4" />
                <span>Ghim</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onRenameChat?.(conversationId)}>
                <Edit2 className="mr-2 h-4 w-4" />
                <span>Đổi tên</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => onDeleteChat?.(conversationId)}
                className="text-destructive focus:text-destructive"
              >
                <Trash2 className="mr-2 h-4 w-4" />
                <span>Xóa</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )}
      </div>

      <Button
        variant="ghost"
        size="icon"
        onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        className="h-9 w-9"
      >
        <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
        <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
        <span className="sr-only">Toggle theme</span>
      </Button>
    </div>
  );
}

