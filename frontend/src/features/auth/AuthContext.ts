import { createContext } from "react";

import type { AuthUser, LoginCredentials } from "./types";

export interface AuthContextValue {
  readonly user: AuthUser | null;
  readonly isAuthenticated: boolean;
  readonly isInitializing: boolean;
  readonly isSubmitting: boolean;
  readonly login: (credentials: LoginCredentials) => Promise<void>;
  readonly logout: () => Promise<void>;
  readonly refreshCurrentUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
);