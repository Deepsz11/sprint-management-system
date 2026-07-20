import {
  BarChart3,
  Briefcase,
  Building2,
  Gauge,
  LayoutDashboard,
  ListChecks,
  Target,
  Timer,
  Trophy,
  UserCog,
  Users,
  Users2,
  type LucideIcon,
} from "lucide-react";

import { ROUTES, type AppRoute } from "./routes";

export interface NavigationItem {
  readonly label: string;
  readonly path: AppRoute;
  readonly icon: LucideIcon;
}

export const PRIMARY_NAVIGATION: readonly NavigationItem[] = [
  { label: "Dashboard", path: ROUTES.DASHBOARD, icon: LayoutDashboard },
  { label: "Organizations", path: ROUTES.ORGANIZATIONS, icon: Building2 },
  { label: "Teams", path: ROUTES.TEAMS, icon: Users2 },
  { label: "Users", path: ROUTES.USERS, icon: Users },
  { label: "Projects", path: ROUTES.PROJECTS, icon: Briefcase },
  { label: "Sprints", path: ROUTES.SPRINTS, icon: Timer },
  { label: "Work Items", path: ROUTES.WORK_ITEMS, icon: ListChecks },
  { label: "Business Outcomes", path: ROUTES.BUSINESS_OUTCOMES, icon: Target },
  { label: "KPIs", path: ROUTES.KPIS, icon: Gauge },
  { label: "OKRs", path: ROUTES.OKRS, icon: Trophy },
  { label: "Reports", path: ROUTES.REPORTS, icon: BarChart3 },
] as const;

export const SECONDARY_NAVIGATION: readonly NavigationItem[] = [
  { label: "Profile", path: ROUTES.PROFILE, icon: UserCog },
] as const;