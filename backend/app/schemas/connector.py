from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


class ConnectorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    connector_type: str = Field(..., min_length=1, max_length=100)
    config: Optional[Dict[str, Any]] = None


class ConnectorCreate(ConnectorBase):
    credentials: Dict[str, Any]


class ConnectorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    config: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ConnectorResponse(ConnectorBase):
    id: UUID
    is_active: bool
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConnectorTestRequest(BaseModel):
    connector_type: str
    credentials: Dict[str, Any]


class ConnectorTestResponse(BaseModel):
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None


class WebhookBase(BaseModel):
    url: str = Field(..., min_length=1, max_length=500)
    events: List[str] = []


class WebhookCreate(WebhookBase):
    secret: Optional[str] = None


class WebhookResponse(WebhookBase):
    id: UUID
    secret: Optional[str] = None
    is_active: bool
    owner_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
