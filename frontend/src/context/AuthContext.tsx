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
  setIsProfileComplete: (complete: boolean) => void;
  setProfile: (profile: Profile | null) => void;
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
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const checkProfile = async (userId: string) => {
    console.log("Profile lookup started for", userId);
    try {
      const prof = await api.get('/profile');
      console.log("Profile found");
      setProfile(prof);
      setIsProfileComplete(!!prof.city);
    } catch (err: any) {
      if (err.message === 'Profile not found' || err.message?.includes('not found') || err.message?.includes('404')) {
        console.log("Profile missing");
        setIsProfileComplete(false);
        setProfile(null);
      } else {
        console.error('Error checking profile:', err);
        setIsProfileComplete(false); 
        setProfile(null);
      }
    } finally {
      setLoading(false);
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
    <AuthContext.Provider value={{ user, session, loading, isProfileComplete, profile, setIsProfileComplete, setProfile, signInWithGoogle, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}
