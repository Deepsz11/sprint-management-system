import { storage } from "./storage";

const ACCESS_KEY = "auth.access_token";
const REFRESH_KEY = "auth.refresh_token";

export const tokenStorage = {
  getAccessToken(): string | null {
    return storage.get<string>(ACCESS_KEY);
  },
  getRefreshToken(): string | null {
    return storage.get<string>(REFRESH_KEY);
  },
  setTokens(access: string, refresh: string): void {
    storage.set(ACCESS_KEY, access);
    storage.set(REFRESH_KEY, refresh);
  },
  clear(): void {
    storage.remove(ACCESS_KEY);
    storage.remove(REFRESH_KEY);
  },
};