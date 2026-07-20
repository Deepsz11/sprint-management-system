"""Business outcome endpoints."""

from __future__ import annotations

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.business_outcome_extensions import (
    BusinessOutcomeArchiveDTO,
    BusinessOutcomeDetailDTO,
    BusinessOutcomeReplaceDTO,
)
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.outcome import (
    BusinessOutcomeCreateDTO,
    BusinessOutcomeDTO,
    BusinessOutcomeUpdateDTO,
)
from app.application.use_cases.outcomes import (
    ArchiveBusinessOutcomeCommand,
    ArchiveBusinessOutcomeUseCase,
    CreateBusinessOutcomeCommand,
    CreateBusinessOutcomeUseCase,
    DeleteBusinessOutcomeCommand,
    DeleteBusinessOutcomeUseCase,
    GetBusinessOutcomeQuery,
    GetBusinessOutcomeUseCase,
    ListBusinessOutcomesQuery,
    ListBusinessOutcomesUseCase,
    UpdateBusinessOutcomeCommand,
    UpdateBusinessOutcomeUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import OutcomeStatus
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/business-outcomes", tags=["business-outcomes"])


@router.post(
    "",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a business outcome",
)
def create_outcome(
    payload: BusinessOutcomeCreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Create a business outcome."""
    use_case = CreateBusinessOutcomeUseCase()
    return use_case.execute(
        CreateBusinessOutcomeCommand(
            name=payload.name,
            owner_id=payload.owner_id,
            description=payload.description,
            hypothesis=payload.hypothesis,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[BusinessOutcomeDTO],
    status_code=status.HTTP_200_OK,
    summary="List business outcomes",
)
def list_outcomes(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    owner_id: UUID | None = Query(default=None),
    status_filter: list[OutcomeStatus] | None = Query(default=None, alias="status"),
    target_before: date | None = Query(default=None),
    target_after: date | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
) -> PaginatedResultDTO[BusinessOutcomeDTO]:
    """List business outcomes with filtering."""
    use_case = ListBusinessOutcomesUseCase()
    return use_case.execute(
        ListBusinessOutcomesQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            owner_id=owner_id,
            statuses=tuple(s.value for s in status_filter) if status_filter else (),
            target_before=target_before,
            target_after=target_after,
            search=search,
        )
    )


@router.get(
    "/{outcome_id}",
    response_model=BusinessOutcomeDetailDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a business outcome (with linked KPIs and work items)",
)
def get_outcome(
    outcome_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_READ))],
    include_linked: bool = Query(default=True),
) -> BusinessOutcomeDetailDTO:
    """Retrieve a business outcome by ID."""
    use_case = GetBusinessOutcomeUseCase()
    return use_case.execute(
        GetBusinessOutcomeQuery(
            outcome_id=outcome_id,
            context=context,
            include_linked=include_linked,
        )
    )


@router.patch(
    "/{outcome_id}",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a business outcome",
)
def patch_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Partially update a business outcome."""
    provided = payload.model_fields_set
    use_case = UpdateBusinessOutcomeUseCase()
    return use_case.execute(
        UpdateBusinessOutcomeCommand(
            outcome_id=outcome_id,
            context=context,
            name=payload.name,
            description=payload.description,
            hypothesis=payload.hypothesis,
            owner_id=payload.owner_id,
            status=payload.status,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            _name_provided="name" in provided,
            _description_provided="description" in provided,
            _hypothesis_provided="hypothesis" in provided,
            _owner_provided="owner_id" in provided,
            _target_date_provided="target_date" in provided,
            _baseline_value_provided="baseline_value" in provided,
            _target_value_provided="target_value" in provided,
            _current_value_provided="current_value" in provided,
            _confidence_score_provided="confidence_score" in provided,
            _financial_impact_provided="financial_impact_estimate" in provided,
        )
    )


@router.put(
    "/{outcome_id}",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a business outcome (full update)",
)
def replace_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Full-replacement update of a business outcome."""
    use_case = UpdateBusinessOutcomeUseCase()
    return use_case.execute(
        UpdateBusinessOutcomeCommand(
            outcome_id=outcome_id,
            context=context,
            name=payload.name,
            description=payload.description,
            hypothesis=payload.hypothesis,
            owner_id=payload.owner_id,
            status=payload.status,
            target_date=payload.target_date,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            confidence_score=payload.confidence_score,
            financial_impact_estimate=payload.financial_impact_estimate,
            _name_provided=True,
            _description_provided=True,
            _hypothesis_provided=True,
            _owner_provided=True,
            _target_date_provided=True,
            _baseline_value_provided=True,
            _target_value_provided=True,
            _current_value_provided=True,
            _confidence_score_provided=True,
            _financial_impact_provided=True,
        )
    )


@router.delete(
    "/{outcome_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft-delete a business outcome",
)
def delete_outcome(
    outcome_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> None:
    """Soft-delete a business outcome."""
    use_case = DeleteBusinessOutcomeUseCase()
    use_case.execute(
        DeleteBusinessOutcomeCommand(outcome_id=outcome_id, context=context)
    )


@router.patch(
    "/{outcome_id}/archive",
    response_model=BusinessOutcomeDTO,
    status_code=status.HTTP_200_OK,
    summary="Archive or restore a business outcome",
)
def archive_outcome(
    outcome_id: UUID,
    payload: BusinessOutcomeArchiveDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.OUTCOME_MANAGE))],
) -> BusinessOutcomeDTO:
    """Archive or restore a business outcome."""
    use_case = ArchiveBusinessOutcomeUseCase()
    return use_case.execute(
        ArchiveBusinessOutcomeCommand(
            outcome_id=outcome_id, archived=payload.archived, context=context
        )
    )
    return {"message": "Deleted successfully"}