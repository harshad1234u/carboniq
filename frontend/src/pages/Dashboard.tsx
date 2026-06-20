import { useEffect, useState } from 'react';
import { useCarbon } from '../hooks/useCarbon';
import { useProfile } from '../hooks/useProfile';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { CarbonScoreGauge } from '../components/CarbonScoreGauge';
import { ImpactEquivalents } from '../components/ImpactEquivalents';
import { BadgeDisplay } from '../components/BadgeDisplay';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { ErrorState } from '../components/ErrorState';
import { EmptyState } from '../components/EmptyState';
import { Trophy, TrendingDown, TrendingUp, Minus } from 'lucide-react';
import { formatCO2 } from '../utils/formatters';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';

export function Dashboard() {
  const { profile } = useProfile();
  const { getDashboardSummary, loading, error } = useCarbon();
  const [summary, setSummary] = useState<any>(null);

  const fetchSummary = async () => {
    try {
      const data = await getDashboardSummary();
      setSummary(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  if (loading && !summary) {
    return <LoadingSkeleton variant="dashboard" />;
  }

  if (error && !summary) {
    return <ErrorState message={error} onRetry={fetchSummary} />;
  }

  if (!summary || summary.latest_score === null) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Welcome, {profile?.name?.split(' ')[0] || 'Eco Warrior'}! 👋</h1>
          <p className="text-slate-400">Let's find out your carbon footprint.</p>
        </div>
        <EmptyState 
          title="No Data Yet" 
          description="You haven't calculated your carbon footprint yet. Take the first step towards a greener lifestyle."
          actionLabel="Calculate Footprint"
          onAction={() => window.location.href = '/calculator'}
        />
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* Header section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Dashboard</h1>
          <p className="text-slate-400">Here's your environmental impact summary.</p>
        </div>
        <div className="flex items-center gap-2 bg-slate-900/50 px-4 py-2 rounded-full border border-slate-800">
          <Trophy className="w-5 h-5 text-amber-500" />
          <span className="font-semibold text-amber-500">{summary.eco_points} Eco Points</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Main Score Area */}
        <Card className="lg:col-span-5 bg-slate-900/50 border-slate-800 flex flex-col items-center justify-center pt-8 pb-4">
          <h2 className="text-lg font-medium text-slate-300 mb-2">Your Carbon Score</h2>
          <CarbonScoreGauge score={summary.latest_score} />
          
          <div className="mt-8 grid grid-cols-2 gap-8 w-full px-8 border-t border-slate-800/50 pt-6">
            <div className="text-center">
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Monthly Footprint</span>
              <span className="text-xl font-bold">{formatCO2(summary.monthly_footprint)}</span>
            </div>
            <div className="text-center">
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Trend</span>
              <div className="flex items-center justify-center gap-1 text-xl font-bold">
                {summary.trend === 'down' ? (
                  <span className="text-emerald-500 flex items-center"><TrendingDown className="w-5 h-5 mr-1"/> Improving</span>
                ) : summary.trend === 'up' ? (
                  <span className="text-red-500 flex items-center"><TrendingUp className="w-5 h-5 mr-1"/> Rising</span>
                ) : (
                  <span className="text-slate-400 flex items-center"><Minus className="w-5 h-5 mr-1"/> Stable</span>
                )}
              </div>
            </div>
          </div>
        </Card>

        {/* Right side: Equivalents & Actions */}
        <div className="lg:col-span-7 space-y-8">
          <div>
            <h3 className="text-lg font-medium text-slate-200 mb-4">Your Impact Equals...</h3>
            <ImpactEquivalents data={summary.impact_equivalents} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Card className="bg-slate-900/50 border-slate-800">
              <CardContent className="p-6">
                <h3 className="font-medium text-slate-200 mb-2">Want to improve?</h3>
                <p className="text-sm text-slate-400 mb-4">Get personalized tips from our AI Coach based on your lifestyle and local weather.</p>
                <Link to="/ai-coach">
                  <Button className="w-full bg-emerald-600 hover:bg-emerald-700">Ask AI Coach</Button>
                </Link>
              </CardContent>
            </Card>
            
            <Card className="bg-slate-900/50 border-slate-800">
              <CardContent className="p-6">
                <h3 className="font-medium text-slate-200 mb-2">See your future</h3>
                <p className="text-sm text-slate-400 mb-4">Discover how small changes today impact your footprint tomorrow.</p>
                <Link to="/eco-twin">
                  <Button className="w-full bg-blue-600 hover:bg-blue-700">View Eco Twin</Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Badges Section */}
      {summary.recent_badges && summary.recent_badges.length > 0 && (
        <Card className="bg-slate-900/50 border-slate-800">
          <CardHeader>
            <CardTitle className="text-lg">Recent Badges</CardTitle>
          </CardHeader>
          <CardContent>
            <BadgeDisplay badges={summary.recent_badges} />
          </CardContent>
        </Card>
      )}

    </div>
  );
}
