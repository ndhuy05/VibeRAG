"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send } from "lucide-react";
import { ImageUpload } from "./ImageUpload";
import { VoiceRecorder } from "./VoiceRecorder";
import { WeatherButton } from "./WeatherButton";

interface ChatInputProps {
  onSendMessage?: (message: string, image?: File) => void;
  onWeatherRequest?: (location: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, onWeatherRequest, disabled = false }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [selectedImage, setSelectedImage] = useState<File | null>(null);

  const handleSend = () => {
    if ((message.trim() || selectedImage) && !disabled) {
      console.log("Send:", message, selectedImage);
      onSendMessage?.(message, selectedImage || undefined);
      setMessage("");
      setSelectedImage(null);
    }
  };

  const handleVoiceRecording = (blob: Blob) => {
    console.log("Recording completed:", blob);
    // Handle voice recording
  };

  return (
    <div className="p-4 pb-6 shrink-0">
      <div className="max-w-3xl mx-auto w-full space-y-3">
        {/* Image Preview */}
        {selectedImage && (
          <div className="flex justify-start">
            <ImageUpload
              onImageSelect={setSelectedImage}
              onImageRemove={() => setSelectedImage(null)}
              selectedImage={selectedImage}
            />
          </div>
        )}

        {/* Input Box */}
        <div className="relative bg-muted/50 rounded-full shadow-sm hover:shadow-md transition-shadow flex items-center gap-2 px-3 py-2">
          {/* Left Actions */}
          <div className="flex items-center gap-1 shrink-0">
            {!selectedImage && (
              <ImageUpload
                onImageSelect={setSelectedImage}
                onImageRemove={() => setSelectedImage(null)}
                selectedImage={selectedImage}
              />
            )}
            <VoiceRecorder onRecordingComplete={handleVoiceRecording} />
            <WeatherButton onGetWeather={(loc) => onWeatherRequest?.(loc)} disabled={disabled} />
          </div>

          {/* Textarea */}
          <Textarea
            placeholder={disabled ? "Đang xử lý..." : "Nhập tin nhắn của bạn..."}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            rows={1}
            disabled={disabled}
            className="min-h-0 max-h-[200px] resize-none bg-transparent border-0 px-2 py-1.5 pr-12 focus-visible:ring-0 focus-visible:ring-offset-0 overflow-hidden flex-1 shadow-none focus:shadow-none"
            style={{
              height: "auto",
              minHeight: "28px",
            }}
            onInput={(e) => {
              const target = e.target as HTMLTextAreaElement;
              target.style.height = "28px";
              target.style.height = target.scrollHeight + "px";
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />

          {/* Send Button */}
          <Button
            size="icon"
            className="h-9 w-9 rounded-full shrink-0"
            disabled={(!message.trim() && !selectedImage) || disabled}
            onClick={handleSend}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}

