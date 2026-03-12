#!/usr/bin/env python3
"""
Communication Agent - Handles human-facing content generation and messaging
With mock data support
"""

import os
import json
import random
from datetime import datetime

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class CommunicationAgent:
    """Handles communication, summarization, and human-facing content"""
    
    def __init__(self, api_key=None, use_mock=False):
        self.use_mock = use_mock or not GEMINI_AVAILABLE
        
        if not self.use_mock and GEMINI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=api_key or os.getenv('GOOGLE_API_KEY'))
            except:
                self.use_mock = True
        else:
            self.use_mock = True
        
        self.system_prompt = self._load_communication_prompt()
        
        # Tone and style preferences
        self.default_tone = "professional"
        self.style_guide = {
            "professional": "Clear, concise, business-appropriate language",
            "friendly": "Warm, approachable, collaborative tone",
            "executive": "High-level, strategic, decision-focused",
            "technical": "Precise, detailed, domain-specific"
        }
        
        # Mock templates
        self.mock_templates = {
            "email": self._mock_email,
            "summary": self._mock_summary,
            "announcement": self._mock_announcement,
            "default": self._mock_default
        }
    
    def _load_communication_prompt(self):
        """Load communication agent system prompt"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "communication_prompt.txt")
            with open(prompt_path, "r", encoding='utf-8') as f:
                return f.read()
        except:
            return """You are the Communication Agent for TaskFlowr. You handle all human-facing content and business communication.

Your responsibilities:
- Draft professional emails and announcements
- Create executive summaries and briefings
- Prepare team communications
- Adapt tone for different audiences

