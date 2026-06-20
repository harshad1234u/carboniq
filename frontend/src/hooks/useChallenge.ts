import { useState, useEffect } from 'react';
import { api } from '../services/api';

export function useChallenge() {
  const [challenges, setChallenges] = useState<any[]>([]);
  const [badges, setBadges] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchChallenges = async () => {
    setLoading(true);
    try {
      const data = await api.get('/challenges');
      setChallenges(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load challenges');
    } finally {
      setLoading(false);
    }
  };

  const completeChallenge = async (id: string) => {
    try {
      const data = await api.post(`/challenges/${id}/complete`, {});
      await fetchChallenges();
      await fetchBadges();
      return data;
    } catch (err: any) {
      throw err;
    }
  };

  const fetchBadges = async () => {
    try {
      const data = await api.get('/badges');
      setBadges(data);
    } catch (err: any) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchChallenges();
    fetchBadges();
  }, []);

  return { challenges, badges, loading, error, completeChallenge, refresh: fetchChallenges };
}
