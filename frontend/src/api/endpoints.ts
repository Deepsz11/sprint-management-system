export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: "/auth/login",
    REFRESH: "/auth/token/refresh",
    LOGOUT: "/auth/logout",
    LOGOUT_ALL: "/auth/logout-all",
    ME: "/auth/me",
    SESSIONS: "/auth/sessions",
    CHANGE_PASSWORD: "/auth/password/change",
  },
  ORGANIZATIONS: "/organizations",
  TEAMS: "/teams",
  USERS: "/users",
  PROJECTS: "/projects",
  SPRINTS: "/sprints",
  WORK_ITEMS: "/work-items",
  BUSINESS_OUTCOMES: "/business-outcomes",
  KPIS: "/kpis",
} as const;