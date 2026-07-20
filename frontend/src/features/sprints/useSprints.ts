import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { sprintsApi } from "./sprintsApi";
import type {
  CompleteSprintInput,
  CreateSprintInput,
  PaginatedSprints,
  Sprint,
  UpdateSprintInput,
} from "./types";

interface UseSprintsOptions {
  readonly limit: number;
}

interface UseSprintsResult {
  readonly data: PaginatedSprints | null;
  readonly filtered: Sprint[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly search: string;
  readonly projectId: string | null;
  readonly setSearch: (value: string) => void;
  readonly setProjectId: (value: string | null) => void;
  readonly setPage: (page: number) => void;
  readonly refresh: () => Promise<void>;
  readonly createSprint: (input: CreateSprintInput) => Promise<Sprint>;
  readonly updateSprint: (
    id: string,
    input: UpdateSprintInput,
  ) => Promise<Sprint>;
  readonly deleteSprint: (id: string) => Promise<void>;
  readonly startSprint: (id: string) => Promise<Sprint>;
  readonly completeSprint: (
    id: string,
    input: CompleteSprintInput,
  ) => Promise<Sprint>;
}

export function useSprints(
  options: UseSprintsOptions = { limit: 20 },
): UseSprintsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedSprints | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [search, setSearch] = useState<string>("");
  const [projectId, setProjectIdState] = useState<string | null>(null);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, projId: string | null) => {
      if (!projId) {
        setData(null);
        setIsLoading(false);
        return;
      }
      setIsLoading(true);
      setError(null);
      try {
        const result = await sprintsApi.list({
          project_id: projId,
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
        });
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
    void load(page, projectId);
    return () => {
      mounted.current = false;
    };
  }, [load, page, projectId]);

  const setProjectId = useCallback((value: string | null) => {
    setProjectIdState(value);
    setPage(1);
  }, []);

  const refresh = useCallback(async () => {
    await load(page, projectId);
  }, [load, page, projectId]);

  const createSprint = useCallback(
    async (input: CreateSprintInput) => {
      setIsMutating(true);
      try {
        const created = await sprintsApi.create(input);
        setProjectIdState(input.project_id);
        setPage(1);
        await load(1, input.project_id);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load],
  );

  const updateSprint = useCallback(
    async (id: string, input: UpdateSprintInput) => {
      setIsMutating(true);
      try {
        const updated = await sprintsApi.update(id, input);
        await load(page, projectId);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, projectId],
  );

  const deleteSprint = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await sprintsApi.remove(id);
        const remaining = (data?.items.length ?? 1) - 1;
        const nextPage = remaining <= 0 && page > 1 ? page - 1 : page;
        if (nextPage !== page) {
          setPage(nextPage);
        } else {
          await load(nextPage, projectId);
        }
      } finally {
        setIsMutating(false);
      }
    },
    [data, load, page, projectId],
  );

  const startSprint = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        const started = await sprintsApi.start(id);
        await load(page, projectId);
        return started;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, projectId],
  );

  const completeSprint = useCallback(
    async (id: string, input: CompleteSprintInput) => {
      setIsMutating(true);
      try {
        const completed = await sprintsApi.complete(id, input);
        await load(page, projectId);
        return completed;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, projectId],
  );

  const filtered = useMemo(() => {
    if (!data) return [];
    const term = search.trim().toLowerCase();
    if (!term) return data.items;
    return data.items.filter((sprint) => {
      return (
        sprint.name.toLowerCase().includes(term) ||
        (sprint.goal ?? "").toLowerCase().includes(term) ||
        sprint.status.toLowerCase().includes(term)
      );
    });
  }, [data, search]);

  const totalPages = data ? Math.max(1, Math.ceil(data.total / limit)) : 1;

  return {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    search,
    projectId,
    setSearch,
    setProjectId,
    setPage,
    refresh,
    createSprint,
    updateSprint,
    deleteSprint,
    startSprint,
    completeSprint,
  };
}