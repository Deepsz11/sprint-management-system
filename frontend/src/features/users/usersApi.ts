import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  InviteUserInput,
  PaginatedUserOrganizations,
  PaginatedUserTeams,
  PaginatedUsers,
  UpdateUserInput,
  User,
  UserListParams,
} from "./types";

function buildParams(params: UserListParams): Record<string, unknown> {
  const query: Record<string, unknown> = {
    limit: params.limit,
    offset: params.offset,
  };
  if (params.role) query.role = params.role;
  if (params.search && params.search.trim().length > 0) {
    query.search = params.search.trim();
  }
  return query;
}

export const usersApi = {
  async list(params: UserListParams): Promise<PaginatedUsers> {
    const response = await apiClient.get<PaginatedUsers>(
      API_ENDPOINTS.USERS,
      { params: buildParams(params) },
    );
    return response.data;
  },

  async get(id: string): Promise<User> {
    const response = await apiClient.get<User>(
      `${API_ENDPOINTS.USERS}/${id}`,
    );
    return response.data;
  },

  async invite(input: InviteUserInput): Promise<User> {
    const response = await apiClient.post<User>(
      `${API_ENDPOINTS.USERS}/invite`,
      input,
    );
    return response.data;
  },

  async update(id: string, input: UpdateUserInput): Promise<User> {
    const response = await apiClient.patch<User>(
      `${API_ENDPOINTS.USERS}/${id}`,
      input,
    );
    return response.data;
  },

  async listOrganizations(): Promise<PaginatedUserOrganizations> {
    const response = await apiClient.get<PaginatedUserOrganizations>(
      API_ENDPOINTS.ORGANIZATIONS,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },

  async listTeams(): Promise<PaginatedUserTeams> {
    const response = await apiClient.get<PaginatedUserTeams>(
      API_ENDPOINTS.TEAMS,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },
};