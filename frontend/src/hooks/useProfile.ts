import { useState } from 'react';
import { api } from '../services/api';
import { useAuth } from './useAuth';

export interface Profile {
  id?: string;
  name: string;
  email: string;
  city: string;
  transport_type: string;
  avg_travel_distance: number;
  diet_type: string;
  household_size: number;
  eco_points?: number;
}

export function useProfile() {
  const { user, profile, setProfile } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchProfile = async () => {
    // Left for compatibility, but primarily handled by AuthContext now
    if (!user) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.get('/profile');
      setProfile(data);
    } catch (err) {
      setError(err.message || 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (updates: Partial<Profile>) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.put('/profile', updates);
      setProfile(data);
      return data;
    } catch (err) {
      setError(err.message || 'Failed to update profile');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { profile, loading, error, fetchProfile, updateProfile };
}
