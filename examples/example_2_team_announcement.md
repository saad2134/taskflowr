# Example 2: Team Announcement & Onboarding

## 🎯 User Input
```
Create an onboarding workflow for new software engineers including:
- 30-60-90 day checklist
- Technical setup procedures  
- Team introduction email template
- Learning path for first month
- Manager guidance document
```

## 🔄 Agent Workflow

### Coordinator Analysis
**Intent:** Automation-focused with communication elements
**Subtasks:**
1. Generate structured checklists and procedures → Automation Agent
2. Create communication templates → Communication Agent

### Automation Agent Outputs
```json
{
  "structured_outputs": {
    "checklists": [
      {
        "title": "30-60-90 Day Onboarding Plan",
        "items": [
          "Week 1: Environment setup and team introductions",
          "Days 1-30: Foundation building and initial projects", 
          "Days 31-60: Feature development and collaboration",
          "Days 61-90: Ownership and leadership opportunities"
        ]
      },
      {
        "title": "Technical Setup Checklist",
        "items": [
          "Install development environment",
          "Configure access to repositories",
          "Set up development tools",
          "Complete security training"
        ]
      }
    ],
    "workflows": [
      {
        "name": "New Engineer Onboarding",
        "steps": ["Pre-start preparation", "First week orientation", "First month ramp-up", "First quarter integration"],
        "dependencies": {"technical_setup": "before project_assignment"}
      }
    ]
  }
}
```

### Communication Agent Outputs  
```json
{
  "communication_outputs": {
    "emails": [
      {
        "subject": "Welcome to the Engineering Team!",
        "greeting": "Dear [New Engineer],",
        "body": "We're excited to have you join our engineering team...",
        "closing": "Looking forward to working with you!"
      }
    ],
    "other_content": [
      {
        "type": "manager_guidance",
        "content": "Guidance for managers onboarding new engineers...",
        "tone": "professional"
      }
    ]
  }
}
```

### Final Deliverable
**Status:** ✅ Completed  
**Output Includes:**
- Comprehensive onboarding timeline
- Technical setup procedures
- Welcome communication templates
- Manager guidance document
- Structured learning path

## 🛠️ ADK Features Used

- ✅ Tool integration for structured outputs
- ✅ Session memory for consistent tone
- ✅ Multi-agent task routing
- ✅ Enterprise workflow automation