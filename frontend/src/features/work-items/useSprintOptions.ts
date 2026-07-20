import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { workItemsApi } from "./workItemsApi";
import type { WorkItemProjectOption, WorkItemSprintOption } from "./types";

interface UseSprintOptionsResult {
  readonly projects: WorkItemProjectOption[];
  readonly sprints: WorkItemSprintOption[];
  readonly isLoadingProjects: boolean;
  readonly isLoadingSprints: boolean;
  readonly error: ApiError | null;
}

export function useSprintOptions(
  projectId: string | null,
): UseSprintOptionsResult {
  const [projects, setProjects] = useState<WorkItemProjectOption[]>([]);
  const [sprints, setSprints] = useState<WorkItemSprintOption[]>([]);
  const [isLoadingProjects, setIsLoadingProjects] = useState<boolean>(true);
  const [isLoadingSprints, setIsLoadingSprints] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoadingProjects(true);
      setError(null);
      try {
        const result = await workItemsApi.listProjects();
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
    if (!projectId) {
      setSprints([]);
      setIsLoadingSprints(false);
      return () => {
        cancelled = true;
      };
    }
    void (async () => {
      setIsLoadingSprints(true);
      setError(null);
      try {
        const result = await workItemsApi.listSprints(projectId);
        if (!cancelled) setSprints(result.items);
      } catch (err) {
        if (!cancelled) setError(toApiError(err));
      } finally {
        if (!cancelled) setIsLoadingSprints(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [projectId]);

  return {
    projects,
    sprints,
    isLoadingProjects,
    isLoadingSprints,
    error,
  };
}