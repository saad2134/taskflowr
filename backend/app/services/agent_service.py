import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.user import Task as TaskModel, TaskStatus as TaskStatusEnum
from app.models.user import Execution as ExecutionModel, ExecutionStatus as ExecutionStatusEnum
from app.models.user import Workflow as WorkflowModel


class AgentService:
    def __init__(self):
        self.coordinator = None
    
    async def _init_coordinator(self):
        if self.coordinator is None:
            try:
                from agent.coordinator import CoordinatorAgent
                self.coordinator = CoordinatorAgent()
            except ImportError:
                pass
    
    async def execute_task(
        self,
        task_id: str,
        input_data: Dict[str, Any],
        user_id: str,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        execution_id = str(uuid.uuid4())
        
        if db:
            execution = ExecutionModel(
                id=uuid.UUID(execution_id),
                input_data=input_data,
                owner_id=uuid.UUID(user_id),
                task_id=uuid.UUID(task_id),
                status=ExecutionStatusEnum.RUNNING
            )
            db.add(execution)
            
            await db.execute(
                update(TaskModel)
                .where(TaskModel.id == uuid.UUID(task_id))
                .values(status=TaskStatusEnum.RUNNING)
            )
            await db.commit()
        
        try:
            await self._init_coordinator()
            
            instruction = input_data.get("instruction", "")
            
            if self.coordinator:
                result = await self.coordinator.run(instruction)
            else:
                await asyncio.sleep(1)
                result = {
                    "status": "completed",
                    "output": f"Processed: {instruction}",
                    "type": "task_execution"
                }
            
            output_data = {
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if db:
                await db.execute(
                    update(ExecutionModel)
                    .where(ExecutionModel.id == uuid.UUID(execution_id))
                    .values(
                        output_data=output_data,
                        status=ExecutionStatusEnum.COMPLETED,
                        completed_at=datetime.utcnow()
                    )
                )
                
                await db.execute(
                    update(TaskModel)
                    .where(TaskModel.id == uuid.UUID(task_id))
                    .values(
                        status=TaskStatusEnum.COMPLETED,
                        output_data=output_data,
                        completed_at=datetime.utcnow()
                    )
                )
                await db.commit()
            
            return {
                "task_id": task_id,
                "execution_id": execution_id,
                "status": "completed",
                "message": "Task executed successfully"
            }
            
        except Exception as e:
            error_message = str(e)
            
            if db:
                await db.execute(
                    update(ExecutionModel)
                    .where(ExecutionModel.id == uuid.UUID(execution_id))
                    .values(
                        error_message=error_message,
                        status=ExecutionStatusEnum.FAILED,
                        completed_at=datetime.utcnow()
                    )
                )
                
                await db.execute(
                    update(TaskModel)
                    .where(TaskModel.id == uuid.UUID(task_id))
                    .values(
                        status=TaskStatusEnum.FAILED,
                        error_message=error_message,
                        completed_at=datetime.utcnow()
                    )
                )
                await db.commit()
            
            return {
                "task_id": task_id,
                "execution_id": execution_id,
                "status": "failed",
                "message": error_message
            }
    
    async def execute_workflow(
        self,
        workflow_id: str,
        input_data: Dict[str, Any],
        user_id: str,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        execution_id = str(uuid.uuid4())
        
        if db:
            execution = ExecutionModel(
                id=uuid.UUID(execution_id),
                input_data=input_data,
                owner_id=uuid.UUID(user_id),
                workflow_id=uuid.UUID(workflow_id),
                status=ExecutionStatusEnum.RUNNING
            )
            db.add(execution)
            await db.commit()
        
        try:
            result = await self._run_workflow_steps(workflow_id, input_data)
            
            if db:
                await db.execute(
                    update(ExecutionModel)
                    .where(ExecutionModel.id == uuid.UUID(execution_id))
                    .values(
                        output_data=result,
                        status=ExecutionStatusEnum.COMPLETED,
                        completed_at=datetime.utcnow()
                    )
                )
                await db.commit()
            
            return {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "status": "completed",
                "message": "Workflow executed successfully"
            }
            
        except Exception as e:
            if db:
                await db.execute(
                    update(ExecutionModel)
                    .where(ExecutionModel.id == uuid.UUID(execution_id))
                    .values(
                        error_message=str(e),
                        status=ExecutionStatusEnum.FAILED,
                        completed_at=datetime.utcnow()
                    )
                )
                await db.commit()
            
            return {
                "workflow_id": workflow_id,
                "execution_id": execution_id,
                "status": "failed",
                "message": str(e)
            }
    
    async def _run_workflow_steps(
        self,
        workflow_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        await self._init_coordinator()
        
        if self.coordinator:
            instruction = input_data.get("instruction", "")
            result = await self.coordinator.run(instruction)
            return {"result": result}
        
        return {"result": "Workflow executed", "steps_completed": []}


agent_service = AgentService()
