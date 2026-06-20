import { Activity, Home, ShieldAlert, Sparkles, Trophy, Settings } from 'lucide-react';

export const VEHICLE_TYPES = [
  { value: 'car_petrol', label: 'Car (Petrol)' },
  { value: 'car_diesel', label: 'Car (Diesel)' },
  { value: 'car_electric', label: 'Car (Electric)' },
  { value: 'motorcycle', label: 'Motorcycle' },
  { value: 'bus', label: 'Bus' },
  { value: 'train', label: 'Train' },
  { value: 'bicycle', label: 'Bicycle' },
  { value: 'walk', label: 'Walk' },
];

export const DIET_TYPES = [
  { value: 'meat_heavy', label: 'Meat Heavy' },
  { value: 'average', label: 'Average' },
  { value: 'vegetarian', label: 'Vegetarian' },
  { value: 'vegan', label: 'Vegan' },
];

export const CARBON_SCORE_LEVELS = [
  { min: 0, max: 30, label: 'Green Hero', color: 'text-emerald-500', bg: 'bg-emerald-500/20' },
  { min: 31, max: 60, label: 'Eco Aware', color: 'text-amber-500', bg: 'bg-amber-500/20' },
  { min: 61, max: 80, label: 'High Impact', color: 'text-orange-500', bg: 'bg-orange-500/20' },
  { min: 81, max: 100, label: 'Critical', color: 'text-red-500', bg: 'bg-red-500/20' },
];

export const NAV_ITEMS = [
  { path: '/dashboard', label: 'Dashboard', icon: Home },
  { path: '/calculator', label: 'Calculator', icon: Activity },
  { path: '/ai-coach', label: 'AI Coach', icon: Sparkles },
  { path: '/eco-twin', label: 'Eco Twin', icon: ShieldAlert },
  { path: '/challenges', label: 'Challenges', icon: Trophy },
  { path: '/profile', label: 'Profile', icon: Settings },
];
