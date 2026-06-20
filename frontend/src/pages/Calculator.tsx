import { useState } from 'react';
import { useCarbon } from '../hooks/useCarbon';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { VEHICLE_TYPES, DIET_TYPES } from '../utils/constants';
import { Car, Zap, Wind, Utensils, Plane, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export function Calculator() {
  const { calculate, loading, error, result } = useCarbon();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    vehicle_type: 'car_petrol',
    daily_travel_km: 15,
    electricity_kwh: 150,
    ac_hours: 4,
    diet_type: 'average',
    flights_short: 0,
    flights_long: 0
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await calculate(formData);
  };

  if (result) {
    return (
      <div className="max-w-2xl mx-auto space-y-6 animate-in fade-in zoom-in-95 duration-500">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-emerald-500/20 mb-4">
            <span className="text-3xl">🎉</span>
          </div>
          <h2 className="text-3xl font-bold mb-2">Calculation Complete!</h2>
          <p className="text-slate-400">Your carbon footprint has been updated.</p>
        </div>

        <Card className="bg-slate-900/50 border-emerald-500/30">
          <CardContent className="p-6 text-center">
            <span className="text-sm uppercase tracking-wider text-slate-400 font-medium mb-2 block">Monthly Emissions</span>
            <span className="text-5xl font-bold text-white mb-6 block">{result.total_emissions.toFixed(1)} kg CO₂</span>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
              <Button onClick={() => navigate('/dashboard')} variant="outline" className="border-slate-700 hover:bg-slate-800">
                View Dashboard
              </Button>
              <Button onClick={() => navigate('/ai-coach')} className="bg-emerald-600 hover:bg-emerald-700">
                Get AI Coaching <ArrowRight className="ml-2 w-4 h-4"/>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-2">Carbon Calculator</h1>
        <p className="text-slate-400">Enter your monthly usage details below. We'll crunch the numbers and update your carbon score.</p>
      </div>

      <Card className="bg-slate-900/50 border-slate-800">
        <CardContent className="p-6">
          <form onSubmit={handleSubmit} className="space-y-8">
            
            {/* Transport */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-slate-200 flex items-center gap-2 border-b border-slate-800 pb-2">
                <Car className="w-5 h-5 text-blue-500"/> Transport
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm text-slate-400">Vehicle Type</label>
                  <select
                    value={formData.vehicle_type}
                    onChange={e => setFormData({...formData, vehicle_type: e.target.value})}
                    className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-slate-200 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                  >
                    {VEHICLE_TYPES.map(v => <option key={v.value} value={v.value}>{v.label}</option>)}
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-sm text-slate-400">Daily Travel (km)</label>
                  <input
                    type="number" min="0"
                    value={formData.daily_travel_km}
                    onChange={e => setFormData({...formData, daily_travel_km: Number(e.target.value)})}
                    className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-slate-200 focus:border-emerald-500 outline-none"
                  />
                </div>
              </div>
            </div>

            {/* Energy */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-slate-200 flex items-center gap-2 border-b border-slate-800 pb-2">
                <Zap className="w-5 h-5 text-amber-500"/> Energy
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm text-slate-400">Monthly Electricity (kWh)</label>
                  <input
                    type="number" min="0"
                    value={formData.electricity_kwh}
                    onChange={e => setFormData({...formData, electricity_kwh: Number(e.target.value)})}
                    className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-slate-200 focus:border-emerald-500 outline-none"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm text-slate-400">Daily AC Usage (hours)</label>
                  <input
                    type="number" min="0" max="24"
                    value={formData.ac_hours}
                    onChange={e => setFormData({...formData, ac_hours: Number(e.target.value)})}
                    className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-slate-200 focus:border-emerald-500 outline-none"
                  />
                </div>
              </div>
            </div>

            {/* Diet */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-slate-200 flex items-center gap-2 border-b border-slate-800 pb-2">
                <Utensils className="w-5 h-5 text-emerald-500"/> Diet
              </h3>
              <div className="space-y-2">
                <label className="text-sm text-slate-400">Diet Type</label>
                <select
                  value={formData.diet_type}
                  onChange={e => setFormData({...formData, diet_type: e.target.value})}
                  className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-slate-200 focus:border-emerald-500 outline-none"
                >
                  {DIET_TYPES.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
                </select>
              </div>
            </div>

            {/* Flights */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-slate-200 flex items-center gap-2 border-b border-slate-800 pb-2">
                <Plane className="w-5 h-5 text-indigo-500"/> Flights (Past Year)
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm text-slate-400">Short Haul (&lt; 3 hours)</label>
                  <input
                    type="number" min="0"
                    value={formData.flights_short}
                    onChange={e => setFormData({...formData, flights_short: Number(e.target.value)})}
                    className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-slate-200 focus:border-emerald-500 outline-none"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm text-slate-400">Long Haul (&gt; 3 hours)</label>
                  <input
                    type="number" min="0"
                    value={formData.flights_long}
                    onChange={e => setFormData({...formData, flights_long: Number(e.target.value)})}
                    className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-slate-200 focus:border-emerald-500 outline-none"
                  />
                </div>
              </div>
            </div>

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <Button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-700 h-12 text-lg" disabled={loading}>
              {loading ? "Calculating..." : "Calculate Impact"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
