import { ENV } from "@/config/env";

const PREFIX = ENV.STORAGE_PREFIX;

function key(name: string): string {
  return `${PREFIX}:${name}`;
}

export const storage = {
  get<T = string>(name: string): T | null {
    try {
      const raw = window.localStorage.getItem(key(name));
      if (raw === null) return null;
      try {
        return JSON.parse(raw) as T;
      } catch {
        return raw as unknown as T;
      }
    } catch {
      return null;
    }
  },
  set(name: string, value: unknown): void {
    try {
      const raw = typeof value === "string" ? value : JSON.stringify(value);
      window.localStorage.setItem(key(name), raw);
    } catch {
      /* storage is best-effort */
    }
  },
  remove(name: string): void {
    try {
      window.localStorage.removeItem(key(name));
    } catch {
      /* storage is best-effort */
    }
  },
  clearAll(): void {
    try {
      const toRemove: string[] = [];
      for (let i = 0; i < window.localStorage.length; i += 1) {
        const k = window.localStorage.key(i);
        if (k && k.startsWith(`${PREFIX}:`)) {
          toRemove.push(k);
        }
      }
      toRemove.forEach((k) => window.localStorage.removeItem(k));
    } catch {
      /* storage is best-effort */
    }
  },
};