import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { teamsApi } from "./teamsApi";
import type { TeamOrganizationOption } from "./types";

interface UseOrganizationOptionsResult {
  readonly organizations: TeamOrganizationOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useOrganizationOptions(): UseOrganizationOptionsResult {
  const [organizations, setOrganizations] = useState<TeamOrganizationOption[]>(
    [],
  );
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await teamsApi.listOrganizations();
        if (!cancelled) setOrganizations(result.items);
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

  return { organizations, isLoading, error };
}