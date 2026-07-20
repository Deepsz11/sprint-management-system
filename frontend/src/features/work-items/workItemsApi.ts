import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CreateWorkItemInput,
  PaginatedProjectsResponse,
  PaginatedSprintsResponse,
  PaginatedUsersResponse,
  PaginatedWorkItems,
  UpdateWorkItemInput,
  WorkItem,
  WorkItemListParams,
} from "./types";

function buildParams(params: WorkItemListParams): Record<string, unknown> {
  const query: Record<string, unknown> = {
    limit: params.limit,
    offset: params.offset,
  };
  if (params.project_id) query.project_id = params.project_id;
  if (params.sprint_id) query.sprint_id = params.sprint_id;
  if (params.assignee_id) query.assignee_id = params.assignee_id;
  if (params.item_type && params.item_type.length > 0) {
    query.item_type = [...params.item_type];
  }
  if (params.status && params.status.length > 0) {
    query.status = [...params.status];
  }
  if (params.priority && params.priority.length > 0) {
    query.priority = [...params.priority];
  }
  if (params.search && params.search.trim().length > 0) {
    query.search = params.search.trim();
  }
  return query;
}

export const workItemsApi = {
  async list(params: WorkItemListParams): Promise<PaginatedWorkItems> {
    const response = await apiClient.get<PaginatedWorkItems>(
      API_ENDPOINTS.WORK_ITEMS,
      { params: buildParams(params) },
    );
    return response.data;
  },

  async get(id: string): Promise<WorkItem> {
    const response = await apiClient.get<WorkItem>(
      `${API_ENDPOINTS.WORK_ITEMS}/${id}`,
    );
    return response.data;
  },

  async create(input: CreateWorkItemInput): Promise<WorkItem> {
    const response = await apiClient.post<WorkItem>(
      API_ENDPOINTS.WORK_ITEMS,
      input,
    );
    return response.data;
  },

  async update(id: string, input: UpdateWorkItemInput): Promise<WorkItem> {
    const response = await apiClient.patch<WorkItem>(
      `${API_ENDPOINTS.WORK_ITEMS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.WORK_ITEMS}/${id}`);
  },

  async listProjects(): Promise<PaginatedProjectsResponse> {
    const response = await apiClient.get<PaginatedProjectsResponse>(
      API_ENDPOINTS.PROJECTS,
      { params: { limit: 200, offset: 0, include_archived: false } },
    );
    return response.data;
  },

  async listSprints(projectId: string): Promise<PaginatedSprintsResponse> {
    const response = await apiClient.get<PaginatedSprintsResponse>(
      API_ENDPOINTS.SPRINTS,
      { params: { project_id: projectId, limit: 200, offset: 0 } },
    );
    return response.data;
  },

  async listUsers(): Promise<PaginatedUsersResponse> {
    const response = await apiClient.get<PaginatedUsersResponse>(
      API_ENDPOINTS.USERS,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },
};