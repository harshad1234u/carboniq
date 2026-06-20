import { useEffect, useState } from 'react';
import { useCarbon } from '../hooks/useCarbon';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { EcoTwinCard } from '../components/EcoTwinCard';
import { ImpactEquivalents } from '../components/ImpactEquivalents';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { ErrorState } from '../components/ErrorState';
import { ArrowRight, Sparkles } from 'lucide-react';
import { formatCO2 } from '../utils/formatters';

export function EcoTwin() {
  const { getEcoTwin, loading, error } = useCarbon();
  const [data, setData] = useState<any>(null);

  const fetchTwin = async () => {
    try {
      const res = await getEcoTwin();
      setData(res);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchTwin();
  }, []);

  if (loading && !data) return <LoadingSkeleton variant="dashboard" />;
  if (error && !data) return <ErrorState message={error} onRetry={fetchTwin} />;
  if (!data) return null;

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Eco Twin Simulator</h1>
        <p className="text-slate-400 max-w-2xl">
          We've simulated a parallel timeline where you followed all the AI Coach's recommendations. 
          Here's how much impact you could have over the next month.
        </p>
      </div>

      <EcoTwinCard 
        currentFootprint={data.current_footprint}
        predictedFootprint={data.predicted_footprint}
        reductionPercentage={data.reduction_percentage}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-slate-200">Current Impact</h2>
          <ImpactEquivalents data={data.current_equivalents} />
        </div>
        
        <div className="space-y-4 relative">
          {/* Subtle glow behind future impact */}
          <div className="absolute inset-0 bg-emerald-500/5 blur-3xl -z-10 rounded-full"></div>
          
          <h2 className="text-xl font-semibold text-emerald-400 flex items-center gap-2">
            <Sparkles className="w-5 h-5"/> Predicted Impact
          </h2>
          <ImpactEquivalents data={data.predicted_equivalents} />
        </div>
      </div>

      {data.recommendation_impacts && data.recommendation_impacts.length > 0 && (
        <div className="pt-8">
          <h3 className="text-lg font-medium text-slate-200 mb-4">How you get there:</h3>
          <div className="grid gap-3">
            {data.recommendation_impacts.map((rec: any, idx: number) => (
              <Card key={idx} className="bg-slate-900/50 border-slate-800">
                <CardContent className="p-4 flex items-center justify-between">
                  <span className="font-medium text-slate-300">{rec.title}</span>
                  <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
                    <ArrowRight className="w-4 h-4" />
                    -{formatCO2(rec.co2_saved)}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
