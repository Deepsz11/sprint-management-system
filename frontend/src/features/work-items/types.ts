export type WorkItemType = "epic" | "story" | "task" | "bug" | "spike";

export type WorkItemStatus =
  | "backlog"
  | "todo"
  | "in_progress"
  | "in_review"
  | "done"
  | "cancelled";

export type WorkItemPriority = "critical" | "high" | "medium" | "low";

export interface WorkItem {
  readonly id: string;
  readonly project_id: string;
  readonly sprint_id: string | null;
  readonly parent_id: string | null;
  readonly epic_id: string | null;
  readonly external_key: string | null;
  readonly title: string;
  readonly description: string | null;
  readonly item_type: WorkItemType;
  readonly status: WorkItemStatus;
  readonly priority: WorkItemPriority;
  readonly story_points: number | null;
  readonly estimated_hours: number | null;
  readonly actual_hours: number | null;
  readonly assignee_id: string | null;
  readonly reporter_id: string | null;
  readonly labels: string[];
  readonly started_at: string | null;
  readonly completed_at: string | null;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface WorkItemProjectOption {
  readonly id: string;
  readonly organization_id: string;
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly is_archived: boolean;
}

export interface WorkItemSprintOption {
  readonly id: string;
  readonly project_id: string;
  readonly name: string;
  readonly status: string;
  readonly start_date: string;
  readonly end_date: string;
}

export interface WorkItemAssigneeOption {
  readonly id: string;
  readonly email: string;
  readonly full_name: string;
  readonly organization_id: string | null;
  readonly role: string;
  readonly status: string;
}

export interface PaginatedWorkItems {
  readonly items: WorkItem[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedProjectsResponse {
  readonly items: WorkItemProjectOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedSprintsResponse {
  readonly items: WorkItemSprintOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedUsersResponse {
  readonly items: WorkItemAssigneeOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface CreateWorkItemInput {
  readonly project_id: string;
  readonly sprint_id?: string | null;
  readonly title: string;
  readonly description?: string | null;
  readonly item_type: WorkItemType;
  readonly priority: WorkItemPriority;
  readonly story_points?: number | null;
  readonly estimated_hours?: number | null;
  readonly assignee_id?: string | null;
  readonly labels?: string[];
}

export interface UpdateWorkItemInput {
  readonly title?: string;
  readonly description?: string | null;
  readonly priority?: WorkItemPriority;
  readonly status?: WorkItemStatus;
  readonly story_points?: number | null;
  readonly estimated_hours?: number | null;
  readonly sprint_id?: string | null;
  readonly assignee_id?: string | null;
  readonly labels?: string[];
}

export interface WorkItemListParams {
  readonly limit: number;
  readonly offset: number;
  readonly project_id?: string;
  readonly sprint_id?: string;
  readonly assignee_id?: string;
  readonly item_type?: readonly WorkItemType[];
  readonly status?: readonly WorkItemStatus[];
  readonly priority?: readonly WorkItemPriority[];
  readonly search?: string;
}