from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class WorkflowStep(BaseModel):
    id: str
    name: str
    agent_type: str
    config: Dict[str, Any] = {}
    dependencies: List[str] = []


class WorkflowDefinition(BaseModel):
    steps: List[WorkflowStep]
    metadata: Dict[str, Any] = {}


class WorkflowBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    definition: Optional[WorkflowDefinition] = None
    schedule: Optional[str] = None


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    definition: Optional[WorkflowDefinition] = None
    schedule: Optional[str] = None
    status: Optional[WorkflowStatus] = None


class WorkflowResponse(WorkflowBase):
    id: UUID
    status: WorkflowStatus
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowExecuteRequest(BaseModel):
    input_data: Dict[str, Any]


class WorkflowExecuteResponse(BaseModel):
    workflow_id: UUID
    execution_id: UUID
    status: str
    message: str
