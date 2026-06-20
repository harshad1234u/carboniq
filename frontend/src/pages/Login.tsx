import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Leaf } from 'lucide-react';
import { supabase } from '../lib/supabase';

export function Login() {
  const { user, signInWithGoogle } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSignUp, setIsSignUp] = useState(false);

  if (user) {
    return <Navigate to="/dashboard" />;
  }

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (isSignUp) {
        const { error: signUpError } = await supabase.auth.signUp({ email, password });
        if (signUpError) throw signUpError;
        alert('Check your email for the confirmation link.');
      } else {
        const { error: signInError } = await supabase.auth.signInWithPassword({ email, password });
        if (signInError) throw signInError;
      }
    } catch (err: unknown) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="mb-8 flex items-center gap-2 relative z-10">
        <Leaf className="w-8 h-8 text-emerald-500" />
        <span className="text-3xl font-bold text-white tracking-tight">CarbonIQ</span>
      </div>

      <Card className="w-full max-w-md bg-slate-900/80 backdrop-blur-xl border-slate-800 shadow-2xl relative z-10">
        <CardHeader className="text-center pb-2">
          <CardTitle className="text-2xl text-white">Welcome back</CardTitle>
          <CardDescription className="text-slate-400">Sign in to continue your green journey</CardDescription>
        </CardHeader>
        <CardContent>
          <Button 
            variant="outline" 
            className="w-full mb-6 bg-white text-slate-900 hover:bg-slate-100 border-0 h-12 text-base font-medium"
            onClick={() => signInWithGoogle().catch(e => setError(e.message))}
          >
            <svg className="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
            </svg>
            Continue with Google
          </Button>

          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-800"></div>
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-slate-900 px-2 text-slate-500">Or continue with</span>
            </div>
          </div>

          <form onSubmit={handleEmailAuth} className="space-y-4">
            <div>
              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white placeholder:text-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all"
                required
              />
            </div>
            <div>
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-950 border border-slate-800 text-white placeholder:text-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition-all"
                required
              />
            </div>
            
            {error && <p className="text-red-500 text-sm">{error}</p>}

            <Button 
              type="submit" 
              className="w-full bg-emerald-600 hover:bg-emerald-700 h-12 text-base font-medium"
              disabled={loading}
            >
              {loading ? "Please wait..." : (isSignUp ? "Sign Up" : "Sign In")}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-slate-400">
            {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
            <button 
              onClick={() => setIsSignUp(!isSignUp)}
              className="text-emerald-500 hover:text-emerald-400 font-medium underline-offset-4 hover:underline transition-all"
            >
              {isSignUp ? "Sign in" : "Sign up"}
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
