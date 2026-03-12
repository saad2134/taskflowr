#!/usr/bin/env python3
"""
Automation Agent - Handles structured data processing and operational tasks
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


class AutomationAgent:
    """Handles structured, data-driven automation tasks"""
    
    def __init__(self, api_key=None, use_mock=False):
        self.use_mock = use_mock or not GEMINI_AVAILABLE
        
        if not self.use_mock and GEMINI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=api_key or os.getenv('GOOGLE_API_KEY'))
            except:
                self.use_mock = True
        else:
            self.use_mock = True
        
        self.system_prompt = self._load_automation_prompt()
        
        # Mock data templates
        self.mock_templates = {
            "sales_report": self._mock_sales_report,
            "checklist": self._mock_checklist,
            "metrics": self._mock_metrics,
            "onboarding": self._mock_onboarding,
            "default": self._mock_default
        }
    
    def _load_automation_prompt(self):
        """Load automation agent system prompt"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "automation_prompt.txt")
            with open(prompt_path, "r", encoding='utf-8') as f:
                return f.read()
        except:
            return """You are the Automation Agent for TaskFlowr. You handle structured, operational, and data-driven tasks.

Your capabilities:
- Generate checklists and SOPs
- Create data templates and structures
- Design workflows and processes
- Produce structured reports

Rules:
- Output must be structured, concise, and actionable
- Use clear formatting with bullet points and sections
- Focus on practical, implementable outputs"""
    
    async def process_automation_task(self, task_description: str, context: dict) -> dict:
        """Process automation-focused tasks"""
        print(f"⚙️ Automation Agent processing: {task_description}")
        
        if self.use_mock:
            return await self._process_mock_automation(task_description, context)
        
        prompt = f"""
        SYSTEM: {self.system_prompt}
        
        TASK: {task_description}
        
        Generate structured, actionable outputs for this task. Focus on:
        - Checklists and step-by-step procedures
        - Data templates if needed
        - Workflow descriptions
        - Structured recommendations
        
        Format your response clearly with sections and bullet points.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )
            
            structured_outputs = self._parse_automation_outputs(response.text)
            
            return {
                "task": task_description,
                "structured_outputs": structured_outputs,
                "raw_response": response.text,
                "status": "completed"
            }
            
        except Exception as e:
            print(f"Automation API error: {e}, using mock data")
            return await self._process_mock_automation(task_description, context)
    
    async def _process_mock_automation(self, task_description: str, context: dict) -> dict:
        """Process automation task with mock data"""
        # Determine which mock template to use
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ['sales', 'report', 'revenue']):
            template_type = "sales_report"
        elif any(word in task_lower for word in ['checklist', 'onboarding', 'process']):
            template_type = "checklist"
        elif any(word in task_lower for word in ['metrics', 'analysis', 'kpi']):
            template_type = "metrics"
        elif any(word in task_lower for word in ['onboarding', 'welcome', 'new']):
            template_type = "onboarding"
        else:
            template_type = "default"
        
        # Generate mock data
        mock_output = self.mock_templates[template_type](task_description)
        structured_outputs = self._parse_automation_outputs(mock_output)
        
        return {
            "task": task_description,
            "structured_outputs": structured_outputs,
            "raw_response": mock_output,
            "status": "completed",
            "mock_data": True
        }
    
    def _mock_sales_report(self, task: str) -> str:
        """Generate mock sales report"""
        return f"""
# Sales Report Automation
**Generated for:** {task}
**Date:** {datetime.now().strftime("%Y-%m-%d")}

## Quarterly Sales Data
- **Q4 Revenue:** ${random.randint(500000, 1000000):,}
- **Growth vs Q3:** +{random.randint(5, 25)}%
- **Top Performing Products:**
  1. Product X: ${random.randint(150000, 300000):,}
  2. Product Y: ${random.randint(120000, 250000):,}
  3. Product Z: ${random.randint(100000, 200000):,}

## Regional Performance
- **North America:** ${random.randint(200000, 400000):,} (+{random.randint(8, 20)}%)
- **Europe:** ${random.randint(180000, 350000):,} (+{random.randint(5, 15)}%)
- **Asia Pacific:** ${random.randint(120000, 250000):,} (+{random.randint(12, 30)}%)

## Key Metrics Checklist
- [ ] Monthly revenue tracking
- [ ] Product performance analysis
- [ ] Regional growth assessment
- [ ] Competitive positioning
- [ ] Sales team performance review

## Recommended Actions
1. Increase focus on Product X in European markets
2. Develop targeted campaigns for Asia Pacific growth
3. Review sales incentives for underperforming regions
"""
    
    def _mock_checklist(self, task: str) -> str:
        """Generate mock checklist"""
        return f"""
# Automated Checklist Generation
**Task:** {task}

## Comprehensive Checklist

### Preparation Phase
- [ ] Define objectives and success criteria
- [ ] Identify stakeholders and team members
- [ ] Allocate necessary resources
- [ ] Set timeline and milestones

### Execution Phase  
- [ ] Conduct initial assessment
- [ ] Implement core processes
- [ ] Monitor progress and metrics
- [ ] Adjust strategy as needed

### Review Phase
- [ ] Collect feedback from participants
- [ ] Analyze performance data
- [ ] Document lessons learned
- [ ] Plan for continuous improvement

## Quality Assurance Steps
1. Review checklist completeness
2. Validate task dependencies
3. Confirm resource availability
4. Establish success metrics
5. Schedule follow-up review

