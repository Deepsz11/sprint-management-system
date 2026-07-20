import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { businessOutcomesApi } from "./businessOutcomesApi";
import type {
  BusinessOutcome,
  BusinessOutcomeListParams,
  CreateBusinessOutcomeInput,
  OutcomeStatus,
  PaginatedBusinessOutcomes,
  UpdateBusinessOutcomeInput,
} from "./types";

interface UseBusinessOutcomesOptions {
  readonly limit: number;
}

export interface BusinessOutcomeFilters {
  readonly ownerId: string | null;
  readonly statuses: readonly OutcomeStatus[];
  readonly search: string;
  readonly targetBefore: string | null;
  readonly targetAfter: string | null;
}

interface UseBusinessOutcomesResult {
  readonly data: PaginatedBusinessOutcomes | null;
  readonly items: BusinessOutcome[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly filters: BusinessOutcomeFilters;
  readonly setOwnerId: (value: string | null) => void;
  readonly setStatuses: (values: readonly OutcomeStatus[]) => void;
  readonly setSearch: (value: string) => void;
  readonly setTargetBefore: (value: string | null) => void;
  readonly setTargetAfter: (value: string | null) => void;
  readonly setPage: (page: number) => void;
  readonly resetFilters: () => void;
  readonly refresh: () => Promise<void>;
  readonly createOutcome: (
    input: CreateBusinessOutcomeInput,
  ) => Promise<BusinessOutcome>;
  readonly updateOutcome: (
    id: string,
    input: UpdateBusinessOutcomeInput,
  ) => Promise<BusinessOutcome>;
  readonly deleteOutcome: (id: string) => Promise<void>;
}

const INITIAL_FILTERS: BusinessOutcomeFilters = {
  ownerId: null,
  statuses: [],
  search: "",
  targetBefore: null,
  targetAfter: null,
};

export function useBusinessOutcomes(
  options: UseBusinessOutcomesOptions = { limit: 20 },
): UseBusinessOutcomesResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedBusinessOutcomes | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [filters, setFilters] = useState<BusinessOutcomeFilters>(
    INITIAL_FILTERS,
  );
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, currentFilters: BusinessOutcomeFilters) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: BusinessOutcomeListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
          owner_id: currentFilters.ownerId ?? undefined,
          status:
            currentFilters.statuses.length > 0
              ? currentFilters.statuses
              : undefined,
          target_before: currentFilters.targetBefore ?? undefined,
          target_after: currentFilters.targetAfter ?? undefined,
          search:
            currentFilters.search.trim().length > 0
              ? currentFilters.search
              : undefined,
        };
        const result = await businessOutcomesApi.list(params);
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

  const patchFilters = useCallback(
    (patch: Partial<BusinessOutcomeFilters>) => {
      setFilters((current) => ({ ...current, ...patch }));
      setPage(1);
    },
    [],
  );

  const setOwnerId = useCallback(
    (value: string | null) => patchFilters({ ownerId: value }),
    [patchFilters],
  );
  const setStatuses = useCallback(
    (values: readonly OutcomeStatus[]) => patchFilters({ statuses: values }),
    [patchFilters],
  );
  const setSearch = useCallback(
    (value: string) => patchFilters({ search: value }),
    [patchFilters],
  );
  const setTargetBefore = useCallback(
    (value: string | null) => patchFilters({ targetBefore: value }),
    [patchFilters],
  );
  const setTargetAfter = useCallback(
    (value: string | null) => patchFilters({ targetAfter: value }),
    [patchFilters],
  );
  const resetFilters = useCallback(() => {
    setFilters(INITIAL_FILTERS);
    setPage(1);
  }, []);

  const refresh = useCallback(async () => {
    await load(page, filters);
  }, [load, page, filters]);

  const createOutcome = useCallback(
    async (input: CreateBusinessOutcomeInput) => {
      setIsMutating(true);
      try {
        const created = await businessOutcomesApi.create(input);
        setPage(1);
        await load(1, filters);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load, filters],
  );

  const updateOutcome = useCallback(
    async (id: string, input: UpdateBusinessOutcomeInput) => {
      setIsMutating(true);
      try {
        const updated = await businessOutcomesApi.update(id, input);
        await load(page, filters);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, filters],
  );

  const deleteOutcome = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await businessOutcomesApi.remove(id);
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
    setOwnerId,
    setStatuses,
    setSearch,
    setTargetBefore,
    setTargetAfter,
    setPage,
    resetFilters,
    refresh,
    createOutcome,
    updateOutcome,
    deleteOutcome,
  };
}