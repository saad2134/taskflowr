from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.models.user import Execution as ExecutionModel, ExecutionStatus as ExecutionStatusEnum
from app.schemas.execution import ExecutionResponse, ExecutionListResponse
from app.core.security import get_current_active_user

router = APIRouter(prefix="/executions", tags=["executions"])


@router.get("", response_model=ExecutionListResponse)
async def list_executions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[ExecutionStatusEnum] = None,
    task_id: Optional[UUID] = None,
    workflow_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(ExecutionModel).where(ExecutionModel.owner_id == current_user.id)
    
    if status_filter:
        query = query.where(ExecutionModel.status == status_filter)
    if task_id:
        query = query.where(ExecutionModel.task_id == task_id)
    if workflow_id:
        query = query.where(ExecutionModel.workflow_id == workflow_id)
    
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.offset(skip).limit(limit).order_by(ExecutionModel.created_at.desc())
    result = await db.execute(query)
    executions = result.scalars().all()
    
    return ExecutionListResponse(
        executions=executions,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    execution_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ExecutionModel).where(
            ExecutionModel.id == execution_id,
            ExecutionModel.owner_id == current_user.id
        )
    )
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution


@router.post("/{execution_id}/cancel", response_model=ExecutionResponse)
async def cancel_execution(
    execution_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ExecutionModel).where(
            ExecutionModel.id == execution_id,
            ExecutionModel.owner_id == current_user.id
        )
    )
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    if execution.status not in [ExecutionStatusEnum.QUEUED, ExecutionStatusEnum.RUNNING]:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot cancel execution with status: {execution.status}"
        )
    
    execution.status = ExecutionStatusEnum.CANCELLED
    await db.commit()
    await db.refresh(execution)
    
    return execution


@router.get("/{execution_id}/logs")
async def get_execution_logs(
    execution_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ExecutionModel).where(
            ExecutionModel.id == execution_id,
            ExecutionModel.owner_id == current_user.id
        )
    )
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return {"logs": execution.logs or {}}
