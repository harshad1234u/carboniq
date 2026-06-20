import { useState } from 'react';
import { api } from '../services/api';

export function useCarbon() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any | null>(null);

  const calculate = async (input: unknown) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.post('/carbon/calculate', input);
      setResult(data);
      return data;
    } catch (err) {
      setError(err.message || 'Failed to calculate emissions');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getDashboardSummary = async () => {
    setLoading(true);
    setError(null);
    try {
      return await api.get('/dashboard/summary');
    } catch (err) {
      setError(err.message || 'Failed to load dashboard summary');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getAiRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      return await api.post('/carbon/ai-coach', {});
    } catch (err) {
      setError(err.message || 'Failed to get AI recommendations');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const getEcoTwin = async () => {
    setLoading(true);
    setError(null);
    try {
      return await api.post('/carbon/eco-twin', { entry_id: '' });
    } catch (err) {
      setError(err.message || 'Failed to generate Eco Twin');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, result, calculate, getDashboardSummary, getAiRecommendations, getEcoTwin };
}
