import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CreateProjectInput,
  PaginatedProjects,
  PaginatedTeams,
  Project,
  ProjectListParams,
  UpdateProjectInput,
} from "./types";

export const projectsApi = {
  async list(params: ProjectListParams): Promise<PaginatedProjects> {
    const query: Record<string, string | number | boolean> = {
      limit: params.limit,
      offset: params.offset,
      include_archived: params.include_archived ?? false,
    };
    if (params.team_id) {
      query.team_id = params.team_id;
    }
    const response = await apiClient.get<PaginatedProjects>(
      API_ENDPOINTS.PROJECTS,
      { params: query },
    );
    return response.data;
  },

  async get(id: string): Promise<Project> {
    const response = await apiClient.get<Project>(
      `${API_ENDPOINTS.PROJECTS}/${id}`,
    );
    return response.data;
  },

  async create(input: CreateProjectInput): Promise<Project> {
    const response = await apiClient.post<Project>(
      API_ENDPOINTS.PROJECTS,
      input,
    );
    return response.data;
  },

  async update(id: string, input: UpdateProjectInput): Promise<Project> {
    const response = await apiClient.patch<Project>(
      `${API_ENDPOINTS.PROJECTS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.PROJECTS}/${id}`);
  },

  async listTeams(): Promise<PaginatedTeams> {
    const response = await apiClient.get<PaginatedTeams>(API_ENDPOINTS.TEAMS, {
      params: { limit: 200, offset: 0 },
    });
    return response.data;
  },
};