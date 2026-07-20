import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { workItemsApi } from "./workItemsApi";
import type {
  CreateWorkItemInput,
  PaginatedWorkItems,
  UpdateWorkItemInput,
  WorkItem,
  WorkItemListParams,
  WorkItemPriority,
  WorkItemStatus,
  WorkItemType,
} from "./types";

interface UseWorkItemsOptions {
  readonly limit: number;
}

export interface WorkItemFilters {
  readonly projectId: string | null;
  readonly sprintId: string | null;
  readonly assigneeId: string | null;
  readonly itemTypes: readonly WorkItemType[];
  readonly statuses: readonly WorkItemStatus[];
  readonly priorities: readonly WorkItemPriority[];
  readonly search: string;
}

interface UseWorkItemsResult {
  readonly data: PaginatedWorkItems | null;
  readonly items: WorkItem[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly filters: WorkItemFilters;
  readonly setProjectId: (value: string | null) => void;
  readonly setSprintId: (value: string | null) => void;
  readonly setAssigneeId: (value: string | null) => void;
  readonly setItemTypes: (values: readonly WorkItemType[]) => void;
  readonly setStatuses: (values: readonly WorkItemStatus[]) => void;
  readonly setPriorities: (values: readonly WorkItemPriority[]) => void;
  readonly setSearch: (value: string) => void;
  readonly setPage: (page: number) => void;
  readonly resetFilters: () => void;
  readonly refresh: () => Promise<void>;
  readonly createWorkItem: (input: CreateWorkItemInput) => Promise<WorkItem>;
  readonly updateWorkItem: (
    id: string,
    input: UpdateWorkItemInput,
  ) => Promise<WorkItem>;
  readonly deleteWorkItem: (id: string) => Promise<void>;
}

const INITIAL_FILTERS: WorkItemFilters = {
  projectId: null,
  sprintId: null,
  assigneeId: null,
  itemTypes: [],
  statuses: [],
  priorities: [],
  search: "",
};

export function useWorkItems(
  options: UseWorkItemsOptions = { limit: 20 },
): UseWorkItemsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedWorkItems | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [filters, setFilters] = useState<WorkItemFilters>(INITIAL_FILTERS);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, currentFilters: WorkItemFilters) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: WorkItemListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
          project_id: currentFilters.projectId ?? undefined,
          sprint_id: currentFilters.sprintId ?? undefined,
          assignee_id: currentFilters.assigneeId ?? undefined,
          item_type:
            currentFilters.itemTypes.length > 0
              ? currentFilters.itemTypes
              : undefined,
          status:
            currentFilters.statuses.length > 0
              ? currentFilters.statuses
              : undefined,
          priority:
            currentFilters.priorities.length > 0
              ? currentFilters.priorities
              : undefined,
          search:
            currentFilters.search.trim().length > 0
              ? currentFilters.search
              : undefined,
        };
        const result = await workItemsApi.list(params);
        if (!mounted.current) return;
        setData(result);
      } catch (err) {
        if (!mounted.current) return;
        setError(toApiError(err));
      } finally {
        if (mounted.current) setIsLoading(false);
      }
    },
    [limit],
  );

  useEffect(() => {
    mounted.current = true;
    void load(page, filters);
    return () => {
      mounted.current = false;
    };
  }, [load, page, filters]);

  const patchFilters = useCallback((patch: Partial<WorkItemFilters>) => {
    setFilters((current) => ({ ...current, ...patch }));
    setPage(1);
  }, []);

  const setProjectId = useCallback(
    (value: string | null) => {
      patchFilters({ projectId: value, sprintId: null });
    },
    [patchFilters],
  );
  const setSprintId = useCallback(
    (value: string | null) => patchFilters({ sprintId: value }),
    [patchFilters],
  );
  const setAssigneeId = useCallback(
    (value: string | null) => patchFilters({ assigneeId: value }),
    [patchFilters],
  );
  const setItemTypes = useCallback(
    (values: readonly WorkItemType[]) => patchFilters({ itemTypes: values }),
    [patchFilters],
  );
  const setStatuses = useCallback(
    (values: readonly WorkItemStatus[]) => patchFilters({ statuses: values }),
    [patchFilters],
  );
  const setPriorities = useCallback(
    (values: readonly WorkItemPriority[]) =>
      patchFilters({ priorities: values }),
    [patchFilters],
  );
  const setSearch = useCallback(
    (value: string) => patchFilters({ search: value }),
    [patchFilters],
  );

  const resetFilters = useCallback(() => {
    setFilters(INITIAL_FILTERS);
    setPage(1);
  }, []);

  const refresh = useCallback(async () => {
    await load(page, filters);
  }, [load, page, filters]);

  const createWorkItem = useCallback(
    async (input: CreateWorkItemInput) => {
      setIsMutating(true);
      try {
        const created = await workItemsApi.create(input);
        setFilters((current) => ({ ...current, projectId: input.project_id }));
        setPage(1);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [],
  );

  const updateWorkItem = useCallback(
    async (id: string, input: UpdateWorkItemInput) => {
      setIsMutating(true);
      try {
        const updated = await workItemsApi.update(id, input);
        await load(page, filters);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, filters],
  );

  const deleteWorkItem = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await workItemsApi.remove(id);
        const remaining = (data?.items.length ?? 1) - 1;
        const nextPage = remaining <= 0 && page > 1 ? page - 1 : page;
        if (nextPage !== page) {
          setPage(nextPage);
        } else {
          await load(nextPage, filters);
        }
      } finally {
        setIsMutating(false);
      }
    },
    [data, load, page, filters],
  );

  const totalPages = data ? Math.max(1, Math.ceil(data.total / limit)) : 1;

  return {
    data,
    items: data?.items ?? [],
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    filters,
    setProjectId,
    setSprintId,
    setAssigneeId,
    setItemTypes,
    setStatuses,
    setPriorities,
    setSearch,
    setPage,
    resetFilters,
    refresh,
    createWorkItem,
    updateWorkItem,
    deleteWorkItem,
  };
}