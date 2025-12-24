"use client";

import { useState, useRef, useEffect } from "react";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatHeader } from "@/components/chat/ChatHeader";
import { ChatMessages } from "@/components/chat/ChatMessages";
import { ChatInput } from "@/components/chat/ChatInput";
import { chatAPI, imageAPI, weatherAPI } from "@/services/api";
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

  const handleWeatherRequest = async (location: string) => {
    // Add user message
    const userMessage: Message = {
      id: messageIdCounter.current++,
      role: "user",
      type: "text",
      content: `Gợi ý món ăn cho thời tiết ở ${location}`,
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await weatherAPI.getSuggestions(location);

      // Add AI response text
      let aiResponseText = `🌡️ **Thời tiết tại ${response.location}:** ${response.temperature}°C, ${response.weather_description} (${response.weather_condition})\n\n${response.ai_response}`;

      const aiTextMessage: Message = {
        id: messageIdCounter.current++,
        role: "assistant",
        type: "text",
        content: aiResponseText,
      };
      setMessages(prev => [...prev, aiTextMessage]);

      // Add recipes
      if (response.recommended_meals) {
        response.recommended_meals.forEach((meal: BackendMeal) => {
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
      }

    } catch (error) {
      console.error("Error getting weather suggestions:", error);
      const errorMessage: Message = {
        id: messageIdCounter.current++,
        role: "assistant",
        type: "text",
        content: "Xin lỗi, không thể lấy thông tin thời tiết lúc này. Hãy kiểm tra tên địa điểm và thử lại.",
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (messageText: string, imageFile?: File) => {

    if (!messageText.trim() && !imageFile) return;

    // Create image URL if image is provided
    let imageUrl: string | undefined;
    if (imageFile) {
      imageUrl = URL.createObjectURL(imageFile);
    }

    // Add user message
    const userMessage: Message = {
      id: messageIdCounter.current++,
      role: "user",
      type: imageFile ? "image" : "text",
      content: messageText || (imageFile ? "Phát hiện nguyên liệu từ ảnh" : ""),
      imageUrl: imageUrl,
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call appropriate API based on whether image is provided
      const response = imageFile
        ? await imageAPI.detectIngredients(imageFile, 3)
        : await chatAPI.sendMessage(messageText);

      // Add recipes if available
      if (response.meals_used && response.meals_used.length > 0) {
        // Add AI response text
        let aiResponseText = `Đây là ${response.meals_used.length} món ăn phù hợp với yêu cầu của bạn:`;

        // If image was used, show detected ingredients
        if (imageFile && response.query.includes('Detected ingredients:')) {
          const ingredients = response.query.replace('Detected ingredients: ', '');
          aiResponseText = `🔍 **Nguyên liệu phát hiện được:** ${ingredients}\n\n${aiResponseText}`;
        }

        const aiTextMessage: Message = {
          id: messageIdCounter.current++,
          role: "assistant",
          type: "text",
          content: aiResponseText,
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

        <ChatInput onSendMessage={handleSendMessage} onWeatherRequest={handleWeatherRequest} disabled={isLoading} />
      </div>
    </div>
  );
}
