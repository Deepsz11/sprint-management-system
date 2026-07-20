import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { usersApi } from "./usersApi";
import type { UserOrganizationOption } from "./types";

interface UseOrganizationOptionsResult {
  readonly organizations: UserOrganizationOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useOrganizationOptions(): UseOrganizationOptionsResult {
  const [organizations, setOrganizations] = useState<UserOrganizationOption[]>(
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
        const result = await usersApi.listOrganizations();
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