import React, { createContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { supabase } from '../lib/supabase';
import type { User, Session } from '@supabase/supabase-js';
import { api } from '../services/api';
import type { Profile } from '../hooks/useProfile';

interface AuthContextType {
  user: User | null;
  session: Session | null;
  loading: boolean;
  isProfileComplete: boolean | null;
  profile: Profile | null;
  authError: string | null;
  setIsProfileComplete: (complete: boolean) => void;
  setProfile: (profile: Profile | null) => void;
  refreshProfile: () => Promise<void>;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [isProfileComplete, setIsProfileComplete] = useState<boolean | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);

  const hasCheckedProfile = React.useRef<string | null>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      if (session?.user) {
        if (hasCheckedProfile.current !== session.user.id) {
          hasCheckedProfile.current = session.user.id;
          checkProfile(session.user.id);
        }
      } else {
        setLoading(false);
      }
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      console.log("Auth state changed:", _event);
      setSession(session);
      setUser(session?.user ?? null);
      
      if (session?.user) {
        if (_event === 'INITIAL_SESSION' || _event === 'SIGNED_IN') {
          if (hasCheckedProfile.current !== session.user.id) {
            hasCheckedProfile.current = session.user.id;
            checkProfile(session.user.id);
          }
        }
      } else {
        hasCheckedProfile.current = null;
        setIsProfileComplete(null);
        setProfile(null);
        setLoading(false);
        setAuthError(null);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const checkProfile = async (userId: string) => {
    console.log("Profile lookup started for", userId);
    setLoading(true);
    setAuthError(null);
    
    // Safety timeout of 10s
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Profile request timed out')), 10000);
    });

    try {
      const prof = await Promise.race([api.get('/profile'), timeoutPromise]) as Profile;
      console.log("Profile found");
      setProfile(prof);
      setIsProfileComplete(!!prof.city);
    } catch (err: any) {
      if (err.message === 'Profile not found' || err.message?.includes('not found') || err.message?.includes('404')) {
        console.log("Profile missing - redirecting to onboarding");
        setIsProfileComplete(false);
        setProfile(null);
        setAuthError(null);
      } else {
        console.error('Error checking profile:', err);
        setIsProfileComplete(null); 
        setProfile(null);
        setAuthError(err.message || "Failed to load profile");
      }
    } finally {
      setLoading(false);
    }
  };

  const refreshProfile = async () => {
    if (user) {
      await checkProfile(user.id);
    }
  };

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/dashboard`
      }
    });
    if (error) throw error;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  };

  return (
    <AuthContext.Provider value={{ user, session, loading, isProfileComplete, profile, authError, setIsProfileComplete, setProfile, refreshProfile, signInWithGoogle, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}
