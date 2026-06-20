import { Cloud, Droplets, Sun, Thermometer } from 'lucide-react';
import { Card, CardContent } from './ui/card';

interface WeatherInsightProps {
  weather: {
    city: string;
    temperature: number;
    description: string;
    humidity: number;
  };
}

export function WeatherInsight({ weather }: WeatherInsightProps) {
  if (!weather) return null;

  return (
    <Card className="bg-gradient-to-br from-blue-900/40 to-slate-900/80 border-blue-500/20">
      <CardContent className="p-4 sm:p-6 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-blue-400 mb-1">
            <Sun className="w-5 h-5" />
            <span className="text-sm font-medium uppercase tracking-wider">Local Insight</span>
          </div>
          <h3 className="text-xl font-bold text-slate-100 mb-1">{weather.city}</h3>
          <p className="text-slate-300 capitalize text-sm">{weather.description}</p>
        </div>
        
        <div className="flex gap-6">
          <div className="flex flex-col items-center">
            <Thermometer className="w-5 h-5 text-amber-500 mb-1" />
            <span className="font-semibold">{Math.round(weather.temperature)}°C</span>
          </div>
          <div className="flex flex-col items-center">
            <Droplets className="w-5 h-5 text-blue-400 mb-1" />
            <span className="font-semibold">{weather.humidity}%</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
