"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Flame, Beef, Wheat, Droplet } from "lucide-react";

interface NutritionInfoProps {
  calories?: number;
  protein?: number;
  carbs?: number;
  fat?: number;
  servings?: number;
}

export function NutritionInfo({
  calories,
  protein,
  carbs,
  fat,
  servings = 1,
}: NutritionInfoProps) {
  const nutritionItems = [
    {
      label: "Calories",
      value: calories,
      unit: "kcal",
      icon: Flame,
      color: "text-orange-500",
    },
    {
      label: "Protein",
      value: protein,
      unit: "g",
      icon: Beef,
      color: "text-red-500",
    },
    {
      label: "Carbs",
      value: carbs,
      unit: "g",
      icon: Wheat,
      color: "text-yellow-600",
    },
    {
      label: "Fat",
      value: fat,
      unit: "g",
      icon: Droplet,
      color: "text-blue-500",
    },
  ];

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">Thông tin dinh dưỡng</CardTitle>
          <Badge variant="outline">Cho {servings} người</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {nutritionItems.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.label}
                className="flex flex-col items-center p-3 rounded-lg bg-muted/30"
              >
                <Icon className={`h-5 w-5 mb-2 ${item.color}`} />
                <div className="text-center">
                  <p className="text-lg font-semibold">
                    {item.value !== undefined ? item.value : "—"}
                    {item.value !== undefined && (
                      <span className="text-xs ml-0.5">{item.unit}</span>
                    )}
                  </p>
                  <p className="text-xs text-muted-foreground">{item.label}</p>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

