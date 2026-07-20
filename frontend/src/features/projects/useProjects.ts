import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { toApiError, ApiError } from "@/api/errors";

import { projectsApi } from "./projectsApi";
import type {
  CreateProjectInput,
  PaginatedProjects,
  Project,
  ProjectListParams,
  UpdateProjectInput,
} from "./types";

interface UseProjectsOptions {
  readonly limit: number;
}

interface UseProjectsResult {
  readonly data: PaginatedProjects | null;
  readonly filtered: Project[];
  readonly isLoading: boolean;
  readonly isMutating: boolean;
  readonly error: ApiError | null;
  readonly page: number;
  readonly totalPages: number;
  readonly search: string;
  readonly includeArchived: boolean;
  readonly setSearch: (value: string) => void;
  readonly setIncludeArchived: (value: boolean) => void;
  readonly setPage: (page: number) => void;
  readonly refresh: () => Promise<void>;
  readonly createProject: (input: CreateProjectInput) => Promise<Project>;
  readonly updateProject: (
    id: string,
    input: UpdateProjectInput,
  ) => Promise<Project>;
  readonly deleteProject: (id: string) => Promise<void>;
}

export function useProjects(
  options: UseProjectsOptions = { limit: 20 },
): UseProjectsResult {
  const { limit } = options;

  const [data, setData] = useState<PaginatedProjects | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isMutating, setIsMutating] = useState<boolean>(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [page, setPage] = useState<number>(1);
  const [search, setSearch] = useState<string>("");
  const [includeArchived, setIncludeArchived] = useState<boolean>(false);
  const mounted = useRef<boolean>(true);

  const load = useCallback(
    async (nextPage: number, archived: boolean) => {
      setIsLoading(true);
      setError(null);
      try {
        const params: ProjectListParams = {
          limit,
          offset: Math.max(0, (nextPage - 1) * limit),
          include_archived: archived,
        };
        const result = await projectsApi.list(params);
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
    void load(page, includeArchived);
    return () => {
      mounted.current = false;
    };
  }, [load, page, includeArchived]);

  const refresh = useCallback(async () => {
    await load(page, includeArchived);
  }, [load, page, includeArchived]);

  const createProject = useCallback(
    async (input: CreateProjectInput) => {
      setIsMutating(true);
      try {
        const created = await projectsApi.create(input);
        await load(1, includeArchived);
        setPage(1);
        return created;
      } finally {
        setIsMutating(false);
      }
    },
    [load, includeArchived],
  );

  const updateProject = useCallback(
    async (id: string, input: UpdateProjectInput) => {
      setIsMutating(true);
      try {
        const updated = await projectsApi.update(id, input);
        await load(page, includeArchived);
        return updated;
      } finally {
        setIsMutating(false);
      }
    },
    [load, page, includeArchived],
  );

  const deleteProject = useCallback(
    async (id: string) => {
      setIsMutating(true);
      try {
        await projectsApi.remove(id);
        const remaining = (data?.items.length ?? 1) - 1;
        const nextPage = remaining <= 0 && page > 1 ? page - 1 : page;
        if (nextPage !== page) {
          setPage(nextPage);
        } else {
          await load(nextPage, includeArchived);
        }
      } finally {
        setIsMutating(false);
      }
    },
    [data, load, page, includeArchived],
  );

  const filtered = useMemo(() => {
    if (!data) return [];
    const term = search.trim().toLowerCase();
    if (!term) return data.items;
    return data.items.filter((project) => {
      return (
        project.name.toLowerCase().includes(term) ||
        project.key.toLowerCase().includes(term) ||
        project.slug.toLowerCase().includes(term) ||
        (project.description ?? "").toLowerCase().includes(term)
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
    includeArchived,
    setSearch,
    setIncludeArchived,
    setPage,
    refresh,
    createProject,
    updateProject,
    deleteProject,
  };
}