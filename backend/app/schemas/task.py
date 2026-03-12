from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None


class TaskCreate(TaskBase):
    workflow_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None


class TaskResponse(TaskBase):
    id: UUID
    output_data: Optional[Dict[str, Any]] = None
    status: TaskStatus
    error_message: Optional[str] = None
    owner_id: UUID
    workflow_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskExecuteRequest(BaseModel):
    input_data: Dict[str, Any]


class TaskExecuteResponse(BaseModel):
    task_id: UUID
    execution_id: UUID
    status: TaskStatus
    message: str
