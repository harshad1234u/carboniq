import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { LoadingSkeleton } from './LoadingSkeleton';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireProfile?: boolean;
}

export function ProtectedRoute({ children, requireProfile = true }: ProtectedRouteProps) {
  const { user, loading, isProfileComplete } = useAuth();

  if (loading || isProfileComplete === null) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
        <LoadingSkeleton variant="dashboard" />
      </div>
    );
  }

  if (!user) {
    console.log("Redirect decision: User not authenticated");
    return <Navigate to="/login" />;
  }

  if (requireProfile && !isProfileComplete) {
    console.log("Redirect decision: Profile missing");
    console.log("Redirecting to onboarding");
    return <Navigate to="/onboarding" />;
  }

  if (requireProfile) {
    console.log("Redirect decision: Dashboard access granted");
  }

  return <>{children}</>;
}
