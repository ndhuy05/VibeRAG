"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Bot, User, Volume2 } from "lucide-react";
import { RecipeCard } from "./RecipeCard";
import { NutritionInfo } from "./NutritionInfo";
import { VideoEmbed } from "./VideoEmbed";

interface Message {
  id: number;
  role: "user" | "assistant";
  type?: "text" | "recipe" | "nutrition" | "video";
  content?: string;
  recipe?: any;
  nutrition?: any;
  video?: any;
}

interface ChatMessageProps {
  message: Message;
  isFirstInGroup: boolean;
}

export function ChatMessage({ message, isFirstInGroup }: ChatMessageProps) {
  const handleTextToSpeech = (text: string) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "vi-VN";
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div
      className={`flex gap-4 group ${
        message.role === "user" ? "justify-end" : ""
      }`}
    >
      {message.role === "assistant" && (
        <div className="w-8 shrink-0">
          {isFirstInGroup && (
            <Avatar className="h-8 w-8">
              <AvatarFallback className="bg-muted">
                <Bot className="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
          )}
        </div>
      )}

      <div
        className={`space-y-3 ${
          message.role === "user" ? "max-w-[70%]" : "flex-1"
        }`}
      >
        {message.role === "user" ? (
          <div className="bg-muted/60 rounded-2xl px-4 py-3">
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {message.content}
            </p>
          </div>
        ) : (
          <>
            {message.type === "text" && message.content && (
              <div className="flex items-start gap-2 group/message">
                <p className="text-sm leading-relaxed whitespace-pre-wrap pt-1 flex-1">
                  {message.content}
                </p>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7 opacity-0 group-hover/message:opacity-100 transition-opacity"
                  onClick={() => handleTextToSpeech(message.content!)}
                >
                  <Volume2 className="h-4 w-4" />
                </Button>
              </div>
            )}
            {message.type === "recipe" && message.recipe && (
              <RecipeCard {...message.recipe} />
            )}
            {message.type === "nutrition" && message.nutrition && (
              <NutritionInfo {...message.nutrition} />
            )}
            {message.type === "video" && message.video && (
              <VideoEmbed videoUrl={message.video.url} />
            )}
          </>
        )}
      </div>

      {message.role === "user" && (
        <Avatar className="h-8 w-8 shrink-0">
          <AvatarFallback className="bg-muted">
            <User className="h-4 w-4" />
          </AvatarFallback>
        </Avatar>
      )}
    </div>
  );
}

