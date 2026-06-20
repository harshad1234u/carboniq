-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Profiles table (links to auth.users)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  city TEXT NOT NULL,
  transport_type TEXT NOT NULL,
  avg_travel_distance NUMERIC DEFAULT 0,
  diet_type TEXT NOT NULL DEFAULT 'average',
  household_size INTEGER DEFAULT 1,
  eco_points INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Carbon Entries table
CREATE TABLE IF NOT EXISTS carbon_entries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  vehicle_type TEXT,
  daily_travel_km NUMERIC DEFAULT 0,
  electricity_kwh NUMERIC DEFAULT 0,
  ac_hours NUMERIC DEFAULT 0,
  diet_type TEXT DEFAULT 'average',
  flights_short INTEGER DEFAULT 0,
  flights_long INTEGER DEFAULT 0,
  transport_emissions NUMERIC NOT NULL,
  electricity_emissions NUMERIC NOT NULL,
  food_emissions NUMERIC NOT NULL,
  flight_emissions NUMERIC NOT NULL,
  total_emissions NUMERIC NOT NULL,
  carbon_score INTEGER,
  carbon_level TEXT,
  recorded_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Recommendations table
CREATE TABLE IF NOT EXISTS recommendations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  entry_id UUID REFERENCES carbon_entries(id) ON DELETE CASCADE,
  recommendations JSONB NOT NULL,
  weather_context JSONB,
  total_co2_savings NUMERIC,
  total_cost_savings NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Eco Twin Predictions table
CREATE TABLE IF NOT EXISTS eco_predictions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  entry_id UUID REFERENCES carbon_entries(id) ON DELETE CASCADE,
  current_footprint NUMERIC NOT NULL,
  predicted_footprint NUMERIC NOT NULL,
  reduction_percentage NUMERIC NOT NULL,
  impact_equivalents JSONB,
  recommendation_impacts JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Challenges table
CREATE TABLE IF NOT EXISTS challenges (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  eco_points INTEGER DEFAULT 10,
  is_completed BOOLEAN DEFAULT FALSE,
  week_start DATE DEFAULT DATE_TRUNC('week', CURRENT_DATE),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Badges table
CREATE TABLE IF NOT EXISTS badges (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profile_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  badge_name TEXT NOT NULL,
  badge_description TEXT,
  earned_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE carbon_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE eco_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE challenges ENABLE ROW LEVEL SECURITY;
ALTER TABLE badges ENABLE ROW LEVEL SECURITY;

-- Policies for Profiles
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- Policies for Carbon Entries
CREATE POLICY "Users can view own entries" ON carbon_entries FOR SELECT USING (auth.uid() = profile_id);
CREATE POLICY "Users can insert own entries" ON carbon_entries FOR INSERT WITH CHECK (auth.uid() = profile_id);

-- Policies for Recommendations
CREATE POLICY "Users can view own recs" ON recommendations FOR SELECT USING (auth.uid() = profile_id);
CREATE POLICY "Users can insert own recs" ON recommendations FOR INSERT WITH CHECK (auth.uid() = profile_id);

-- Policies for Eco Predictions
CREATE POLICY "Users can view own predictions" ON eco_predictions FOR SELECT USING (auth.uid() = profile_id);
CREATE POLICY "Users can insert own predictions" ON eco_predictions FOR INSERT WITH CHECK (auth.uid() = profile_id);

-- Policies for Challenges
CREATE POLICY "Users can view own challenges" ON challenges FOR SELECT USING (auth.uid() = profile_id);
CREATE POLICY "Users can insert own challenges" ON challenges FOR INSERT WITH CHECK (auth.uid() = profile_id);
CREATE POLICY "Users can update own challenges" ON challenges FOR UPDATE USING (auth.uid() = profile_id);

-- Policies for Badges
CREATE POLICY "Users can view own badges" ON badges FOR SELECT USING (auth.uid() = profile_id);
CREATE POLICY "Users can insert own badges" ON badges FOR INSERT WITH CHECK (auth.uid() = profile_id);
