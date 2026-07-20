import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { usersApi } from "./usersApi";
import type { UserTeamOption } from "./types";

interface UseTeamOptionsResult {
  readonly teams: UserTeamOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useTeamOptions(): UseTeamOptionsResult {
  const [teams, setTeams] = useState<UserTeamOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await usersApi.listTeams();
        if (!cancelled) setTeams(result.items);
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

  return { teams, isLoading, error };
}