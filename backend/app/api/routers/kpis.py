"""KPI endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.security import build_request_context, require_permissions
from app.application.context import RequestContext
from app.application.dtos.common import PageDTO, PaginatedResultDTO
from app.application.dtos.kpi import (
    KPICreateDTO,
    KPIDTO,
    KPIUpdateDTO,
    MetricSnapshotDTO,
)
from app.application.dtos.kpi_extensions import (
    KPIHistoryDTO,
    KPIRecordSnapshotDTO,
    KPIReplaceDTO,
    KPITargetUpdateDTO,
)
from app.application.use_cases.kpis import (
    CreateKPICommand,
    CreateKPIUseCase,
    DeleteKPICommand,
    DeleteKPIUseCase,
    GetKPIQuery,
    GetKPIUseCase,
    ListKPIHistoryQuery,
    ListKPIHistoryUseCase,
    ListKPIsQuery,
    ListKPIsUseCase,
    RecordKPISnapshotCommand,
    RecordKPISnapshotUseCase,
    UpdateKPICommand,
    UpdateKPIUseCase,
    UpdateKPITargetCommand,
    UpdateKPITargetUseCase,
)
from app.domain.entities.user import User
from app.domain.enums import KPIUnit
from app.domain.services.permissions import Permission

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.post(
    "",
    response_model=KPIDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a KPI",
)
def create_kpi(
    payload: KPICreateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Create a KPI."""
    use_case = CreateKPIUseCase()
    return use_case.execute(
        CreateKPICommand(
            name=payload.name,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            description=payload.description,
            unit=payload.unit,
            currency=payload.currency,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            context=context,
        )
    )


@router.get(
    "",
    response_model=PaginatedResultDTO[KPIDTO],
    status_code=status.HTTP_200_OK,
    summary="List KPIs",
)
def list_kpis(
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    outcome_id: UUID | None = Query(default=None),
    owner_id: UUID | None = Query(default=None),
    unit: list[KPIUnit] | None = Query(default=None),
    is_active: bool | None = Query(default=None),
) -> PaginatedResultDTO[KPIDTO]:
    """List KPIs with filtering."""
    use_case = ListKPIsUseCase()
    return use_case.execute(
        ListKPIsQuery(
            context=context,
            page=PageDTO(limit=limit, offset=offset),
            outcome_id=outcome_id,
            owner_id=owner_id,
            units=tuple(u.value for u in unit) if unit else (),
            is_active=is_active,
        )
    )


@router.get(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a KPI",
)
def get_kpi(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
) -> KPIDTO:
    """Retrieve a KPI by ID."""
    use_case = GetKPIUseCase()
    return use_case.execute(GetKPIQuery(kpi_id=kpi_id, context=context))


@router.patch(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Partially update a KPI",
)
def patch_kpi(
    kpi_id: UUID,
    payload: KPIUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Partially update a KPI."""
    provided = payload.model_fields_set
    use_case = UpdateKPIUseCase()
    return use_case.execute(
        UpdateKPICommand(
            kpi_id=kpi_id,
            context=context,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            name=payload.name,
            description=payload.description,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            is_active=payload.is_active,
            _outcome_provided="outcome_id" in provided,
            _owner_provided="owner_id" in provided,
            _name_provided="name" in provided,
            _description_provided="description" in provided,
            _direction_provided="direction" in provided,
            _baseline_provided="baseline_value" in provided,
            _target_provided="target_value" in provided,
            _current_provided="current_value" in provided,
            _data_source_provided="data_source" in provided,
            _refresh_provided="refresh_frequency_hours" in provided,
            _is_active_provided="is_active" in provided,
        )
    )


@router.put(
    "/{kpi_id}",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Replace a KPI (full update)",
)
def replace_kpi(
    kpi_id: UUID,
    payload: KPIReplaceDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Full-replacement update of a KPI (baseline changes are still guarded)."""
    use_case = UpdateKPIUseCase()
    return use_case.execute(
        UpdateKPICommand(
            kpi_id=kpi_id,
            context=context,
            outcome_id=payload.outcome_id,
            owner_id=payload.owner_id,
            name=payload.name,
            description=payload.description,
            direction=payload.direction,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            current_value=payload.current_value,
            data_source=payload.data_source,
            refresh_frequency_hours=payload.refresh_frequency_hours,
            is_active=payload.is_active,
            _outcome_provided=True,
            _owner_provided=True,
            _name_provided=True,
            _description_provided=True,
            _direction_provided=True,
            _baseline_provided=True,
            _target_provided=True,
            _current_provided=True,
            _data_source_provided=True,
            _refresh_provided=True,
            _is_active_provided=True,
        )
    )


@router.delete(
    "/{kpi_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft-delete a KPI",
)
def delete_kpi(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> None:
    """Soft-delete a KPI."""
    use_case = DeleteKPIUseCase()
    use_case.execute(DeleteKPICommand(kpi_id=kpi_id, context=context))


@router.post(
    "/{kpi_id}/snapshots",
    response_model=MetricSnapshotDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Record a KPI snapshot",
)
def record_snapshot(
    kpi_id: UUID,
    payload: KPIRecordSnapshotDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> MetricSnapshotDTO:
    """Record a new metric snapshot for a KPI."""
    use_case = RecordKPISnapshotUseCase()
    return use_case.execute(
        RecordKPISnapshotCommand(
            kpi_id=kpi_id,
            value=payload.value,
            recorded_at=payload.recorded_at,
            source=payload.source,
            notes=payload.notes,
            context=context,
        )
    )


@router.get(
    "/{kpi_id}/history",
    response_model=KPIHistoryDTO,
    status_code=status.HTTP_200_OK,
    summary="Get KPI snapshot history",
)
def get_history(
    kpi_id: UUID,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_READ))],
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    recorded_after: datetime | None = Query(default=None),
    recorded_before: datetime | None = Query(default=None),
    source: str | None = Query(default=None, max_length=200),
) -> KPIHistoryDTO:
    """Return the historical snapshots for a KPI."""
    use_case = ListKPIHistoryUseCase()
    return use_case.execute(
        ListKPIHistoryQuery(
            kpi_id=kpi_id,
            context=context,
            limit=limit,
            offset=offset,
            recorded_after=recorded_after,
            recorded_before=recorded_before,
            source=source,
        )
    )


@router.patch(
    "/{kpi_id}/target",
    response_model=KPIDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a KPI's target value (audited)",
)
def update_kpi_target(
    kpi_id: UUID,
    payload: KPITargetUpdateDTO,
    context: Annotated[RequestContext, Depends(build_request_context)],
    _: Annotated[User, Depends(require_permissions(Permission.KPI_MANAGE))],
) -> KPIDTO:
    """Update a KPI's target value and record an audit entry."""
    use_case = UpdateKPITargetUseCase()
    return use_case.execute(
        UpdateKPITargetCommand(
            kpi_id=kpi_id,
            target_value=payload.target_value,
            reason=payload.reason,
            context=context,
        )
    )
    return {"message": "Team deleted successfully"}