import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { businessOutcomesApi } from "./businessOutcomesApi";
import type { OutcomeOwnerOption, OutcomeProjectOption } from "./types";

interface UseProjectOptionsResult {
  readonly projects: OutcomeProjectOption[];
  readonly owners: OutcomeOwnerOption[];
  readonly isLoadingProjects: boolean;
  readonly isLoadingOwners: boolean;
  readonly error: ApiError | null;
}

export function useProjectOptions(): UseProjectOptionsResult {
  const [projects, setProjects] = useState<OutcomeProjectOption[]>([]);
  const [owners, setOwners] = useState<OutcomeOwnerOption[]>([]);
  const [isLoadingProjects, setIsLoadingProjects] = useState<boolean>(true);
  const [isLoadingOwners, setIsLoadingOwners] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoadingProjects(true);
      try {
        const result = await businessOutcomesApi.listProjects();
        if (!cancelled) setProjects(result.items);
      } catch (err) {
        if (!cancelled) setError(toApiError(err));
      } finally {
        if (!cancelled) setIsLoadingProjects(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoadingOwners(true);
      try {
        const result = await businessOutcomesApi.listOwners();
        if (!cancelled) setOwners(result.items);
      } catch (err) {
        if (!cancelled) setError(toApiError(err));
      } finally {
        if (!cancelled) setIsLoadingOwners(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return {
    projects,
    owners,
    isLoadingProjects,
    isLoadingOwners,
    error,
  };
}