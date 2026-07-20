import { Navigate } from "react-router-dom";

import { PageLoader } from "@/components/ui/PageLoader";
import { ROUTES } from "@/config/routes";
import { useAuth } from "@/features/auth/useAuth";

interface PublicRouteProps {
  readonly children: React.ReactNode;
}

export function PublicRoute({ children }: PublicRouteProps) {
  const { isAuthenticated, isInitializing } = useAuth();

  if (isInitializing) {
    return <PageLoader />;
  }

  if (isAuthenticated) {
    return <Navigate to={ROUTES.DASHBOARD} replace />;
  }

  return <>{children}</>;
}