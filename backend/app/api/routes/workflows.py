from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.models.user import Workflow as WorkflowModel, WorkflowStatus as WorkflowStatusEnum
from app.schemas.workflow import (
    WorkflowCreate, WorkflowResponse, WorkflowUpdate,
    WorkflowExecuteRequest, WorkflowExecuteResponse
)
from app.core.security import get_current_active_user
from app.services.agent_service import AgentService

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    workflow = WorkflowModel(
        name=workflow_data.name,
        description=workflow_data.description,
        definition=workflow_data.definition.model_dump() if workflow_data.definition else None,
        schedule=workflow_data.schedule,
        owner_id=current_user.id,
        status=WorkflowStatusEnum.DRAFT
    )
    
    db.add(workflow)
    await db.commit()
    await db.refresh(workflow)
    
    return workflow


@router.get("", response_model=List[WorkflowResponse])
async def list_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[WorkflowStatusEnum] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(WorkflowModel).where(WorkflowModel.owner_id == current_user.id)
    
    if status_filter:
        query = query.where(WorkflowModel.status == status_filter)
    
    query = query.offset(skip).limit(limit).order_by(WorkflowModel.created_at.desc())
    result = await db.execute(query)
    workflows = result.scalars().all()
    
    return workflows


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkflowModel).where(
            WorkflowModel.id == workflow_id,
            WorkflowModel.owner_id == current_user.id
        )
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: UUID,
    workflow_data: WorkflowUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkflowModel).where(
            WorkflowModel.id == workflow_id,
            WorkflowModel.owner_id == current_user.id
        )
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if workflow_data.name is not None:
        workflow.name = workflow_data.name
    if workflow_data.description is not None:
        workflow.description = workflow_data.description
    if workflow_data.definition is not None:
        workflow.definition = workflow_data.definition.model_dump()
    if workflow_data.schedule is not None:
        workflow.schedule = workflow_data.schedule
    if workflow_data.status is not None:
        workflow.status = workflow_data.status
    
    await db.commit()
    await db.refresh(workflow)
    
    return workflow


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkflowModel).where(
            WorkflowModel.id == workflow_id,
            WorkflowModel.owner_id == current_user.id
        )
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    await db.delete(workflow)
    await db.commit()
    
    return None


@router.post("/{workflow_id}/execute", response_model=WorkflowExecuteResponse)
async def execute_workflow(
    workflow_id: UUID,
    execute_data: WorkflowExecuteRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkflowModel).where(
            WorkflowModel.id == workflow_id,
            WorkflowModel.owner_id == current_user.id
        )
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if workflow.status != WorkflowStatusEnum.ACTIVE:
        raise HTTPException(status_code=400, detail="Workflow must be active to execute")
    
    agent_service = AgentService()
    workflow_response = await agent_service.execute_workflow(
        workflow_id=str(workflow_id),
        input_data=execute_data.input_data,
        user_id=str(current_user.id)
    )
    
    return WorkflowExecuteResponse(**workflow_response)


@router.post("/{workflow_id}/activate", response_model=WorkflowResponse)
async def activate_workflow(
    workflow_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkflowModel).where(
            WorkflowModel.id == workflow_id,
            WorkflowModel.owner_id == current_user.id
        )
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if not workflow.definition:
        raise HTTPException(status_code=400, detail="Workflow has no definition")
    
    workflow.status = WorkflowStatusEnum.ACTIVE
    await db.commit()
    await db.refresh(workflow)
    
    return workflow


@router.post("/{workflow_id}/pause", response_model=WorkflowResponse)
async def pause_workflow(
    workflow_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WorkflowModel).where(
            WorkflowModel.id == workflow_id,
            WorkflowModel.owner_id == current_user.id
        )
    )
    workflow = result.scalar_one_or_none()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow.status = WorkflowStatusEnum.PAUSED
    await db.commit()
    await db.refresh(workflow)
    
    return workflow
