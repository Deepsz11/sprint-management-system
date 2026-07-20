import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CreateTeamInput,
  PaginatedTeamLeads,
  PaginatedTeamOrganizations,
  PaginatedTeams,
  Team,
  TeamListParams,
  UpdateTeamInput,
} from "./types";

export const teamsApi = {
  async list(params: TeamListParams): Promise<PaginatedTeams> {
    const response = await apiClient.get<PaginatedTeams>(
      API_ENDPOINTS.TEAMS,
      {
        params: {
          limit: params.limit,
          offset: params.offset,
        },
      },
    );
    return response.data;
  },

  async get(id: string): Promise<Team> {
    const response = await apiClient.get<Team>(
      `${API_ENDPOINTS.TEAMS}/${id}`,
    );
    return response.data;
  },

  async create(input: CreateTeamInput): Promise<Team> {
    const response = await apiClient.post<Team>(
      API_ENDPOINTS.TEAMS,
      input,
    );
    return response.data;
  },

  async update(id: string, input: UpdateTeamInput): Promise<Team> {
    const response = await apiClient.patch<Team>(
      `${API_ENDPOINTS.TEAMS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.TEAMS}/${id}`);
  },

  async listOrganizations(): Promise<PaginatedTeamOrganizations> {
    const response = await apiClient.get<PaginatedTeamOrganizations>(
      API_ENDPOINTS.ORGANIZATIONS,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },

  async listLeads(): Promise<PaginatedTeamLeads> {
    const response = await apiClient.get<PaginatedTeamLeads>(
      API_ENDPOINTS.USERS,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },
};