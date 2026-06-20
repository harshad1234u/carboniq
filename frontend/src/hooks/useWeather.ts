import { useState } from 'react';
import { api } from '../services/api';

export function useWeather() {
  const [weather, setWeather] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchWeather = async (city: string) => {
    if (!city) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.get(`/carbon/weather/${encodeURIComponent(city)}`);
      setWeather(data);
    } catch (err) {
      setError(err.message || 'Failed to load weather');
    } finally {
      setLoading(false);
    }
  };

  return { weather, loading, error, fetchWeather };
}
