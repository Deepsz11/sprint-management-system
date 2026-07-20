import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError, toApiError } from "@/api/errors";

import { usersApi } from "./usersApi";
import type {
  InviteUserInput,
  PaginatedUsers,
  UpdateUserInput,
  User,
  UserListParams,
  UserRole,
  UserStatus,
} from "./types";

interface UseUsersOptions {
  readonly limit: number;
}

export interface UserFilters {
  readonly search: string;
  readonly organizationId: string | null;
  readonly teamId: string | null;
  readonly role: UserRole | null;
  readonly status: UserStatus | "all";
}

interface UseUsersResult {
  readonly data: PaginatedUsers | null;
  readonly items: User[];
  readonly filtered: User[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly filters: UserFilters;
  readonly setSearch: (value: string) => void;
  readonly setOrganizationId: (value: string | null) => void;
  readonly setTeamId: (value: string | null) => void;
  readonly setRole: (value: UserRole | null) => void;
  readonly setStatus: (value: UserFilters["status"]) => void;
  readonly setPage: (page: number) => void;
  readonly resetFilters: () => void;
  readonly refresh: () => Promise<void>;
  readonly inviteUser: (input: InviteUserInput) => Promise<User>;
  readonly updateUser: (id: string, input: UpdateUserInput) => Promise<User>;
  readonly deactivateUser: (id: string) => Promise<User>;
}

const INITIAL_FILTERS: UserFilters = {
  search: "",
  organizationId: null,
  teamId: null,
  role: null,
  status: "all",
};

export function useUsers(
  options: UseUsersOptions = { limit: 20 },
): UseUsersResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedUsers | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [filters, setFilters] = useState<UserFilters>(INITIAL_FILTERS);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, currentFilters: UserFilters) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: UserListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
          role: currentFilters.role ?? undefined,
          search:
            currentFilters.search.trim().length > 0
              ? currentFilters.search
              : undefined,
        };
        const result = await usersApi.list(params);
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

  const patch = useCallback((changes: Partial<UserFilters>) => {
    setFilters((current) => ({ ...current, ...changes }));
    setPage(1);
  }, []);

  const setSearch = useCallback(
    (value: string) => patch({ search: value }),
    [patch],
  );
  const setOrganizationId = useCallback(
    (value: string | null) => patch({ organizationId: value, teamId: null }),
    [patch],
  );
  const setTeamId = useCallback(
    (value: string | null) => patch({ teamId: value }),
    [patch],
  );
  const setRole = useCallback(
    (value: UserRole | null) => patch({ role: value }),
    [patch],
  );
  const setStatus = useCallback(
    (value: UserFilters["status"]) => patch({ status: value }),
    [patch],
  );

  const resetFilters = useCallback(() => {
    setFilters(INITIAL_FILTERS);
    setPage(1);
  }, []);

  const refresh = useCallback(async () => {
    await load(page, filters);
  }, [load, page, filters]);

  const inviteUser = useCallback(
    async (input: InviteUserInput) => {
      setIsMutating(true);
      try {
        const created = await usersApi.invite(input);
        setPage(1);
        await load(1, filters);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load, filters],
  );

  const updateUser = useCallback(
    async (id: string, input: UpdateUserInput) => {
      setIsMutating(true);
      try {
        const updated = await usersApi.update(id, input);
        await load(page, filters);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, filters],
  );

  const deactivateUser = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        const updated = await usersApi.update(id, { status: "deactivated" });
        await load(page, filters);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, filters],
  );

  const items = data?.items ?? [];
  const filtered = items.filter((user) => {
    if (
      filters.organizationId &&
      user.organization_id !== filters.organizationId
    ) {
      return false;
    }
    if (filters.status !== "all" && user.status !== filters.status) {
      return false;
    }
    return true;
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
    setSearch,
    setOrganizationId,
    setTeamId,
    setRole,
    setStatus,
    setPage,
    resetFilters,
    refresh,
    inviteUser,
    updateUser,
    deactivateUser,
  };
}