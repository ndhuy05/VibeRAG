"use client";

import { useState } from "react";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatHeader } from "@/components/chat/ChatHeader";
import { ChatMessages } from "@/components/chat/ChatMessages";
import { ChatInput } from "@/components/chat/ChatInput";

export default function ChatPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const chatHistory = [
    { id: 1, title: "Công thức nấu Phở Bò", timestamp: "2 giờ trước" },
    { id: 2, title: "Cách làm Bánh mì Việt Nam", timestamp: "Hôm qua" },
    { id: 3, title: "Món ăn chay cho người mới", timestamp: "3 ngày trước" },
  ];

  const messages = [
    {
      id: 1,
      role: "user" as const,
      content: "Xin chào! Bạn có thể giúp tôi tìm công thức nấu ăn không?",
      type: "text" as const,
    },
    {
      id: 2,
      role: "assistant" as const,
      content:
        "Chào bạn! Tất nhiên rồi, tôi rất vui được giúp bạn tìm công thức nấu ăn. Bạn muốn nấu món gì hôm nay?",
      type: "text" as const,
    },
    {
      id: 3,
      role: "user" as const,
      content: "Tôi muốn học cách làm món phở bò truyền thống",
      type: "text" as const,
    },
    {
      id: 4,
      role: "assistant" as const,
      content: "Tuyệt vời! Đây là công thức phở bò truyền thống:",
      type: "text" as const,
    },
    {
      id: 5,
      role: "assistant" as const,
      type: "recipe" as const,
      recipe: {
        title: "Phở Bò Truyền Thống",
        ingredients: [
          "1kg xương ống, xương gối",
          "500g thịt bò (nạm, gân)",
          "500g bánh phở tươi",
          "2 củ hành tây",
          "1 củ gừng (khoảng 50g)",
          "3 cây hành lá",
          "Gia vị: 2 hoa hồi, 1 thanh quế, 2 quả thảo quả",
          "Nước mắm, muối, đường",
        ],
        steps: [
          "Ninh xương trong 3-4 tiếng với lửa nhỏ để có nước dùng trong",
          "Rang gừng và hành tây cho thơm, cho vào nồi nước dùng",
          "Cho gia vị (hồi, quế, thảo quả) vào túi vải, thả vào nồi",
          "Luộc thịt bò riêng, sau đó thái mỏng",
          "Trụng bánh phở trong nước sôi",
          "Bày bánh phở vào tô, xếp thịt bò lên trên",
          "Chan nước dùng nóng, rắc hành lá và ngò gai",
        ],
        prepTime: "4 giờ",
        servings: 4,
        difficulty: "Trung bình" as const,
      },
    },
    {
      id: 6,
      role: "assistant" as const,
      type: "nutrition" as const,
      nutrition: {
        calories: 450,
        protein: 35,
        carbs: 55,
        fat: 12,
        servings: 1,
      },
    },
    {
      id: 7,
      role: "assistant" as const,
      content: "Bạn có thể xem video hướng dẫn chi tiết tại đây:",
      type: "text" as const,
    },
    {
      id: 8,
      role: "assistant" as const,
      type: "video" as const,
      video: {
        url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      },
    },
  ];

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <ChatSidebar isOpen={sidebarOpen} chatHistory={chatHistory} />

      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <ChatHeader
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />

        <ChatMessages messages={messages} />

        <ChatInput />
      </div>
    </div>
  );
}
