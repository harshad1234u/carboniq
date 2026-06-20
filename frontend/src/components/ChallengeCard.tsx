import { CheckCircle2, Circle } from 'lucide-react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { cn } from '../lib/utils';

interface ChallengeProps {
  challenge: {
    id: string;
    title: string;
    description: string;
    eco_points: number;
    is_completed: boolean;
  };
  onComplete: (id: string) => void;
  isLoading?: boolean;
}

export function ChallengeCard({ challenge, onComplete, isLoading }: ChallengeProps) {
  return (
    <Card 
      role="article"
      className={cn(
      "transition-all duration-300",
      challenge.is_completed 
        ? "bg-emerald-950/20 border-emerald-500/30 opacity-80" 
        : "bg-slate-900/50 border-slate-800 hover:border-slate-700"
    )}>
      <CardContent className="p-5 flex items-start gap-4">
        <div role="status" className="shrink-0 mt-1">
          {challenge.is_completed ? (
            <CheckCircle2 className="w-6 h-6 text-emerald-500" aria-label="Completed" />
          ) : (
            <Circle className="w-6 h-6 text-slate-500" aria-label="Incomplete" />
          )}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-4 mb-2">
            <h3 className={cn(
              "font-semibold text-lg leading-tight",
              challenge.is_completed ? "text-slate-300 line-through" : "text-slate-100"
            )}>
              {challenge.title}
            </h3>
            <span className="shrink-0 inline-flex items-center justify-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-500 border border-amber-500/20">
              +{challenge.eco_points} pts
            </span>
          </div>
          <p className="text-slate-400 text-sm mb-4 line-clamp-2">{challenge.description}</p>
          
          {!challenge.is_completed && (
            <Button 
              size="sm" 
              variant="outline" 
              className="w-full sm:w-auto border-emerald-500/30 text-emerald-500 hover:bg-emerald-500/10"
              onClick={() => onComplete(challenge.id)}
              disabled={isLoading}
              aria-label={`Mark ${challenge.title} as complete`}
            >
              {isLoading ? "Completing..." : "Mark Complete"}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
