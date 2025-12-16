"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock, Users, ChefHat } from "lucide-react";

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
  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <CardTitle className="text-lg">{title}</CardTitle>
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

