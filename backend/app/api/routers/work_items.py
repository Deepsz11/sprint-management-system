"""Work item endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.work_item import (
    WorkItemCreateDTO,
    WorkItemDTO,
    WorkItemUpdateDTO,
)
from app.application.dtos.work_item_extensions import (
    WorkItemAssignDTO,
    WorkItemMoveDTO,
    WorkItemReplaceDTO,
    WorkItemStatusChangeDTO,
)
from app.application.use_cases.work_items import (
    AssignWorkItemCommand,
    AssignWorkItemUseCase,
    ChangeWorkItemStatusCommand,
    ChangeWorkItemStatusUseCase,
    CreateWorkItemCommand,
    CreateWorkItemUseCase,
    DeleteWorkItemCommand,
    DeleteWorkItemUseCase,
    GetWorkItemQuery,
    GetWorkItemUseCase,
    ListWorkItemsQuery,
    ListWorkItemsUseCase,
    MoveWorkItemToSprintCommand,
    MoveWorkItemToSprintUseCase,
    UpdateWorkItemCommand,
    UpdateWorkItemUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import WorkItemPriority, WorkItemStatus, WorkItemType
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/work-items", tags=["work-items"])


@router.post(
    "",
    response_model=WorkItemDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a work item",
)
def create_work_item(
    payload: WorkItemCreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Create a new work item."""
    use_case = CreateWorkItemUseCase()
    return use_case.execute(
        CreateWorkItemCommand(
            project_id=payload.project_id,
            title=payload.title,
            description=payload.description,
            item_type=payload.item_type,
            priority=payload.priority,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            external_key=payload.external_key,
            labels=list(payload.labels),
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[WorkItemDTO],
    status_code=status.HTTP_200_OK,
    summary="List work items",
)
def list_work_items(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    project_id: UUID | None = Query(default=None),
    sprint_id: UUID | None = Query(default=None),
    assignee_id: UUID | None = Query(default=None),
    reporter_id: UUID | None = Query(default=None),
    epic_id: UUID | None = Query(default=None),
    item_type: list[WorkItemType] | None = Query(default=None),
    status_filter: list[WorkItemStatus] | None = Query(default=None, alias="status"),
    priority: list[WorkItemPriority] | None = Query(default=None),
    label: list[str] | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
    completed_after: datetime | None = Query(default=None),
    completed_before: datetime | None = Query(default=None),
) -> PaginatedResultDTO[WorkItemDTO]:
    """List work items with filtering."""
    use_case = ListWorkItemsUseCase()
    return use_case.execute(
        ListWorkItemsQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            project_id=project_id,
            sprint_id=sprint_id,
            assignee_id=assignee_id,
            reporter_id=reporter_id,
            epic_id=epic_id,
            item_types=tuple(t.value for t in item_type) if item_type else (),
            statuses=tuple(s.value for s in status_filter) if status_filter else (),
            priorities=tuple(p.value for p in priority) if priority else (),
            labels=tuple(label) if label else (),
            search=search,
            completed_after=completed_after,
            completed_before=completed_before,
        )
    )


@router.get(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a work item",
)
def get_work_item(
    work_item_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_READ))],
) -> WorkItemDTO:
    """Retrieve a work item by ID."""
    use_case = GetWorkItemUseCase()
    return use_case.execute(
        GetWorkItemQuery(work_item_id=work_item_id, context=context)
    )


@router.patch(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a work item",
)
def patch_work_item(
    work_item_id: UUID,
    payload: WorkItemUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Partially update a work item."""
    provided = payload.model_fields_set
    use_case = UpdateWorkItemUseCase()
    return use_case.execute(
        UpdateWorkItemCommand(
            work_item_id=work_item_id,
            context=context,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            actual_hours=payload.actual_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            labels=payload.labels,
            _sprint_id_provided="sprint_id" in provided,
            _parent_id_provided="parent_id" in provided,
            _epic_id_provided="epic_id" in provided,
            _assignee_id_provided="assignee_id" in provided,
        )
    )


@router.put(
    "/{work_item_id}",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a work item (full update)",
)
def replace_work_item(
    work_item_id: UUID,
    payload: WorkItemReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Full-replacement update of a work item."""
    use_case = UpdateWorkItemUseCase()
    return use_case.execute(
        UpdateWorkItemCommand(
            work_item_id=work_item_id,
            context=context,
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
            story_points=payload.story_points,
            estimated_hours=payload.estimated_hours,
            actual_hours=payload.actual_hours,
            sprint_id=payload.sprint_id,
            parent_id=payload.parent_id,
            epic_id=payload.epic_id,
            assignee_id=payload.assignee_id,
            labels=payload.labels,
            _sprint_id_provided=True,
            _parent_id_provided=True,
            _epic_id_provided=True,
            _assignee_id_provided=True,
        )
    )


@router.delete(
    "/{work_item_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft-delete a work item",
)
def delete_work_item(
    work_item_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> None:
    """Soft-delete a work item."""
    use_case = DeleteWorkItemUseCase()
    use_case.execute(
        DeleteWorkItemCommand(work_item_id=work_item_id, context=context)
    )


@router.patch(
    "/{work_item_id}/assign",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Assign or unassign a work item",
)
def assign_work_item(
    work_item_id: UUID,
    payload: WorkItemAssignDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Reassign a work item to a user."""
    use_case = AssignWorkItemUseCase()
    return use_case.execute(
        AssignWorkItemCommand(
            work_item_id=work_item_id,
            assignee_id=payload.assignee_id,
            context=context,
        )
    )


@router.patch(
    "/{work_item_id}/status",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Change a work item's status",
)
def change_work_item_status(
    work_item_id: UUID,
    payload: WorkItemStatusChangeDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Change the status of a work item."""
    use_case = ChangeWorkItemStatusUseCase()
    return use_case.execute(
        ChangeWorkItemStatusCommand(
            work_item_id=work_item_id,
            target_status=payload.status,
            actual_hours=payload.actual_hours,
            context=context,
        )
    )


@router.patch(
    "/{work_item_id}/move",
    response_model=WorkItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Move a work item to a sprint or the backlog",
)
def move_work_item(
    work_item_id: UUID,
    payload: WorkItemMoveDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.WORK_ITEM_WRITE))],
) -> WorkItemDTO:
    """Move a work item into a sprint or return it to the backlog."""
    use_case = MoveWorkItemToSprintUseCase()
    return use_case.execute(
        MoveWorkItemToSprintCommand(
            work_item_id=work_item_id,
            sprint_id=payload.sprint_id,
            context=context,
        )
    )