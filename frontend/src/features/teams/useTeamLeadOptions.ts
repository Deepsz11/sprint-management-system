import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { teamsApi } from "./teamsApi";
import type { TeamLeadOption } from "./types";

interface UseTeamLeadOptionsResult {
  readonly leads: TeamLeadOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useTeamLeadOptions(): UseTeamLeadOptionsResult {
  const [leads, setLeads] = useState<TeamLeadOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await teamsApi.listLeads();
        if (!cancelled) setLeads(result.items);
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

  return { leads, isLoading, error };
}