from fastapi import APIRouter

from app.api.routes import auth, tasks, workflows, executions, connectors

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(tasks.router)
api_router.include_router(workflows.router)
api_router.include_router(executions.router)
api_router.include_router(connectors.router)
api_router.include_router(connectors.webhook_router)
