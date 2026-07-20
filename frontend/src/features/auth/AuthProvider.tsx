import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { onUnauthorized } from "@/api/client";
import { toApiError } from "@/api/errors";
import { tokenStorage } from "@/lib/tokens";

import { AuthContext, type AuthContextValue } from "./AuthContext";
import { authApi } from "./authApi";
import type { AuthUser, LoginCredentials } from "./types";

interface AuthProviderProps {
  readonly children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isInitializing, setIsInitializing] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const mounted = useRef<boolean>(true);

  const refreshCurrentUser = useCallback(async () => {
    const token = tokenStorage.getAccessToken();
    if (!token) {
      setUser(null);
      return;
    }
    try {
      const me = await authApi.me();
      if (mounted.current) setUser(me);
    } catch {
      tokenStorage.clear();
      if (mounted.current) setUser(null);
    }
  }, []);

  useEffect(() => {
    mounted.current = true;
    void (async () => {
      await refreshCurrentUser();
      if (mounted.current) setIsInitializing(false);
    })();
    return () => {
      mounted.current = false;
    };
  }, [refreshCurrentUser]);

  useEffect(() => {
    const off = onUnauthorized(() => {
      tokenStorage.clear();
      setUser(null);
    });
    return off;
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setIsSubmitting(true);
    try {
      const tokens = await authApi.login(credentials);
      tokenStorage.setTokens(tokens.access_token, tokens.refresh_token);
      const me = await authApi.me();
      setUser(me);
    } catch (error) {
      throw toApiError(error);
    } finally {
      setIsSubmitting(false);
    }
  }, []);

  const logout = useCallback(async () => {
    const refreshToken = tokenStorage.getRefreshToken();
    try {
      if (refreshToken) {
        await authApi.logout(refreshToken);
      }
    } catch {
      /* best-effort logout */
    } finally {
      tokenStorage.clear();
      setUser(null);
    }
  }, []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: user !== null,
      isInitializing,
      isSubmitting,
      login,
      logout,
      refreshCurrentUser,
    }),
    [user, isInitializing, isSubmitting, login, logout, refreshCurrentUser],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}