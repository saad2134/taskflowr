from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class ExecutionStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionBase(BaseModel):
    input_data: Optional[Dict[str, Any]] = None


class ExecutionResponse(ExecutionBase):
    id: UUID
    output_data: Optional[Dict[str, Any]] = None
    logs: Optional[Dict[str, Any]] = None
    status: ExecutionStatus
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None
    owner_id: UUID
    task_id: Optional[UUID] = None
    workflow_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ExecutionListResponse(BaseModel):
    executions: List[ExecutionResponse]
    total: int
    page: int
    page_size: int
