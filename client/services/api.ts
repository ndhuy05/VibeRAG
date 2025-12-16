import type { ChatResponse } from '@/types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export const chatAPI = {
  async sendMessage(query: string): Promise<ChatResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error calling chat API:', error);
      throw error;
    }
  },
};

export const ttsAPI = {
  async textToSpeech(text: string, language: string = 'en-US'): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/text-to-speech`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          language: language,
        }),
      });

      if (!response.ok) {
        throw new Error(`TTS API error: ${response.status}`);
      }

      const data = await response.json();
      // Return full URL to audio file
      return `${API_BASE_URL}${data.audio_url}`;
    } catch (error) {
      console.error('Error calling TTS API:', error);
      throw error;
    }
  },
};

export const imageAPI = {
  async detectIngredients(imageFile: File, maxMeals: number = 3): Promise<ChatResponse> {
    try {
      // Convert image to base64
      const base64Image = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          const result = reader.result as string;
          // Remove data:image/...;base64, prefix
          const base64 = result.split(',')[1];
          resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(imageFile);
      });

      const response = await fetch(`${API_BASE_URL}/detect-ingredients`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: base64Image,
          max_meals: maxMeals,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `Image detection failed with status ${response.status}`;
        throw new Error(errorMessage);
      }

      const data = await response.json();

      // Transform to ChatResponse format
      return {
        query: `Detected ingredients: ${data.detected_ingredients.join(', ')}`,
        response: data.response,
        meals_used: data.meals_used,
        scores: data.scores,
      };
    } catch (error) {
      console.error('Error calling image detection API:', error);
      throw error;
    }
  },
};
