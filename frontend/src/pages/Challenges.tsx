import { useChallenge } from '../hooks/useChallenge';
import { ChallengeCard } from '../components/ChallengeCard';
import { BadgeDisplay } from '../components/BadgeDisplay';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { ErrorState } from '../components/ErrorState';
import { Trophy, Award } from 'lucide-react';
import { useState } from 'react';

export function Challenges() {
  const { challenges, badges, loading, error, completeChallenge } = useChallenge();
  const [completingId, setCompletingId] = useState<string | null>(null);

  const handleComplete = async (id: string) => {
    setCompletingId(id);
    try {
      await completeChallenge(id);
    } catch (err) {
      alert("Failed to complete challenge");
    } finally {
      setCompletingId(null);
    }
  };

  if (loading && challenges.length === 0) return <LoadingSkeleton variant="dashboard" />;
  if (error && challenges.length === 0) return <ErrorState message={error} />;

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Weekly Challenges</h1>
        <p className="text-slate-400 max-w-2xl">
          Turn intent into action. Complete these personalized challenges to lower your footprint and earn eco points.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Active Challenges List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <Trophy className="w-5 h-5 text-amber-500" />
            <h2 className="text-xl font-semibold text-slate-200">Current Tasks</h2>
          </div>
          
          {challenges.length === 0 ? (
            <div className="p-8 text-center border border-dashed border-slate-800 rounded-xl bg-slate-900/30">
              <p className="text-slate-400">No active challenges right now. Check back later!</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {challenges.map(challenge => (
                <ChallengeCard 
                  key={challenge.id} 
                  challenge={challenge} 
                  onComplete={handleComplete}
                  isLoading={completingId === challenge.id}
                />
              ))}
            </div>
          )}
        </div>

        {/* Badges sidebar */}
        <div className="lg:col-span-1 space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <Award className="w-5 h-5 text-purple-500" />
            <h2 className="text-xl font-semibold text-slate-200">Your Badges</h2>
          </div>
          <div className="bg-slate-900/30 rounded-xl p-4 border border-slate-800">
            <BadgeDisplay badges={badges} />
          </div>
        </div>

      </div>
    </div>
  );
}
