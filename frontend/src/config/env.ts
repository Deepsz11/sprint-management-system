interface AppEnv {
  readonly API_BASE_URL: string;
  readonly APP_NAME: string;
  readonly STORAGE_PREFIX: string;
}

function readEnv(key: string, fallback: string): string {
  const value = import.meta.env[key as keyof ImportMetaEnv] as
    | string
    | undefined;
  return value && value.length > 0 ? value : fallback;
}

export const ENV: AppEnv = {
  API_BASE_URL: readEnv("VITE_API_BASE_URL", "/api/v1"),
  APP_NAME: readEnv("VITE_APP_NAME", "Sprint Business Outcome Tracer"),
  STORAGE_PREFIX: readEnv("VITE_STORAGE_PREFIX", "sbot"),
};