import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CreateOrganizationInput,
  Organization,
  OrganizationListParams,
  PaginatedOrganizations,
  UpdateOrganizationInput,
} from "./types";

export const organizationsApi = {
  async list(
    params: OrganizationListParams,
  ): Promise<PaginatedOrganizations> {
    const response = await apiClient.get<PaginatedOrganizations>(
      API_ENDPOINTS.ORGANIZATIONS,
      {
        params: {
          limit: params.limit,
          offset: params.offset,
        },
      },
    );
    return response.data;
  },

  async get(id: string): Promise<Organization> {
    const response = await apiClient.get<Organization>(
      `${API_ENDPOINTS.ORGANIZATIONS}/${id}`,
    );
    return response.data;
  },

  async create(input: CreateOrganizationInput): Promise<Organization> {
    const response = await apiClient.post<Organization>(
      API_ENDPOINTS.ORGANIZATIONS,
      input,
    );
    return response.data;
  },

  async update(
    id: string,
    input: UpdateOrganizationInput,
  ): Promise<Organization> {
    const response = await apiClient.patch<Organization>(
      `${API_ENDPOINTS.ORGANIZATIONS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.ORGANIZATIONS}/${id}`);
  },
};