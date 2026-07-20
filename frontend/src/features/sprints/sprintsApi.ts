import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CompleteSprintInput,
  CreateSprintInput,
  PaginatedSprintProjects,
  PaginatedSprints,
  Sprint,
  SprintListParams,
  UpdateSprintInput,
} from "./types";

export const sprintsApi = {
  async list(params: SprintListParams): Promise<PaginatedSprints> {
    const response = await apiClient.get<PaginatedSprints>(
      API_ENDPOINTS.SPRINTS,
      {
        params: {
          project_id: params.project_id,
          limit: params.limit,
          offset: params.offset,
        },
      },
    );
    return response.data;
  },

  async get(id: string): Promise<Sprint> {
    const response = await apiClient.get<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}`,
    );
    return response.data;
  },

  async create(input: CreateSprintInput): Promise<Sprint> {
    const response = await apiClient.post<Sprint>(
      API_ENDPOINTS.SPRINTS,
      input,
    );
    return response.data;
  },

  async update(id: string, input: UpdateSprintInput): Promise<Sprint> {
    const response = await apiClient.patch<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.SPRINTS}/${id}`);
  },

  async start(id: string): Promise<Sprint> {
    const response = await apiClient.post<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}/start`,
    );
    return response.data;
  },

  async complete(id: string, input: CompleteSprintInput): Promise<Sprint> {
    const response = await apiClient.post<Sprint>(
      `${API_ENDPOINTS.SPRINTS}/${id}/complete`,
      input,
    );
    return response.data;
  },

  async listProjects(): Promise<PaginatedSprintProjects> {
    const response = await apiClient.get<PaginatedSprintProjects>(
      API_ENDPOINTS.PROJECTS,
      {
        params: { limit: 200, offset: 0, include_archived: false },
      },
    );
    return response.data;
  },
};