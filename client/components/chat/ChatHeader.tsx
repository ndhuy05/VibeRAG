"use client";

import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import { PanelLeft, PanelLeftClose, Sun, Moon } from "lucide-react";

interface ChatHeaderProps {
  sidebarOpen: boolean;
  onToggleSidebar: () => void;
}

export function ChatHeader({ sidebarOpen, onToggleSidebar }: ChatHeaderProps) {
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

      <div className="flex-1" />

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

