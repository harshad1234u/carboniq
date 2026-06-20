import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useProfile } from '../hooks/useProfile';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { VEHICLE_TYPES, DIET_TYPES } from '../utils/constants';
import { MapPin, Users, Car, Utensils } from 'lucide-react';

export function Onboarding() {
  const { user, isProfileComplete, refreshProfile } = useAuth();
  const { updateProfile } = useProfile();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.user_metadata?.full_name || '',
    city: '',
    transport_type: 'car_petrol',
    avg_travel_distance: 10,
    diet_type: 'average',
    household_size: 1
  });

  if (!user) return <Navigate to="/login" />;
  if (isProfileComplete) return <Navigate to="/dashboard" />;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    console.log("Creating profile");
    try {
      await updateProfile(formData);
      console.log("Profile created successfully via API");
      
      await refreshProfile();
      console.log("Profile row verified via global state refresh");
      
      navigate('/dashboard');
    } catch (err: any) {
      alert(err.message || 'Failed to save profile');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <Card className="w-full max-w-xl bg-slate-900/80 border-slate-800">
        <CardHeader className="text-center pb-6">
          <CardTitle className="text-3xl text-white mb-2">Welcome to CarbonIQ</CardTitle>
          <CardDescription className="text-base text-slate-400">
            Let's personalize your experience. This info helps us provide accurate carbon tracking.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={e => setFormData({...formData, name: e.target.value})}
                  className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-emerald-500"/> City
                </label>
                <input
                  type="text"
                  value={formData.city}
                  onChange={e => setFormData({...formData, city: e.target.value})}
                  className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                  placeholder="e.g. Mumbai, New York"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                  <Car className="w-4 h-4 text-emerald-500"/> Primary Transport
                </label>
                <select
                  value={formData.transport_type}
                  onChange={e => setFormData({...formData, transport_type: e.target.value})}
                  className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                >
                  {VEHICLE_TYPES.map(v => <option key={v.value} value={v.value}>{v.label}</option>)}
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                  <Utensils className="w-4 h-4 text-emerald-500"/> Diet Type
                </label>
                <select
                  value={formData.diet_type}
                  onChange={e => setFormData({...formData, diet_type: e.target.value})}
                  className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                >
                  {DIET_TYPES.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">Daily Travel (km)</label>
                <input
                  type="number"
                  min="0"
                  value={formData.avg_travel_distance}
                  onChange={e => setFormData({...formData, avg_travel_distance: parseInt(e.target.value) || 0})}
                  className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300 flex items-center gap-2">
                  <Users className="w-4 h-4 text-emerald-500"/> Household Size
                </label>
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={formData.household_size}
                  onChange={e => setFormData({...formData, household_size: parseInt(e.target.value) || 1})}
                  className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                />
              </div>
            </div>

            <Button 
              type="submit" 
              className="w-full bg-emerald-600 hover:bg-emerald-700 h-12 text-base font-medium mt-8"
              disabled={loading}
            >
              {loading ? "Saving..." : "Complete Setup"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
