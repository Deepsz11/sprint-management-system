import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { kpisApi } from "./kpisApi";
import type {
  CreateKPIInput,
  KPI,
  KPIListParams,
  KPIUnit,
  PaginatedKPIs,
  UpdateKPIInput,
} from "./types";

interface UseKPIsOptions {
  readonly limit: number;
}

export interface KPIFilters {
  readonly outcomeId: string | null;
  readonly ownerId: string | null;
  readonly units: readonly KPIUnit[];
  readonly isActive: boolean | null;
  readonly search: string;
}

interface UseKPIsResult {
  readonly data: PaginatedKPIs | null;
  readonly items: KPI[];
  readonly filtered: KPI[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly filters: KPIFilters;
  readonly setOutcomeId: (value: string | null) => void;
  readonly setOwnerId: (value: string | null) => void;
  readonly setUnits: (values: readonly KPIUnit[]) => void;
  readonly setIsActive: (value: boolean | null) => void;
  readonly setSearch: (value: string) => void;
  readonly setPage: (page: number) => void;
  readonly resetFilters: () => void;
  readonly refresh: () => Promise<void>;
  readonly createKPI: (input: CreateKPIInput) => Promise<KPI>;
  readonly updateKPI: (id: string, input: UpdateKPIInput) => Promise<KPI>;
  readonly deleteKPI: (id: string) => Promise<void>;
}

const INITIAL_FILTERS: KPIFilters = {
  outcomeId: null,
  ownerId: null,
  units: [],
  isActive: null,
  search: "",
};

export function useKPIs(
  options: UseKPIsOptions = { limit: 20 },
): UseKPIsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedKPIs | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [filters, setFilters] = useState<KPIFilters>(INITIAL_FILTERS);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, currentFilters: KPIFilters) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: KPIListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
          outcome_id: currentFilters.outcomeId ?? undefined,
          owner_id: currentFilters.ownerId ?? undefined,
          unit:
            currentFilters.units.length > 0 ? currentFilters.units : undefined,
          is_active:
            currentFilters.isActive === null
              ? undefined
              : currentFilters.isActive,
        };
        const result = await kpisApi.list(params);
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

  const patchFilters = useCallback((patch: Partial<KPIFilters>) => {
    setFilters((current) => ({ ...current, ...patch }));
    setPage(1);
  }, []);

  const setOutcomeId = useCallback(
    (value: string | null) => patchFilters({ outcomeId: value }),
    [patchFilters],
  );
  const setOwnerId = useCallback(
    (value: string | null) => patchFilters({ ownerId: value }),
    [patchFilters],
  );
  const setUnits = useCallback(
    (values: readonly KPIUnit[]) => patchFilters({ units: values }),
    [patchFilters],
  );
  const setIsActive = useCallback(
    (value: boolean | null) => patchFilters({ isActive: value }),
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

  const createKPI = useCallback(
    async (input: CreateKPIInput) => {
      setIsMutating(true);
      try {
        const created = await kpisApi.create(input);
        setPage(1);
        await load(1, filters);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load, filters],
  );

  const updateKPI = useCallback(
    async (id: string, input: UpdateKPIInput) => {
      setIsMutating(true);
      try {
        const updated = await kpisApi.update(id, input);
        await load(page, filters);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, filters],
  );

  const deleteKPI = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await kpisApi.remove(id);
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

  const items = data?.items ?? [];
  const term = filters.search.trim().toLowerCase();
  const filtered =
    term.length === 0
      ? items
      : items.filter((kpi) => {
          return (
            kpi.name.toLowerCase().includes(term) ||
            (kpi.description ?? "").toLowerCase().includes(term) ||
            (kpi.data_source ?? "").toLowerCase().includes(term)
          );
        });

  const totalPages = data ? Math.max(1, Math.ceil(data.total / limit)) : 1;

  return {
    data,
    items,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    filters,
    setOutcomeId,
    setOwnerId,
    setUnits,
    setIsActive,
    setSearch,
    setPage,
    resetFilters,
    refresh,
    createKPI,
    updateKPI,
    deleteKPI,
  };
}