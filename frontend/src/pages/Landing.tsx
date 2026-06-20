import { ArrowRight, Leaf, Shield, Zap } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function Landing() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 flex flex-col">
      <header className="p-6 flex items-center justify-between max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-2">
          <Leaf className="w-8 h-8 text-emerald-500" />
          <span className="text-2xl font-bold tracking-tight">CarbonIQ</span>
        </div>
        <div className="flex gap-4">
          {user ? (
            <Link to="/dashboard">
              <Button variant="outline" className="border-emerald-500/50 text-emerald-500 hover:bg-emerald-500/10">
                Go to Dashboard
              </Button>
            </Link>
          ) : (
            <Link to="/login">
              <Button className="bg-emerald-600 hover:bg-emerald-700">Sign In</Button>
            </Link>
          )}
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center text-center p-6 max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 mb-8 border border-emerald-500/20">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-sm font-medium">Your Personal Sustainability Coach</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400 leading-tight">
          Understand, Track, &<br /> Reduce Your Impact
        </h1>
        
        <p className="text-xl text-slate-400 mb-10 max-w-2xl leading-relaxed">
          Go beyond basic calculations. CarbonIQ uses AI to analyze your footprint, predict future savings, and provide personalized coaching to help you live greener.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-20">
          {!user && (
            <Link to="/login">
              <Button size="lg" className="bg-emerald-600 hover:bg-emerald-700 w-full sm:w-auto text-lg h-14 px-8">
                Get Started Free <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left w-full">
          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800">
            <div className="w-12 h-12 rounded-lg bg-blue-500/10 flex items-center justify-center mb-4">
              <Zap className="w-6 h-6 text-blue-500" />
            </div>
            <h3 className="text-xl font-bold mb-2">AI-Powered Insights</h3>
            <p className="text-slate-400">Receive smart, actionable recommendations based on your unique lifestyle and local weather.</p>
          </div>
          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800">
            <div className="w-12 h-12 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-4">
              <Leaf className="w-6 h-6 text-emerald-500" />
            </div>
            <h3 className="text-xl font-bold mb-2">Eco Twin Simulation</h3>
            <p className="text-slate-400">See your future footprint! Our Eco Twin predicts how small lifestyle changes impact your carbon score.</p>
          </div>
          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800">
            <div className="w-12 h-12 rounded-lg bg-amber-500/10 flex items-center justify-center mb-4">
              <Shield className="w-6 h-6 text-amber-500" />
            </div>
            <h3 className="text-xl font-bold mb-2">Gamified Progress</h3>
            <p className="text-slate-400">Complete weekly challenges, earn eco points, and unlock badges as you reduce your emissions.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
