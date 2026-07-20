import { useEffect, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { workItemsApi } from "./workItemsApi";
import type { WorkItemAssigneeOption } from "./types";

interface UseAssigneeOptionsResult {
  readonly assignees: WorkItemAssigneeOption[];
  readonly isLoading: boolean;
  readonly error: ApiError | null;
}

export function useAssigneeOptions(): UseAssigneeOptionsResult {
  const [assignees, setAssignees] = useState<WorkItemAssigneeOption[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await workItemsApi.listUsers();
        if (!cancelled) setAssignees(result.items);
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

  return { assignees, isLoading, error };
}