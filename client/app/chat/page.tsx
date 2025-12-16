"use client";

import { useState, useRef, useEffect } from "react";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatHeader } from "@/components/chat/ChatHeader";
import { ChatMessages } from "@/components/chat/ChatMessages";
import { ChatInput } from "@/components/chat/ChatInput";
import { chatAPI } from "@/services/api";
import type { Message, BackendMeal } from "@/types/chat";
import { useChatHistory } from "@/hooks/useChatHistory";

export default function ChatPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messageIdCounter = useRef(1);

  const {
    conversations,
    currentConversationId,
    saveConversation,
    loadConversation,
    deleteConversation,
    startNewConversation,
  } = useChatHistory();

  // Helper function to extract steps from recipe text
  const extractSteps = (recipe: string): string[] => {
    return recipe
      .split(/\r?\n/)
      .filter(step => step.trim().length > 0)
      .map(step => step.trim());
  };

  // Save conversation whenever messages change (debounced)
  useEffect(() => {
    if (messages.length > 0) {
      const timer = setTimeout(() => {
        saveConversation(messages);
      }, 500); // Debounce 500ms

      return () => clearTimeout(timer);
    }
  }, [messages, saveConversation]);

  const handleNewChat = () => {
    setMessages([]);
    messageIdCounter.current = 1;
    startNewConversation();
  };

  const handleSelectChat = (id: string) => {
    const loadedMessages = loadConversation(id);
    if (loadedMessages) {
      setMessages(loadedMessages);
      // Find max message ID to continue counter
      const maxId = loadedMessages.reduce((max, msg) => Math.max(max, msg.id), 0);
      messageIdCounter.current = maxId + 1;
    }
  };

  const handleDeleteChat = (id: string) => {
    deleteConversation(id);
    // If deleting current conversation, start new one
    if (currentConversationId === id) {
      handleNewChat();
    }
  };

  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: messageIdCounter.current++,
      role: "user",
      type: "text",
      content: messageText,
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call API
      const response = await chatAPI.sendMessage(messageText);

      // Add recipes if available
      if (response.meals_used && response.meals_used.length > 0) {
        // Add AI response text - short and simple
        const aiTextMessage: Message = {
          id: messageIdCounter.current++,
          role: "assistant",
          type: "text",
          content: `Đây là ${response.meals_used.length} món ăn phù hợp với yêu cầu của bạn:`,
        };
        setMessages(prev => [...prev, aiTextMessage]);

        response.meals_used.forEach((meal: BackendMeal) => {
          // Add recipe card
          const recipeMessage: Message = {
            id: messageIdCounter.current++,
            role: "assistant",
            type: "recipe",
            recipe: {
              title: meal.name,
              ingredients: meal.ingredients.map(ing => `${ing.quantity} ${ing.name}`),
              steps: extractSteps(meal.recipe),
              difficulty: "Trung bình",
            },
          };
          setMessages(prev => [...prev, recipeMessage]);

          // Add video if available
          if (meal.youtube_url) {
            const videoMessage: Message = {
              id: messageIdCounter.current++,
              role: "assistant",
              type: "video",
              video: {
                url: meal.youtube_url,
              },
            };
            setMessages(prev => [...prev, videoMessage]);
          }
        });
      } else {
        // No meals found - show AI response
        const aiTextMessage: Message = {
          id: messageIdCounter.current++,
          role: "assistant",
          type: "text",
          content: response.response || "Xin lỗi, tôi không tìm thấy món ăn phù hợp với yêu cầu của bạn.",
        };
        setMessages(prev => [...prev, aiTextMessage]);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: Message = {
        id: messageIdCounter.current++,
        role: "assistant",
        type: "text",
        content: "Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.",
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <ChatSidebar
        isOpen={sidebarOpen}
        chatHistory={conversations}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
        onDeleteChat={handleDeleteChat}
        currentChatId={currentConversationId}
      />

      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <ChatHeader
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />

        <ChatMessages
          messages={messages}
          isLoading={isLoading}
          onSuggestedQuery={handleSendMessage}
        />

        <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