*Checklist generated automatically by TaskFlowr Automation Agent*
"""
    
    def _mock_metrics(self, task: str) -> str:
        """Generate mock metrics analysis"""
        return f"""
# Metrics Analysis Report
**Analysis Target:** {task}

## Key Performance Indicators
- **Monthly Active Users:** {random.randint(10000, 50000)}
- **Conversion Rate:** {random.uniform(2.5, 8.5):.1f}%
- **Customer Satisfaction:** {random.randint(80, 95)}/100
- **Revenue Growth:** +{random.randint(8, 22)}% MoM

## Trend Analysis
- User engagement increased by {random.randint(5, 15)}% this month
- Conversion rates stable within target range
- Customer satisfaction shows positive trend
- Revenue growth exceeding projections

## Actionable Insights
1. Focus on retaining engaged user segments
2. Optimize conversion funnel steps 3-4
3. Expand successful engagement strategies
4. Monitor satisfaction drivers closely
"""
    
    def _mock_onboarding(self, task: str) -> str:
        """Generate mock onboarding workflow"""
        return f"""
# Onboarding Workflow Automation
**For:** {task}

## 30-60-90 Day Plan

### First 30 Days: Foundation
- [ ] Complete technical setup and access
- [ ] Attend team introductions and orientation
- [ ] Review project documentation and codebase
- [ ] Complete initial training modules
- [ ] Set up development environment

### Days 31-60: Contribution  
- [ ] Take ownership of small features
- [ ] Participate in code reviews
- [ ] Attend team ceremonies and planning
- [ ] Contribute to documentation
- [ ] Begin pairing with senior developers

### Days 61-90: Leadership
- [ ] Lead small feature development
- [ ] Mentor newer team members
- [ ] Participate in architectural discussions
- [ ] Drive process improvements
- [ ] Establish professional development plan

## Success Metrics
- Environment setup within 3 days
- First code contribution within 2 weeks
- Feature ownership within 6 weeks
- Full team integration within 90 days
"""
    
    def _mock_default(self, task: str) -> str:
        """Default mock response"""
        return f"""
# Automated Task Processing
**Task:** {task}

## Structured Output Generated

### Analysis Complete
The Automation Agent has processed your request and generated structured outputs including:
- Task decomposition
- Process workflows
- Quality checkpoints
- Success criteria

### Generated Components
1. **Process Documentation** - Step-by-step procedures
2. **Quality Checklists** - Verification steps
3. **Success Metrics** - Measurable outcomes
4. **Implementation Guide** - Actionable instructions

## Next Steps
Review the generated outputs and customize for your specific implementation context.

*Processed by TaskFlowr Automation Agent*
"""
    
    def _parse_automation_outputs(self, response_text: str) -> dict:
        """Parse structured outputs from agent response"""
        outputs = {
            "checklists": self._extract_checklists(response_text),
            "templates": self._extract_templates(response_text),
            "workflows": self._extract_workflows(response_text),
            "sections": self._extract_sections(response_text)
        }
        return outputs
    
    def _extract_checklists(self, text: str) -> list:
        """Extract checklist items from text"""
        checklists = []
        lines = text.split('\n')
        current_checklist = None
        
        for line in lines:
            line = line.strip()
            if line.startswith(('- [ ]', '- [x]', '• [ ]', '• [x]')):
                if current_checklist:
                    current_checklist['items'].append(line)
                else:
                    current_checklist = {'title': 'Checklist', 'items': [line]}
            elif line and len(line) < 100 and line.startswith('#'):
                if current_checklist and current_checklist['items']:
                    checklists.append(current_checklist)
                current_checklist = {'title': line.replace('#', '').strip(), 'items': []}
        
        if current_checklist and current_checklist['items']:
            checklists.append(current_checklist)
        
        return checklists if checklists else [{'title': 'General Checklist', 'items': ['Task processed successfully']}]
    
    def _extract_templates(self, text: str) -> list:
        """Extract template structures from text"""
        templates = []
        if any(word in text.lower() for word in ['template', 'format', 'structure']):
            templates.append({
                "type": "data_template",
                "description": "Structured data format",
                "fields": ["field1", "field2", "field3"]
            })
        return templates
    
    def _extract_workflows(self, text: str) -> list:
        """Extract workflow steps from text"""
        workflows = []
        lines = text.split('\n')
        steps = []
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['step', 'phase', 'stage', 'first', 'next', 'then']):
                if len(line.strip()) > 10:
                    steps.append(line.strip())
        
        if steps:
            workflows.append({
                "name": "Automated Workflow",
                "steps": steps[:5],  # Limit to 5 steps for demo
                "step_count": len(steps)
            })
        
        return workflows
    
    def _extract_sections(self, text: str) -> list:
        """Extract sections from structured response"""
        sections = []
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('## ') and len(line) < 100:
                if current_section:
                    sections.append(current_section)
                current_section = {'title': line.replace('##', '').strip(), 'content': []}
            elif current_section is not None and line and not line.startswith('#') and len(line) > 10:
                current_section['content'].append(line)
        
        if current_section:
            sections.append(current_section)
        
        return sections if sections else [{'title': 'Output', 'content': [text[:200] + '...']}]


def create_automation_agent(api_key=None, use_mock=False) -> AutomationAgent:
    """Factory function for automation agent"""
    return AutomationAgent(api_key, use_mock)