from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.models.user import Task as TaskModel, TaskStatus as TaskStatusEnum
from app.schemas.task import (
    TaskCreate, TaskResponse, TaskUpdate, 
    TaskExecuteRequest, TaskExecuteResponse
)
from app.core.security import get_current_active_user
from app.services.agent_service import AgentService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    task = TaskModel(
        name=task_data.name,
        description=task_data.description,
        input_data=task_data.input_data,
        owner_id=current_user.id,
        workflow_id=task_data.workflow_id,
        status=TaskStatusEnum.PENDING
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[TaskStatusEnum] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(TaskModel).where(TaskModel.owner_id == current_user.id)
    
    if status_filter:
        query = query.where(TaskModel.status == status_filter)
    
    query = query.offset(skip).limit(limit).order_by(TaskModel.created_at.desc())
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_data.name is not None:
        task.name = task_data.name
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.input_data is not None:
        task.input_data = task_data.input_data
    
    await db.commit()
    await db.refresh(task)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()
    
    return None


@router.post("/{task_id}/execute", response_model=TaskExecuteResponse)
async def execute_task(
    task_id: UUID,
    execute_data: TaskExecuteRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TaskModel).where(
            TaskModel.id == task_id,
            TaskModel.owner_id == current_user.id
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status == TaskStatusEnum.RUNNING:
        raise HTTPException(status_code=400, detail="Task is already running")
    
    agent_service = AgentService()
    task_response = await agent_service.execute_task(
        task_id=str(task_id),
        input_data=execute_data.input_data,
        user_id=str(current_user.id)
    )
    
    return TaskExecuteResponse(**task_response)


@router.post("/execute", response_model=TaskExecuteResponse)
async def execute_task_direct(
    execute_data: TaskExecuteRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    task = TaskModel(
        name=f"Quick Task {execute_data.input_data.get('instruction', 'Direct execution')[:50]}",
        input_data=execute_data.input_data,
        owner_id=current_user.id,
        status=TaskStatusEnum.PENDING
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    agent_service = AgentService()
    task_response = await agent_service.execute_task(
        task_id=str(task.id),
        input_data=execute_data.input_data,
        user_id=str(current_user.id)
    )
    
    return TaskExecuteResponse(**task_response)
