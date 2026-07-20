import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { businessOutcomesApi } from "./businessOutcomesApi";
import type { OutcomeKpiOption } from "./types";

interface UseKpiOptionsResult {
  readonly kpis: OutcomeKpiOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useKpiOptions(outcomeId?: string): UseKpiOptionsResult {
  const [kpis, setKpis] = useState<OutcomeKpiOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await businessOutcomesApi.listKpis(outcomeId);
        if (!cancelled) setKpis(result.items);
      } catch (err) {
        if (!cancelled) setError(toApiError(err));
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [outcomeId]);

  return { kpis, isLoading, error };
}