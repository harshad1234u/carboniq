import { Award } from 'lucide-react';
import { formatDate } from '../utils/formatters';

interface BadgeProps {
  badges: Array<{
    id: string;
    badge_name: string;
    badge_description: string;
    earned_at: string;
  }>;
}

export function BadgeDisplay({ badges }: BadgeProps) {
  if (!badges || badges.length === 0) {
    return (
      <div className="text-center py-8 text-slate-500 text-sm">
        <Award className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p>Complete challenges to earn badges!</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
      {badges.map((badge) => (
        <div key={badge.id} className="flex flex-col items-center text-center p-4 rounded-xl bg-slate-900/50 border border-slate-800 hover:border-amber-500/30 transition-colors">
          <div className="relative mb-3">
            <div className="absolute inset-0 bg-amber-500/20 blur-xl rounded-full"></div>
            <Award className="w-10 h-10 text-amber-400 relative z-10" />
          </div>
          <h4 className="font-semibold text-slate-200 text-sm mb-1">{badge.badge_name}</h4>
          <p className="text-[10px] text-slate-400 mb-2">{badge.badge_description}</p>
          <span className="text-[10px] text-slate-500 font-medium">Earned {formatDate(badge.earned_at)}</span>
        </div>
      ))}
    </div>
  );
}
