"use client";

import { Card } from "@/components/ui/card";

interface VideoEmbedProps {
  videoUrl: string;
  title?: string;
}

export function VideoEmbed({ videoUrl, title }: VideoEmbedProps) {
  // Extract YouTube video ID from URL
  const getYouTubeId = (url: string) => {
    const regExp =
      /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return match && match[2].length === 11 ? match[2] : null;
  };

  const videoId = getYouTubeId(videoUrl);

  if (!videoId) {
    return (
      <Card className="p-4">
        <p className="text-sm text-muted-foreground">
          Không thể tải video. URL không hợp lệ.
        </p>
      </Card>
    );
  }

  return (
    <Card className="overflow-hidden">
      <div className="relative w-full" style={{ paddingBottom: "56.25%" }}>
        <iframe
          className="absolute top-0 left-0 w-full h-full"
          src={`https://www.youtube.com/embed/${videoId}`}
          title={title || "YouTube video"}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>
    </Card>
  );
}

