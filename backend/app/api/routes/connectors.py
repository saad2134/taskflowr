from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
import secrets

from app.db.session import get_db
from app.models.user import User, Connector as ConnectorModel, Webhook as WebhookModel
from app.schemas.connector import (
    ConnectorCreate, ConnectorResponse, ConnectorUpdate,
    ConnectorTestRequest, ConnectorTestResponse,
    WebhookCreate, WebhookResponse
)
from app.core.security import get_current_active_user
from app.connectors.registry import get_connector

router = APIRouter(prefix="/connectors", tags=["connectors"])


@router.post("", response_model=ConnectorResponse, status_code=status.HTTP_201_CREATED)
async def create_connector(
    connector_data: ConnectorCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    connector = ConnectorModel(
        name=connector_data.name,
        connector_type=connector_data.connector_type,
        config=connector_data.config,
        credentials=connector_data.credentials,
        owner_id=current_user.id
    )
    
    db.add(connector)
    await db.commit()
    await db.refresh(connector)
    
    return connector


@router.get("", response_model=List[ConnectorResponse])
async def list_connectors(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConnectorModel).where(ConnectorModel.owner_id == current_user.id)
    )
    connectors = result.scalars().all()
    return connectors


@router.get("/{connector_id}", response_model=ConnectorResponse)
async def get_connector(
    connector_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConnectorModel).where(
            ConnectorModel.id == connector_id,
            ConnectorModel.owner_id == current_user.id
        )
    )
    connector = result.scalar_one_or_none()
    
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    return connector


@router.put("/{connector_id}", response_model=ConnectorResponse)
async def update_connector(
    connector_id: UUID,
    connector_data: ConnectorUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConnectorModel).where(
            ConnectorModel.id == connector_id,
            ConnectorModel.owner_id == current_user.id
        )
    )
    connector = result.scalar_one_or_none()
    
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    if connector_data.name is not None:
        connector.name = connector_data.name
    if connector_data.config is not None:
        connector.config = connector_data.config
    if connector_data.credentials is not None:
        connector.credentials = connector_data.credentials
    if connector_data.is_active is not None:
        connector.is_active = connector_data.is_active
    
    await db.commit()
    await db.refresh(connector)
    
    return connector


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connector(
    connector_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConnectorModel).where(
            ConnectorModel.id == connector_id,
            ConnectorModel.owner_id == current_user.id
        )
    )
    connector = result.scalar_one_or_none()
    
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    await db.delete(connector)
    await db.commit()
    
    return None


@router.post("/test", response_model=ConnectorTestResponse)
async def test_connector(
    test_data: ConnectorTestRequest,
    current_user: User = Depends(get_current_active_user)
):
    connector = get_connector(test_data.connector_type, test_data.credentials)
    
    if not connector:
        return ConnectorTestResponse(
            success=False,
            message=f"Unknown connector type: {test_data.connector_type}"
        )
    
    result = await connector.test_connection()
    return ConnectorTestResponse(**result)


webhook_router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@webhook_router.post("", response_model=WebhookResponse, status_code=status.HTTP_201_CREATED)
async def create_webhook(
    webhook_data: WebhookCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    webhook = WebhookModel(
        url=webhook_data.url,
        events=webhook_data.events,
        secret=webhook_data.secret or secrets.token_urlsafe(32),
        owner_id=current_user.id
    )
    
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    
    return webhook


@webhook_router.get("", response_model=List[WebhookResponse])
async def list_webhooks(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WebhookModel).where(WebhookModel.owner_id == current_user.id)
    )
    webhooks = result.scalars().all()
    return webhooks


@webhook_router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_webhook(
    webhook_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(WebhookModel).where(
            WebhookModel.id == webhook_id,
            WebhookModel.owner_id == current_user.id
        )
    )
    webhook = result.scalar_one_or_none()
    
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    await db.delete(webhook)
    await db.commit()
    
    return None
