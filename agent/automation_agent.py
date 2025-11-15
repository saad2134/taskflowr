#!/usr/bin/env python3
"""
Automation Agent - Handles structured data processing and operational tasks
"""

import os
import json
import pandas as pd
from adk import Agent
from adk.agents import GeminiAgent


class AutomationAgent:
    """Handles structured, data-driven automation tasks"""
    
    def __init__(self):
        self.agent = GeminiAgent(
            model="gemini-2.0-flash-exp",
            system_prompt=self._load_automation_prompt(),
            tools=self._load_automation_tools()
        )
    
    def _load_automation_prompt(self):
        """Load automation agent system prompt"""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "automation_prompt.txt")
        with open(prompt_path, "r") as f:
            return f.read()
    
    def _load_automation_tools(self):
        """Load tools for automation tasks"""
        # In production, these would be actual ADK tools
        return [
            {
                "name": "generate_checklist",
                "description": "Generate structured checklists and SOPs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "items": {"type": "array", "items": {"type": "string"}},
                        "categories": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            {
                "name": "process_data_template",
                "description": "Create data processing templates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "template_type": {"type": "string"},
                        "fields": {"type": "array", "items": {"type": "string"}},
                        "format": {"type": "string"}
                    }
                }
            },
            {
                "name": "generate_workflow",
                "description": "Create workflow diagrams and process maps",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "process_name": {"type": "string"},
                        "steps": {"type": "array", "items": {"type": "string"}},
                        "dependencies": {"type": "object"}
                    }
                }
            }
        ]
    
    async def process_automation_task(self, task_description: str, context: dict) -> dict:
        """Process automation-focused tasks"""
        print(f"⚙️ Automation Agent processing: {task_description}")
        
        prompt = f"""
        TASK: {task_description}
        CONTEXT: {json.dumps(context, indent=2)}
        
        As Automation Agent, your role is to handle structured, operational tasks.
        
        Based on the task, determine what structured outputs are needed:
        - Checklists/SOPs
        - Data templates
        - Workflow diagrams
        - Process documentation
        - Structured reports
        
        Generate appropriate structured outputs using available tools.
        """
        
        response = await self.agent.generate_async(prompt)
        
        # Parse tool calls from response
        structured_outputs = self._parse_automation_outputs(response.text)
        
        return {
            "task": task_description,
            "structured_outputs": structured_outputs,
            "raw_response": response.text,
            "tools_used": [tool_call.get("name", "unknown") for tool_call in structured_outputs.get("tool_calls", [])]
        }
    
    def _parse_automation_outputs(self, response_text: str) -> dict:
        """Parse structured outputs from agent response"""
        try:
            # Look for JSON blocks in response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            else:
                # Fallback: extract structured content
                return {
                    "checklists": self._extract_checklists(response_text),
                    "templates": self._extract_templates(response_text),
                    "workflows": self._extract_workflows(response_text),
                    "tool_calls": []
                }
        except Exception as e:
            return {"error": str(e), "raw_text": response_text}
    
    def _extract_checklists(self, text: str) -> list:
        """Extract checklist items from text"""
        checklists = []
        lines = text.split('\n')
        current_checklist = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('- [ ]') or line.startswith('- [x]') or line.startswith('•'):
                if current_checklist:
                    current_checklist['items'].append(line)
            elif line and not line.startswith('#') and len(line) < 100:
                if current_checklist:
                    checklists.append(current_checklist)
                current_checklist = {'title': line, 'items': []}
        
        if current_checklist:
            checklists.append(current_checklist)
        
        return checklists
    
    def _extract_templates(self, text: str) -> list:
        """Extract template structures from text"""
        templates = []
        # Simple extraction logic - in production would use more sophisticated parsing
        if "template" in text.lower() or "format" in text.lower():
            templates.append({
                "type": "data_template",
                "fields": ["field1", "field2", "field3"],  # Placeholder
                "description": "Extracted template"
            })
        return templates
    
    def _extract_workflows(self, text: str) -> list:
        """Extract workflow steps from text"""
        workflows = []
        lines = text.split('\n')
        steps = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['step', 'phase', 'stage']):
                steps.append(line.strip())
        
        if steps:
            workflows.append({
                "name": "Extracted Workflow",
                "steps": steps,
                "step_count": len(steps)
            })
        
        return workflows


def create_automation_agent() -> AutomationAgent:
    """Factory function for automation agent"""
    return AutomationAgent()