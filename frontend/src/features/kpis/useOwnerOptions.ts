import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { kpisApi } from "./kpisApi";
import type { KPIOwnerOption } from "./types";

interface UseOwnerOptionsResult {
  readonly owners: KPIOwnerOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useOwnerOptions(): UseOwnerOptionsResult {
  const [owners, setOwners] = useState<KPIOwnerOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await kpisApi.listOwners();
        if (!cancelled) setOwners(result.items);
      } catch (err) {
        if (!cancelled) setError(toApiError(err));
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return { owners, isLoading, error };
}