"use client";

import { useState } from "react";
import { CloudSun, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface WeatherButtonProps {
    onGetWeather: (location: string) => void;
    disabled?: boolean;
}

export function WeatherButton({ onGetWeather, disabled }: WeatherButtonProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [location, setLocation] = useState("");

    const handleSubmit = (e?: React.FormEvent) => {
        e?.preventDefault();
        if (location.trim()) {
            onGetWeather(location);
            setLocation("");
            setIsOpen(false);
        }
    };

    return (
        <div className="relative">
            <Button
                variant="ghost"
                size="icon"
                className="h-9 w-9 rounded-full"
                onClick={() => setIsOpen(!isOpen)}
                disabled={disabled}
                title="Gợi ý theo thời tiết"
                type="button"
            >
                <CloudSun className="h-5 w-5" />
            </Button>

            {isOpen && (
                <div className="absolute bottom-12 left-0 z-50 w-72 rounded-md border bg-white p-4 shadow-md dark:bg-zinc-900 dark:border-zinc-800">
                    <div className="flex justify-between items-center mb-3">
                        <h3 className="font-semibold text-sm">Gợi ý theo thời tiết</h3>
                        <Button
                            variant="ghost"
                            size="icon"
                            className="h-6 w-6 p-0 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-full"
                            onClick={() => setIsOpen(false)}
                        >
                            <X className="h-4 w-4" />
                        </Button>
                    </div>
                    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                        <Input
                            placeholder="Nhập thành phố (VD: Hanoi)"
                            value={location}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLocation(e.target.value)}
                            className="h-9"
                            autoFocus
                        />
                        <Button type="submit" size="sm" disabled={!location.trim()}>
                            Xem gợi ý món ăn
                        </Button>
                    </form>
                </div>
            )}
        </div>
    );
}
