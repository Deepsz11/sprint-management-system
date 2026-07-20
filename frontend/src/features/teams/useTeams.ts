import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { teamsApi } from "./teamsApi";
import type {
  CreateTeamInput,
  PaginatedTeams,
  Team,
  TeamListParams,
  UpdateTeamInput,
} from "./types";

interface UseTeamsOptions {
  readonly limit: number;
}

export interface TeamFilters {
  readonly search: string;
  readonly organizationId: string | null;
  readonly status: "all" | "active" | "inactive";
}

interface UseTeamsResult {
  readonly data: PaginatedTeams | null;
  readonly items: Team[];
  readonly filtered: Team[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly filters: TeamFilters;
  readonly setSearch: (value: string) => void;
  readonly setOrganizationId: (value: string | null) => void;
  readonly setStatus: (value: TeamFilters["status"]) => void;
  readonly setPage: (page: number) => void;
  readonly resetFilters: () => void;
  readonly refresh: () => Promise<void>;
  readonly createTeam: (input: CreateTeamInput) => Promise<Team>;
  readonly updateTeam: (id: string, input: UpdateTeamInput) => Promise<Team>;
  readonly deleteTeam: (id: string) => Promise<void>;
}

const INITIAL_FILTERS: TeamFilters = {
  search: "",
  organizationId: null,
  status: "all",
};

export function useTeams(
  options: UseTeamsOptions = { limit: 20 },
): UseTeamsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedTeams | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [filters, setFilters] = useState<TeamFilters>(INITIAL_FILTERS);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: TeamListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
        };
        const result = await teamsApi.list(params);
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
    void load(page);
    return () => {
      mounted.current = false;
    };
  }, [load, page]);

  const setSearch = useCallback((value: string) => {
    setFilters((current) => ({ ...current, search: value }));
  }, []);

  const setOrganizationId = useCallback((value: string | null) => {
    setFilters((current) => ({ ...current, organizationId: value }));
  }, []);

  const setStatus = useCallback((value: TeamFilters["status"]) => {
    setFilters((current) => ({ ...current, status: value }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(INITIAL_FILTERS);
  }, []);

  const refresh = useCallback(async () => {
    await load(page);
  }, [load, page]);

  const createTeam = useCallback(
    async (input: CreateTeamInput) => {
      setIsMutating(true);
      try {
        const created = await teamsApi.create(input);
        setPage(1);
        await load(1);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load],
  );

  const updateTeam = useCallback(
    async (id: string, input: UpdateTeamInput) => {
      setIsMutating(true);
      try {
        const updated = await teamsApi.update(id, input);
        await load(page);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page],
  );

  const deleteTeam = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await teamsApi.remove(id);
        const remaining = (data?.items.length ?? 1) - 1;
        const nextPage = remaining <= 0 && page > 1 ? page - 1 : page;
        if (nextPage !== page) {
          setPage(nextPage);
        } else {
          await load(nextPage);
        }
      } finally {
        setIsMutating(false);
      }
    },
    [data, load, page],
  );

  const items = data?.items ?? [];

  const filtered = useMemo(() => {
    const term = filters.search.trim().toLowerCase();
    return items.filter((team) => {
      if (
        filters.organizationId &&
        team.organization_id !== filters.organizationId
      ) {
        return false;
      }
      if (term.length === 0) return true;
      return (
        team.name.toLowerCase().includes(term) ||
        team.slug.toLowerCase().includes(term) ||
        (team.description ?? "").toLowerCase().includes(term)
      );
    });
  }, [items, filters]);

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
    setSearch,
    setOrganizationId,
    setStatus,
    setPage,
    resetFilters,
    refresh,
    createTeam,
    updateTeam,
    deleteTeam,
  };
}