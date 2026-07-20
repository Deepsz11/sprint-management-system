import { Suspense, lazy } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "@/components/layout/AppLayout";
import { PageLoader } from "@/components/ui/PageLoader";
import { ROUTES } from "@/config/routes";

import { ProtectedRoute } from "./ProtectedRoute";
import { PublicRoute } from "./PublicRoute";

const LoginPage = lazy(() => import("@/pages/auth/LoginPage"));
const DashboardPage = lazy(() => import("@/pages/dashboard/DashboardPage"));
const NotFoundPage = lazy(() => import("@/pages/NotFoundPage"));
const ModulePlaceholder = lazy(() => import("@/pages/ModulePlaceholder"));
const ProjectsPage = lazy(() => import("@/pages/projects/ProjectsPage"));
const SprintsPage = lazy(() => import("@/pages/sprints/SprintsPage"));
const WorkItemsPage = lazy(() => import("@/pages/work-items/WorkItemsPage"));
const BusinessOutcomesPage = lazy(
  () => import("@/pages/business-outcomes/BusinessOutcomesPage"),
);
const KPIsPage = lazy(() => import("@/pages/kpis/KPIsPage"));
const OrganizationsPage = lazy(
  () => import("@/pages/organizations/OrganizationsPage"),
);
export function AppRouter() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route
            path={ROUTES.ROOT}
            element={<Navigate to={ROUTES.DASHBOARD} replace />}
          />

          <Route
            path={ROUTES.LOGIN}
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />

          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
            <Route path={ROUTES.ORGANIZATIONS} element={<OrganizationsPage />} />
            <Route
              path={ROUTES.TEAMS}
              element={<ModulePlaceholder title="Teams" />}
            />
            <Route
              path={ROUTES.USERS}
              element={<ModulePlaceholder title="Users" />}
            />
            <Route path={ROUTES.PROJECTS} element={<ProjectsPage />} />
            <Route path={ROUTES.SPRINTS} element={<SprintsPage />} />
            <Route path={ROUTES.WORK_ITEMS} element={<WorkItemsPage />} />
            <Route
              path={ROUTES.BUSINESS_OUTCOMES}
              element={<BusinessOutcomesPage />}
            />
            <Route path={ROUTES.KPIS} element={<KPIsPage />} />
            <Route
              path={ROUTES.OKRS}
              element={<ModulePlaceholder title="OKRs" />}
            />
            <Route
              path={ROUTES.REPORTS}
              element={<ModulePlaceholder title="Reports" />}
            />
            <Route
              path={ROUTES.PROFILE}
              element={<ModulePlaceholder title="Profile" />}
            />
          </Route>

          <Route path={ROUTES.NOT_FOUND} element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}