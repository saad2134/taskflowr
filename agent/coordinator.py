#!/usr/bin/env python3
"""
Coordinator Agent - Main orchestrator for TaskFlowr multi-agent system
"""

import os
import json
import asyncio
from datetime import datetime
from adk import Agent, participants
from adk.agents import GeminiAgent
from adk.application import app
from adk.messages import Message

# Import sub-agents
from .automation_agent import create_automation_agent
from .communication_agent import create_communication_agent


class CoordinatorAgent:
    """Main coordinator that orchestrates workflow between specialized agents"""
    
    def __init__(self):
        self.agent = GeminiAgent(
            model="gemini-2.0-flash-exp",
            system_prompt=self._load_coordinator_prompt(),
            tools=[]  # Coordinator uses A2A, not direct tools
        )
        
        # Initialize sub-agents
        self.automation_agent = create_automation_agent()
        self.communication_agent = create_communication_agent()
        
        # Session memory
        self.session_memory = {
            "user_preferences": {},
            "workflow_history": [],
            "current_context": {}
        }
    
    def _load_coordinator_prompt(self):
        """Load the coordinator system prompt"""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "coordinator_prompt.txt")
        with open(prompt_path, "r") as f:
            return f.read()
    
    async def process_user_request(self, user_input: str, context: dict = None):
        """
        Main entry point for processing user requests
        """
        print(f"🔄 Coordinator received request: {user_input}")
        
        # Update session context
        if context:
            self.session_memory["current_context"].update(context)
        
        # Analyze intent and decompose task
        task_analysis = await self._analyze_intent(user_input)
        
        # Route to appropriate agents
        results = await self._route_to_agents(task_analysis)
        
        # Assemble final output
        final_output = await self._assemble_final_output(results, user_input)
        
        # Log workflow
        self._log_workflow(user_input, task_analysis, results)
        
        return final_output
    
    async def _analyze_intent(self, user_input: str) -> dict:
        """Analyze user intent and decompose tasks"""
        analysis_prompt = f"""
        USER REQUEST: {user_input}
        
        Analyze this request and determine:
        1. Main intent category (data_processing, communication, workflow, hybrid)
        2. Subtasks needed
        3. Which agent should handle each subtask (automation/communication/both)
        4. Expected outputs
        
        Return JSON format:
        {{
            "intent": "category",
            "subtasks": [
                {{
                    "description": "task description", 
                    "agent": "automation|communication",
                    "priority": "high|medium|low"
                }}
            ],
            "dependencies": ["task1 must complete before task2"],
            "expected_outputs": ["list", "of", "expected", "outputs"]
        }}
        """
        
        response = await self.agent.generate_async(analysis_prompt)
        
        try:
            # Extract JSON from response
            json_str = response.text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except:
            # Fallback analysis
            return {
                "intent": "hybrid",
                "subtasks": [
                    {"description": "Process structured components", "agent": "automation", "priority": "high"},
                    {"description": "Generate communication elements", "agent": "communication", "priority": "high"}
                ],
                "dependencies": [],
                "expected_outputs": ["final_deliverable"]
            }
    
    async def _route_to_agents(self, task_analysis: dict) -> dict:
        """Route subtasks to appropriate agents"""
        results = {}
        
        for subtask in task_analysis["subtasks"]:
            agent_type = subtask["agent"]
            task_desc = subtask["description"]
            
            print(f"🔄 Routing to {agent_type}: {task_desc}")
            
            if agent_type == "automation":
                results["automation"] = await self.automation_agent.process_automation_task(
                    task_desc, self.session_memory
                )
            elif agent_type == "communication":
                results["communication"] = await self.communication_agent.process_communication_task(
                    task_desc, self.session_memory
                )
        
        return results
    
    async def _assemble_final_output(self, agent_results: dict, original_request: str) -> dict:
        """Assemble final output from agent results"""
        assembly_prompt = f"""
        ORIGINAL REQUEST: {original_request}
        
        AGENT RESULTS:
        {json.dumps(agent_results, indent=2)}
        
        Assemble these into a cohesive final deliverable. Include:
        - Executive summary
        - Key findings/outputs
        - Action items
        - Next steps
        
        Return structured JSON response.
        """
        
        response = await self.agent.generate_async(assembly_prompt)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "original_request": original_request,
            "final_output": response.text,
            "component_results": agent_results,
            "status": "completed"
        }
    
    def _log_workflow(self, user_input: str, analysis: dict, results: dict):
        """Log workflow for observability"""
        workflow_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "analysis": analysis,
            "results_keys": list(results.keys()),
            "status": "completed"
        }
        self.session_memory["workflow_history"].append(workflow_entry)


# Singleton instance
_coordinator_instance = None

def create_coordinator() -> CoordinatorAgent:
    """Factory function to create coordinator instance"""
    global _coordinator_instance
    if _coordinator_instance is None:
        _coordinator_instance = CoordinatorAgent()
    return _coordinator_instance


# CLI interface for testing
async def main():
    """Test the coordinator agent"""
    coordinator = create_coordinator()
    
    test_requests = [
        "Create a sales report for Q4 and email summary to team",
        "Generate onboarding checklist for new engineers and draft welcome email",
        "Analyze monthly metrics and prepare executive briefing"
    ]
    
    for request in test_requests:
        print(f"\n🎯 Testing: {request}")
        result = await coordinator.process_user_request(request)
        print(f"📦 Result: {result['status']}")
        print(f"📄 Output: {result['final_output'][:200]}...")

if __name__ == "__main__":
    asyncio.run(main())