import { useState, useEffect } from 'react';
import { useProfile } from '../hooks/useProfile';
import { useAuth } from '../hooks/useAuth';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { VEHICLE_TYPES, DIET_TYPES } from '../utils/constants';
import { LoadingSkeleton } from '../components/LoadingSkeleton';

export function Profile() {
  const { user } = useAuth();
  const { profile, updateProfile, loading: profileLoading } = useProfile();
  
  const [formData, setFormData] = useState({
    name: '',
    city: '',
    transport_type: 'car_petrol',
    avg_travel_distance: 10,
    diet_type: 'average',
    household_size: 1
  });
  
  const [isSaving, setIsSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    if (profile) {
      setFormData({
        name: profile.name || '',
        city: profile.city || '',
        transport_type: profile.transport_type || 'car_petrol',
        avg_travel_distance: profile.avg_travel_distance || 10,
        diet_type: profile.diet_type || 'average',
        household_size: profile.household_size || 1
      });
    }
  }, [profile]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setSuccessMsg('');
    try {
      await updateProfile(formData);
      setSuccessMsg('Profile updated successfully!');
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err: any) {
      alert(err.message || 'Failed to update profile');
    } finally {
      setIsSaving(false);
    }
  };

  if (profileLoading && !profile) return <LoadingSkeleton variant="card" />;

  return (
    <div className="max-w-2xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">Profile Settings</h1>
        <p className="text-slate-400">Manage your personal information and preferences.</p>
      </div>

      <Card className="bg-slate-900/50 border-slate-800">
        <CardHeader>
          <CardTitle>Account Details</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 mb-8">
            <div>
              <label className="text-sm text-slate-400 block mb-1">Email</label>
              <div className="p-3 bg-slate-950 rounded-md border border-slate-800 text-slate-300">
                {user?.email}
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={e => setFormData({...formData, name: e.target.value})}
                  className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 outline-none"
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">City</label>
                <input
                  type="text"
                  value={formData.city}
                  onChange={e => setFormData({...formData, city: e.target.value})}
                  className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 outline-none"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">Primary Transport</label>
                <select
                  value={formData.transport_type}
                  onChange={e => setFormData({...formData, transport_type: e.target.value})}
                  className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 outline-none"
                >
                  {VEHICLE_TYPES.map(v => <option key={v.value} value={v.value}>{v.label}</option>)}
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">Daily Travel (km)</label>
                <input
                  type="number" min="0"
                  value={formData.avg_travel_distance}
                  onChange={e => setFormData({...formData, avg_travel_distance: parseInt(e.target.value) || 0})}
                  className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 outline-none"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">Diet Type</label>
                <select
                  value={formData.diet_type}
                  onChange={e => setFormData({...formData, diet_type: e.target.value})}
                  className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 outline-none"
                >
                  {DIET_TYPES.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-300">Household Size</label>
                <input
                  type="number" min="1" max="20"
                  value={formData.household_size}
                  onChange={e => setFormData({...formData, household_size: parseInt(e.target.value) || 1})}
                  className="w-full p-2.5 rounded-md bg-slate-950 border border-slate-800 text-white focus:border-emerald-500 outline-none"
                />
              </div>
            </div>

            {successMsg && <p className="text-emerald-500 text-sm font-medium">{successMsg}</p>}

            <Button type="submit" className="w-full md:w-auto bg-emerald-600 hover:bg-emerald-700" disabled={isSaving}>
              {isSaving ? "Saving..." : "Save Changes"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