Rules:
- Always maintain professional standards
- Be clear, concise, and actionable
- Adapt tone based on audience and context"""
    
    async def process_communication_task(self, task_description: str, context: dict) -> dict:
        """Process communication-focused tasks"""
        print(f"💬 Communication Agent processing: {task_description}")
        
        # Determine appropriate tone from context
        tone = self._determine_tone(context)
        
        if self.use_mock:
            return await self._process_mock_communication(task_description, context, tone)
        
        prompt = f"""
        SYSTEM: {self.system_prompt}
        
        TONE: {tone}
        STYLE: {self.style_guide.get(tone, 'professional')}
        
        TASK: {task_description}
        
        Create professional, well-structured communication content.
        Focus on clarity, appropriate tone, and actionable information.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3
                )
            )
            
            communication_outputs = self._parse_communication_outputs(response.text, tone)
            
            return {
                "task": task_description,
                "tone_used": tone,
                "communication_outputs": communication_outputs,
                "raw_response": response.text,
                "status": "completed"
            }
            
        except Exception as e:
            print(f"Communication API error: {e}, using mock data")
            return await self._process_mock_communication(task_description, context, tone)
    
    async def _process_mock_communication(self, task_description: str, context: dict, tone: str) -> dict:
        """Process communication task with mock data"""
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ['email', 'draft', 'send']):
            template_type = "email"
        elif any(word in task_lower for word in ['summary', 'briefing', 'executive']):
            template_type = "summary"
        elif any(word in task_lower for word in ['announcement', 'update', 'news']):
            template_type = "announcement"
        else:
            template_type = "default"
        
        mock_output = self.mock_templates[template_type](task_description, tone)
        communication_outputs = self._parse_communication_outputs(mock_output, tone)
        
        return {
            "task": task_description,
            "tone_used": tone,
            "communication_outputs": communication_outputs,
            "raw_response": mock_output,
            "status": "completed",
            "mock_data": True
        }
    
    def _mock_email(self, task: str, tone: str) -> str:
        """Generate mock email"""
        subjects = {
            "sales": "Q4 Sales Performance Update and Key Insights",
            "onboarding": "Welcome to the Team - Onboarding Information",
            "metrics": "Monthly Performance Metrics Review",
            "general": "Important Update Regarding Your Request"
        }
        
        # Determine email subject based on task
        task_lower = task.lower()
        if 'sales' in task_lower:
            subject = subjects['sales']
        elif 'onboarding' in task_lower or 'welcome' in task_lower:
            subject = subjects['onboarding']
        elif 'metrics' in task_lower or 'analysis' in task_lower:
            subject = subjects['metrics']
        else:
            subject = subjects['general']
        
        greetings = {
            "professional": "Dear Team,",
            "friendly": "Hello everyone!",
            "executive": "To the Leadership Team:",
            "technical": "Team,"
        }
        
        closings = {
            "professional": "Best regards,\n[Your Name]",
            "friendly": "Looking forward to our continued collaboration!\nBest,",
            "executive": "Sincerely,\n[Executive Name]",
            "technical": "Regards,\n[Your Name]"
        }
        
        return f"""
Subject: {subject}

{greetings.get(tone, greetings['professional'])}

I'm writing to provide an update regarding: {task}

Based on our recent analysis and review, here are the key points:

• We have successfully processed your request through our automated workflow system
• The necessary outputs and documentation have been generated
• Next steps include reviewing the materials and implementing the recommendations

Key accomplishments:
- Automated processing completed successfully
- All requested deliverables prepared
- Quality assurance checks passed

Please review the attached materials and let me know if you have any questions or require additional information.

{closings.get(tone, closings['professional'])}

*This communication was drafted by TaskFlowr Communication Agent*
"""
    
    def _mock_summary(self, task: str, tone: str) -> str:
        """Generate mock executive summary"""
        return f"""
# Executive Summary
**Prepared for:** {task}
**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Tone:** {tone.capitalize()}

## Key Takeaways

1. **Strategic Insight**: The analysis reveals significant opportunities for optimization in current processes.

2. **Performance Metrics**: Key indicators show {random.randint(5, 15)}% improvement potential in target areas.

3. **Recommendations**: 
   - Implement automated workflow enhancements
   - Streamline communication channels
   - Establish continuous monitoring

## Action Items

- Review detailed analysis report
- Schedule implementation planning session
- Assign ownership for key initiatives
- Set measurable success criteria

## Next Steps

1. Immediate (1-2 weeks): Initial implementation planning
2. Short-term (1 month): Process optimization rollout
3. Medium-term (3 months): Performance review and adjustment

*Summary generated by TaskFlowr Communication Agent*
"""
    
    def _mock_announcement(self, task: str, tone: str) -> str:
        """Generate mock team announcement"""
        return f"""
# Team Announcement

**Subject:** Important Update Regarding {task.split(' for ')[0] if ' for ' in task else 'Recent Initiatives'}

Hello Team,

I'm excited to share some important updates regarding our ongoing efforts to streamline operations and enhance productivity.

## What's New

We've successfully implemented automated workflow processing for: {task}

## Key Benefits

• **Efficiency**: Reduced manual processing time by estimated {random.randint(40, 70)}%
• **Accuracy**: Automated quality checks ensure consistent outputs
• **Scalability**: System can handle increasing request volumes
• **Accessibility**: Team members can submit requests easily

## What This Means for You

- Faster turnaround times for similar requests
- Consistent, high-quality outputs
- More time to focus on strategic initiatives
- Improved collaboration through standardized processes

## Getting Started

The new automated system is now available for team use. Training materials and documentation will be shared in the coming days.

We're confident these enhancements will significantly improve our team's effectiveness and allow us to deliver even greater value.

Thank you for your adaptability and commitment to continuous improvement!

Best regards,
The Operations Team

*Announcement drafted by TaskFlowr Communication Agent*
"""
    
    def _mock_default(self, task: str, tone: str) -> str:
        """Default mock communication"""
        return f"""
# Communication Output
**Task:** {task}
**Tone:** {tone}

## Professional Communication Draft

Dear Recipient,

This communication serves to inform you that your request has been processed through our automated communication system.

**Request Details:**
- Task: {task}
- Status: Completed
- Processing Date: {datetime.now().strftime("%Y-%m-%d")}

**Key Message:**
Your request has been successfully handled by our multi-agent automation system. The Communication Agent has prepared this professional draft to ensure clear and effective information delivery.

**Next Steps:**
Please review the information provided and feel free to reach out if you require any modifications or additional details.

We appreciate the opportunity to assist you with this matter.

Sincerely,
TaskFlowr Communication System

*This is a mock communication generated for demonstration purposes*
"""
    
    def _determine_tone(self, context: dict) -> str:
        """Determine appropriate tone from context"""
        user_prefs = context.get("user_preferences", {})
        current_context = context.get("current_context", {})
        
        # Check for explicit tone preference
        if "tone" in user_prefs:
            return user_prefs["tone"]
        
        # Infer tone from context
        task_type = str(current_context.get("task_type", "")).lower()
        audience = str(current_context.get("audience", "")).lower()
        
        if any(word in task_type for word in ["executive", "leadership", "ceo", "board"]):
            return "executive"
        elif any(word in audience for word in ["team", "colleagues", "internal", "staff"]):
            return "friendly"
        elif any(word in task_type for word in ["technical", "engineering", "development", "code"]):
            return "technical"
        else:
            return "professional"
    
    def _parse_communication_outputs(self, response_text: str, tone: str) -> dict:
        """Parse communication outputs from agent response"""
        outputs = {
            "emails": self._extract_emails(response_text),
            "summaries": self._extract_summaries(response_text),
            "announcements": self._extract_announcements(response_text),
            "general_content": {
                "type": "communication",
                "content": response_text,
                "tone": tone,
                "word_count": len(response_text.split())
            }
        }
        return outputs
    
    def _extract_emails(self, text: str) -> list:
        """Extract email-like content"""
        emails = []
        lines = text.split('\n')
        
        # Look for email structure
        if any(keyword in text.lower() for keyword in ['dear', 'subject:', 'regards', 'sincerely']):
            email_content = {
                "subject": self._extract_subject(lines),
                "greeting": self._extract_greeting(lines),
                "body": self._extract_body(text),
                "closing": self._extract_closing(lines),
                "type": "email"
            }
            emails.append(email_content)
        
        return emails
    
    def _extract_summaries(self, text: str) -> list:
        """Extract summary content"""
        summaries = []
        if any(keyword in text.lower() for keyword in ['summary', 'key takeaways', 'executive']):
            summaries.append({
                "type": "summary",
                "key_points": self._extract_bullet_points(text),
                "overview": text[:200] + "..." if len(text) > 200 else text
            })
        return summaries
    
    def _extract_announcements(self, text: str) -> list:
        """Extract announcement content"""
        announcements = []
        if any(keyword in text.lower() for keyword in ['announce', 'update', 'team', 'news']):
            announcements.append({
                "type": "announcement",
                "key_message": self._extract_key_message(text),
                "action_items": self._extract_bullet_points(text)
            })
        return announcements
    
    def _extract_subject(self, lines: list) -> str:
        """Extract subject line from text"""
        for line in lines:
            if line.lower().startswith('subject:'):
                return line[8:].strip()
        return "Communication Update"
    
    def _extract_greeting(self, lines: list) -> str:
        """Extract greeting from text"""
        for line in lines:
            if line.lower().startswith('dear') or line.lower().startswith('hello') or line.lower().startswith('to the'):
                return line.strip()
        return "Dear Team,"
    
    def _extract_body(self, text: str) -> str:
        """Extract main body content"""
        lines = text.split('\n')
        body_lines = []
        in_body = False
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith('dear') or line.lower().startswith('hello'):
                in_body = True
                continue
            if in_body and any(line.lower().startswith(closing) for closing in ['best', 'regards', 'sincerely', 'thank you']):
                break
            if in_body and line and not line.startswith('Subject:'):
                body_lines.append(line)
        
        return '\n'.join(body_lines) if body_lines else text
    
    def _extract_closing(self, lines: list) -> str:
        """Extract closing from text"""
        for line in lines:
            line_lower = line.lower()
            if any(line_lower.startswith(closing) for closing in ['best', 'regards', 'sincerely', 'thank you']):
                return line.strip()
        return "Best regards,\nTaskFlowr System"
    
    def _extract_bullet_points(self, text: str) -> list:
        """Extract bullet points from text"""
        points = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if (line.startswith('-') or line.startswith('•') or 
                (len(line) > 2 and line[0].isdigit() and line[1] == '.') or
                line.startswith('*')):
                points.append(line)
        
        return points if points else ["Key point extracted from communication"]
    
    def _extract_key_message(self, text: str) -> str:
        """Extract the main message from text"""
        sentences = text.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 20:
                return sentence
        return text[:100] + "..." if len(text) > 100 else text


def create_communication_agent(api_key=None, use_mock=False) -> CommunicationAgent:
    """Factory function for communication agent"""
    return CommunicationAgent(api_key, use_mock)