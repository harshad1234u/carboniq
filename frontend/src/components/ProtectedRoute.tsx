import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { LoadingSkeleton } from './LoadingSkeleton';
import { Button } from './ui/button';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireProfile?: boolean;
}

export function ProtectedRoute({ children, requireProfile = true }: ProtectedRouteProps) {
  const { user, loading, isProfileComplete, authError, refreshProfile } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-emerald-500">
        <LoadingSkeleton variant="dashboard" />
        <p className="mt-4 animate-pulse font-medium text-slate-400">Loading your green journey...</p>
      </div>
    );
  }

  // If there's an authError and we REQUIRE a profile (e.g. Dashboard), show error state with retry.
  // We do NOT show an error for onboarding, because onboarding doesn't require a profile.
  if (authError && requireProfile) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-center">
        <AlertCircle className="w-16 h-16 text-red-500 mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Failed to Load Profile</h2>
        <p className="text-slate-400 mb-6 max-w-md">{authError}</p>
        <Button 
          onClick={() => refreshProfile()}
          className="bg-emerald-600 hover:bg-emerald-700 flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" /> Try Again
        </Button>
      </div>
    );
  }

  // Wait, if it's NOT loading, AND there's NO user, we MUST have checked auth state already.
  // The AuthContext initializes with loading=true.
  if (!user) {
    console.log("Redirect decision: User not authenticated");
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (requireProfile && isProfileComplete === false) {
    console.log("Redirect decision: Profile missing");
    console.log("Redirecting to onboarding");
    return <Navigate to="/onboarding" replace />;
  }

  if (requireProfile) {
    console.log("Redirect decision: Dashboard access granted");
  }

  return <>{children}</>;
}
