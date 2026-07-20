export const ROUTES = {
  ROOT: "/",
  LOGIN: "/login",
  DASHBOARD: "/dashboard",
  ORGANIZATIONS: "/organizations",
  TEAMS: "/teams",
  USERS: "/users",
  PROJECTS: "/projects",
  SPRINTS: "/sprints",
  WORK_ITEMS: "/work-items",
  BUSINESS_OUTCOMES: "/business-outcomes",
  KPIS: "/kpis",
  OKRS: "/okrs",
  REPORTS: "/reports",
  PROFILE: "/profile",
  NOT_FOUND: "*",
} as const;

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES];