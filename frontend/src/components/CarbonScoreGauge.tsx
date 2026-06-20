import { useEffect, useState } from 'react';
import { cn } from '../lib/utils';
import { CARBON_SCORE_LEVELS } from '../utils/constants';

interface CarbonScoreGaugeProps {
  score: number;
}

export function CarbonScoreGauge({ score }: CarbonScoreGaugeProps) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedScore(score);
    }, 100);
    return () => clearTimeout(timer);
  }, [score]);

  const level = CARBON_SCORE_LEVELS.find(l => score >= l.min && score <= l.max) || CARBON_SCORE_LEVELS[0];

  // SVG Gauge calculations
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  // Make the gauge a semi-circle (or 3/4 circle). Let's do 3/4 circle:
  const offset = circumference - (animatedScore / 100) * circumference * 0.75;
  const dashArray = `${circumference * 0.75} ${circumference * 0.25}`;

  return (
    <div 
      className="flex flex-col items-center justify-center relative p-6"
      role="meter" 
      aria-valuenow={animatedScore} 
      aria-valuemin={0} 
      aria-valuemax={100} 
      aria-label="Carbon Score Gauge"
    >
      <div className="relative w-48 h-48">
        <svg className="w-full h-full transform -rotate-135" viewBox="0 0 140 140">
          {/* Background Track */}
          <circle
            cx="70"
            cy="70"
            r={radius}
            fill="transparent"
            stroke="currentColor"
            strokeWidth="12"
            strokeDasharray={dashArray}
            strokeDashoffset="0"
            strokeLinecap="round"
            className="text-slate-800"
          />
          {/* Active Progress */}
          <circle
            cx="70"
            cy="70"
            r={radius}
            fill="transparent"
            stroke="currentColor"
            strokeWidth="12"
            strokeDasharray={dashArray}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className={cn("transition-all duration-1000 ease-out", level.color)}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center pt-4">
          <span className="text-4xl font-bold tracking-tighter">{animatedScore}</span>
          <span className="text-xs text-slate-400 font-medium">/ 100</span>
        </div>
      </div>
      <div className={cn("mt-[-1rem] px-4 py-1.5 rounded-full border text-sm font-semibold tracking-wide", level.bg, level.color, `border-${level.color.split('-')[1]}-500/30`)}>
        {level.label}
      </div>
    </div>
  );
}
