import { ArrowRight, Leaf, TrendingDown } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { formatCO2, formatPercentage } from '../utils/formatters';
import { CARBON_SCORE_LEVELS } from '../utils/constants';
import { cn } from '../lib/utils';

interface EcoTwinProps {
  currentFootprint: number;
  predictedFootprint: number;
  reductionPercentage: number;
}

export function EcoTwinCard({ currentFootprint, predictedFootprint, reductionPercentage }: EcoTwinProps) {
  const currentScore = Math.min(100, Math.max(0, Math.floor((currentFootprint / 333) * 100)));
  const predictedScore = Math.min(100, Math.max(0, Math.floor((predictedFootprint / 333) * 100)));

  const currentLevel = CARBON_SCORE_LEVELS.find(l => currentScore >= l.min && currentScore <= l.max) || CARBON_SCORE_LEVELS[0];
  const predictedLevel = CARBON_SCORE_LEVELS.find(l => predictedScore >= l.min && predictedScore <= l.max) || CARBON_SCORE_LEVELS[0];

  return (
    <Card className="bg-slate-900/50 border-slate-800 overflow-hidden relative">
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-500/5 to-emerald-500/10 pointer-events-none" />
      <CardContent className="p-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          
          {/* Current You */}
          <div className="flex-1 flex flex-col items-center text-center p-6 bg-slate-950/50 rounded-2xl border border-slate-800 w-full">
            <h3 className="text-sm font-medium text-slate-400 mb-4 uppercase tracking-wider">Current You</h3>
            <span className="text-3xl font-bold mb-2">{formatCO2(currentFootprint)}</span>
            <div className={cn("px-3 py-1 rounded-full text-xs font-semibold border", currentLevel.bg, currentLevel.color, `border-${currentLevel.color.split('-')[1]}-500/30`)}>
              Score: {currentScore} - {currentLevel.label}
            </div>
          </div>

          {/* Arrow & Reduction */}
          <div className="flex flex-col items-center justify-center relative shrink-0">
            <div className="bg-slate-900 rounded-full p-4 border border-slate-800 z-10 flex flex-col items-center justify-center w-24 h-24 shadow-[0_0_30px_rgba(16,185,129,0.2)]">
              <TrendingDown className="w-6 h-6 text-emerald-500 mb-1" />
              <span className="text-emerald-500 font-bold text-sm">-{formatPercentage(reductionPercentage)}</span>
            </div>
            {/* Connecting lines for desktop */}
            <div className="hidden md:block absolute top-1/2 left-1/2 -translate-y-1/2 w-[200px] -translate-x-1/2 h-[2px] bg-gradient-to-r from-slate-800 via-emerald-500/50 to-slate-800 -z-0"></div>
          </div>

          {/* Future You */}
          <div className="flex-1 flex flex-col items-center text-center p-6 bg-emerald-950/20 rounded-2xl border border-emerald-500/20 w-full relative overflow-hidden">
            <div className="absolute top-0 right-0 p-3">
              <Leaf className="w-5 h-5 text-emerald-500/30" />
            </div>
            <h3 className="text-sm font-medium text-emerald-500 mb-4 uppercase tracking-wider">Eco Twin (Future)</h3>
            <span className="text-3xl font-bold mb-2 text-emerald-400">{formatCO2(predictedFootprint)}</span>
            <div className={cn("px-3 py-1 rounded-full text-xs font-semibold border", predictedLevel.bg, predictedLevel.color, `border-${predictedLevel.color.split('-')[1]}-500/30`)}>
              Score: {predictedScore} - {predictedLevel.label}
            </div>
          </div>

        </div>
      </CardContent>
    </Card>
  );
}
