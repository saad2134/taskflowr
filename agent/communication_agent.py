#!/usr/bin/env python3
"""
Communication Agent - Handles human-facing content generation and messaging
"""

import os
import json
from adk.agents import GeminiAgent


class CommunicationAgent:
    """Handles communication, summarization, and human-facing content"""
    
    def __init__(self):
        self.agent = GeminiAgent(
            model="gemini-2.0-flash-exp",
            system_prompt=self._load_communication_prompt(),
            tools=self._load_communication_tools()
        )
        
        # Tone and style preferences
        self.default_tone = "professional"
        self.style_guide = {
            "professional": "Clear, concise, business-appropriate language",
            "friendly": "Warm, approachable, collaborative tone",
            "executive": "High-level, strategic, decision-focused",
            "technical": "Precise, detailed, domain-specific"
        }
    
    def _load_communication_prompt(self):
        """Load communication agent system prompt"""
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "communication_prompt.txt")
        with open(prompt_path, "r") as f:
            return f.read()
    
    def _load_communication_tools(self):
        """Load tools for communication tasks"""
        return [
            {
                "name": "draft_email",
                "description": "Draft professional emails",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient": {"type": "string"},
                        "subject": {"type": "string"},
                        "body": {"type": "string"},
                        "tone": {"type": "string"},
                        "key_points": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            {
                "name": "create_summary",
                "description": "Create executive summaries and briefs",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "audience": {"type": "string"},
                        "length": {"type": "string"},
                        "key_takeaways": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            {
                "name": "generate_announcement",
                "description": "Create team announcements and updates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "audience": {"type": "string"},
                        "key_message": {"type": "string"},
                        "action_items": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        ]
    
    async def process_communication_task(self, task_description: str, context: dict) -> dict:
        """Process communication-focused tasks"""
        print(f"💬 Communication Agent processing: {task_description}")
        
        # Determine appropriate tone from context
        tone = self._determine_tone(context)
        
        prompt = f"""
        TASK: {task_description}
        CONTEXT: {json.dumps(context, indent=2)}
        TONE: {tone}
        STYLE GUIDE: {self.style_guide.get(tone, 'professional')}
        
        As Communication Agent, your role is to create clear, effective human-facing content.
        
        Based on the task, determine what communication outputs are needed:
        - Email drafts
        - Executive summaries
        - Team announcements
        - Meeting notes
        - Instructions/documentation
        
        Generate polished, professional content using the specified tone.
        """
        
        response = await self.agent.generate_async(prompt)
        
        communication_outputs = self._parse_communication_outputs(response.text, tone)
        
        return {
            "task": task_description,
            "tone_used": tone,
            "communication_outputs": communication_outputs,
            "raw_response": response.text
        }
    
    def _determine_tone(self, context: dict) -> str:
        """Determine appropriate tone from context"""
        user_prefs = context.get("user_preferences", {})
        current_context = context.get("current_context", {})
        
        # Check for explicit tone preference
        if "tone" in user_prefs:
            return user_prefs["tone"]
        
        # Infer tone from context
        task_type = current_context.get("task_type", "")
        audience = current_context.get("audience", "")
        
        if any(word in task_type.lower() for word in ["executive", "leadership", "ceo"]):
            return "executive"
        elif any(word in audience.lower() for word in ["team", "colleagues", "internal"]):
            return "friendly"
        elif any(word in task_type.lower() for word in ["technical", "engineering", "development"]):
            return "technical"
        else:
            return "professional"
    
    def _parse_communication_outputs(self, response_text: str, tone: str) -> dict:
        """Parse communication outputs from agent response"""
        outputs = {
            "emails": [],
            "summaries": [],
            "announcements": [],
            "other_content": []
        }
        
        # Extract email-like content
        if "subject:" in response_text.lower() or "dear" in response_text.lower():
            email_content = self._extract_email_content(response_text)
            if email_content:
                outputs["emails"].append(email_content)
        
        # Extract summary content
        if any(keyword in response_text.lower() for keyword in ["summary", "key takeaways", "executive brief"]):
            summary_content = self._extract_summary_content(response_text)
            if summary_content:
                outputs["summaries"].append(summary_content)
        
        # Extract announcement content
        if any(keyword in response_text.lower() for keyword in ["announce", "update", "team news"]):
            announcement_content = self._extract_announcement_content(response_text)
            if announcement_content:
                outputs["announcements"].append(announcement_content)
        
        # If no specific type detected, add as general content
        if not any(outputs.values()):
            outputs["other_content"].append({
                "type": "general_communication",
                "content": response_text,
                "tone": tone,
                "word_count": len(response_text.split())
            })
        
        return outputs
    
    def _extract_email_content(self, text: str) -> dict:
        """Extract email structure from text"""
        lines = text.split('\n')
        email = {
            "subject": "",
            "greeting": "",
            "body": "",
            "closing": ""
        }
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line.lower().startswith('subject:'):
                email["subject"] = line[8:].strip()
            elif line.lower().startswith('dear'):
                email["greeting"] = line
            elif any(line.lower().startswith(closing) for closing in ['best', 'regards', 'sincerely', 'thank you']):
                email["closing"] = line
        
        # Extract body (content between greeting and closing)
        if email["greeting"]:
            start_idx = text.find(email["greeting"]) + len(email["greeting"])
            if email["closing"]:
                end_idx = text.find(email["closing"])
                email["body"] = text[start_idx:end_idx].strip()
            else:
                email["body"] = text[start_idx:].strip()
        
        return email if any(email.values()) else None
    
    def _extract_summary_content(self, text: str) -> dict:
        """Extract summary structure from text"""
        return {
            "type": "executive_summary",
            "key_points": self._extract_bullet_points(text),
            "overview": text[:200] + "..." if len(text) > 200 else text
        }
    
    def _extract_announcement_content(self, text: str) -> dict:
        """Extract announcement structure from text"""
        return {
            "type": "team_announcement",
            "key_message": self._extract_key_message(text),
            "action_items": self._extract_bullet_points(text)
        }
    
    def _extract_bullet_points(self, text: str) -> list:
        """Extract bullet points or numbered items from text"""
        points = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if (line.startswith('-') or line.startswith('•') or 
                (line[:2].isdigit() and line[2] == '.') or
                line.startswith('*')):
                points.append(line)
        
        return points
    
    def _extract_key_message(self, text: str) -> str:
        """Extract the main message from text"""
        sentences = text.split('.')
        if sentences:
            return sentences[0].strip()
        return text[:100] + "..." if len(text) > 100 else text


def create_communication_agent() -> CommunicationAgent:
    """Factory function for communication agent"""
    return CommunicationAgent()