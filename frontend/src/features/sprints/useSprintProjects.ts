import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { sprintsApi } from "./sprintsApi";
import type { SprintProjectOption } from "./types";

interface UseSprintProjectsResult {
  readonly projects: SprintProjectOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useSprintProjects(): UseSprintProjectsResult {
  const [projects, setProjects] = useState<SprintProjectOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await sprintsApi.listProjects();
        if (!cancelled) setProjects(result.items);
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

  return { projects, isLoading, error };
}