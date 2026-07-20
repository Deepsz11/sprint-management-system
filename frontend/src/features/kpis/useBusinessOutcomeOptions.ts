import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { kpisApi } from "./kpisApi";
import type { KPIOutcomeOption } from "./types";

interface UseBusinessOutcomeOptionsResult {
  readonly outcomes: KPIOutcomeOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useBusinessOutcomeOptions(): UseBusinessOutcomeOptionsResult {
  const [outcomes, setOutcomes] = useState<KPIOutcomeOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await kpisApi.listOutcomes();
        if (!cancelled) setOutcomes(result.items);
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

  return { outcomes, isLoading, error };
}