import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { organizationsApi } from "./organizationsApi";
import type {
  CreateOrganizationInput,
  Organization,
  OrganizationListParams,
  PaginatedOrganizations,
  UpdateOrganizationInput,
} from "./types";

interface UseOrganizationsOptions {
  readonly limit: number;
}

export interface OrganizationFilters {
  readonly search: string;
  readonly status: "all" | "active" | "inactive";
}

interface UseOrganizationsResult {
  readonly data: PaginatedOrganizations | null;
  readonly items: Organization[];
  readonly filtered: Organization[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly filters: OrganizationFilters;
  readonly setSearch: (value: string) => void;
  readonly setStatus: (value: OrganizationFilters["status"]) => void;
  readonly setPage: (page: number) => void;
  readonly resetFilters: () => void;
  readonly refresh: () => Promise<void>;
  readonly createOrganization: (
    input: CreateOrganizationInput,
  ) => Promise<Organization>;
  readonly updateOrganization: (
    id: string,
    input: UpdateOrganizationInput,
  ) => Promise<Organization>;
  readonly deleteOrganization: (id: string) => Promise<void>;
}

const INITIAL_FILTERS: OrganizationFilters = {
  search: "",
  status: "all",
};

export function useOrganizations(
  options: UseOrganizationsOptions = { limit: 20 },
): UseOrganizationsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedOrganizations | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [filters, setFilters] = useState<OrganizationFilters>(INITIAL_FILTERS);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: OrganizationListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
        };
        const result = await organizationsApi.list(params);
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

  const setStatus = useCallback((value: OrganizationFilters["status"]) => {
    setFilters((current) => ({ ...current, status: value }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(INITIAL_FILTERS);
  }, []);

  const refresh = useCallback(async () => {
    await load(page);
  }, [load, page]);

  const createOrganization = useCallback(
    async (input: CreateOrganizationInput) => {
      setIsMutating(true);
      try {
        const created = await organizationsApi.create(input);
        setPage(1);
        await load(1);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load],
  );

  const updateOrganization = useCallback(
    async (id: string, input: UpdateOrganizationInput) => {
      setIsMutating(true);
      try {
        const updated = await organizationsApi.update(id, input);
        await load(page);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page],
  );

  const deleteOrganization = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await organizationsApi.remove(id);
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
    return items.filter((org) => {
      if (filters.status === "active" && !org.is_active) return false;
      if (filters.status === "inactive" && org.is_active) return false;
      if (term.length === 0) return true;
      return (
        org.name.toLowerCase().includes(term) ||
        org.slug.toLowerCase().includes(term) ||
        (org.description ?? "").toLowerCase().includes(term) ||
        (org.billing_email ?? "").toLowerCase().includes(term)
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
    setStatus,
    setPage,
    resetFilters,
    refresh,
    createOrganization,
    updateOrganization,
    deleteOrganization,
  };
}