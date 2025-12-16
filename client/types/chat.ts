export interface Message {
  id: number;
  role: "user" | "assistant";
  type?: "text" | "recipe" | "nutrition" | "video";
  content?: string;
  recipe?: Recipe;
  nutrition?: Nutrition;
  video?: Video;
}

export interface Recipe {
  title: string;
  ingredients: string[];
  steps: string[];
  prepTime?: string;
  servings?: number;
  difficulty?: "Dễ" | "Trung bình" | "Khó";
}

export interface Nutrition {
  calories?: number;
  protein?: number;
  carbs?: number;
  fat?: number;
  servings?: number;
}

export interface Video {
  url: string;
}

export interface Ingredient {
  name: string;
  quantity: string;
}

export interface BackendMeal {
  name: string;
  category: string;
  origin: string;
  ingredients: Ingredient[];
  recipe: string;
  youtube_url?: string;
}

export interface ChatResponse {
  query: string;
  response: string;
  meals_used: BackendMeal[];
  scores: number[];
  audio_path?: string;
}

