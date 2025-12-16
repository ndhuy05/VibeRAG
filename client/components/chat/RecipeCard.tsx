"use client";

import { useState, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Clock, Users, ChefHat, Volume2, VolumeX, Loader2, Pause, Play, Square } from "lucide-react";
import { ttsAPI } from "@/services/api";

interface RecipeCardProps {
  title: string;
  ingredients: string[];
  steps: string[];
  prepTime?: string;
  servings?: number;
  difficulty?: "Dễ" | "Trung bình" | "Khó";
}

export function RecipeCard({
  title,
  ingredients,
  steps,
  prepTime,
  servings,
  difficulty,
}: RecipeCardProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const handlePlay = async () => {
    try {
      setIsLoading(true);

      // Build text content from card
      let textContent = `Recipe: ${title}. `;

      if (difficulty) {
        textContent += `Difficulty: ${difficulty}. `;
      }

      textContent += `Ingredients: ${ingredients.join(', ')}. `;
      textContent += `Instructions: ${steps.join('. ')}`;

      // Call TTS API
      const audioUrl = await ttsAPI.textToSpeech(textContent, 'en-US');

      // Create and play audio
      if (audioRef.current) {
        audioRef.current.pause();
      }

      const audio = new Audio(audioUrl);
      audioRef.current = audio;

      audio.onended = () => {
        setIsPlaying(false);
        setIsPaused(false);
      };

      audio.onerror = () => {
        setIsPlaying(false);
        setIsPaused(false);
        setIsLoading(false);
        console.error('Error playing audio');
      };

      await audio.play();
      setIsPlaying(true);
      setIsPaused(false);
      setIsLoading(false);
    } catch (error) {
      console.error('Error generating speech:', error);
      setIsLoading(false);
      setIsPlaying(false);
      setIsPaused(false);
    }
  };

  const handlePause = () => {
    if (audioRef.current && isPlaying) {
      audioRef.current.pause();
      setIsPaused(true);
    }
  };

  const handleResume = () => {
    if (audioRef.current && isPaused) {
      audioRef.current.play();
      setIsPaused(false);
    }
  };

  const handleStop = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
      setIsPaused(false);
    }
  };

  const handleMute = () => {
    if (audioRef.current) {
      audioRef.current.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <CardTitle className="text-lg">{title}</CardTitle>
          <div className="flex items-center gap-2">
            {difficulty && (
              <Badge
                variant={
                  difficulty === "Dễ"
                    ? "default"
                    : difficulty === "Trung bình"
                    ? "secondary"
                    : "destructive"
                }
              >
                {difficulty}
              </Badge>
            )}

            {/* Audio Controls */}
            {isPlaying && (
              <div className="flex items-center gap-1 bg-primary/10 rounded-md px-2 py-1">
                <div className="flex gap-0.5">
                  <div className="w-1 h-3 bg-primary animate-pulse" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-1 h-3 bg-primary animate-pulse" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-1 h-3 bg-primary animate-pulse" style={{ animationDelay: '300ms' }}></div>
                </div>
                <span className="text-xs text-primary font-medium ml-1">Playing</span>
              </div>
            )}

            <div className="flex items-center gap-1">
              {!isPlaying ? (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={handlePlay}
                  disabled={isLoading}
                  className="h-8 w-8"
                  title="Play audio"
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Volume2 className="h-4 w-4" />
                  )}
                </Button>
              ) : (
                <>
                  {isPaused ? (
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={handleResume}
                      className="h-8 w-8"
                      title="Resume"
                    >
                      <Play className="h-4 w-4" />
                    </Button>
                  ) : (
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={handlePause}
                      className="h-8 w-8"
                      title="Pause"
                    >
                      <Pause className="h-4 w-4" />
                    </Button>
                  )}

                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleStop}
                    className="h-8 w-8"
                    title="Stop"
                  >
                    <Square className="h-4 w-4" />
                  </Button>

                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleMute}
                    className="h-8 w-8"
                    title={isMuted ? "Unmute" : "Mute"}
                  >
                    {isMuted ? (
                      <VolumeX className="h-4 w-4" />
                    ) : (
                      <Volume2 className="h-4 w-4" />
                    )}
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
        <div className="flex gap-4 text-sm text-muted-foreground mt-2">
          {prepTime && (
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>{prepTime}</span>
            </div>
          )}
          {servings && (
            <div className="flex items-center gap-1">
              <Users className="h-4 w-4" />
              <span>{servings} người</span>
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Ingredients */}
        <div>
          <h4 className="font-semibold flex items-center gap-2 mb-2">
            <ChefHat className="h-4 w-4" />
            Nguyên liệu
          </h4>
          <ul className="space-y-1.5 ml-6">
            {ingredients.map((ingredient, index) => (
              <li key={index} className="text-sm list-disc">
                {ingredient}
              </li>
            ))}
          </ul>
        </div>

        {/* Steps */}
        <div>
          <h4 className="font-semibold mb-2">Cách làm</h4>
          <div className="space-y-2">
            {steps.map((step, index) => (
              <p key={index} className="text-sm leading-relaxed">
                {step}
              </p>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

