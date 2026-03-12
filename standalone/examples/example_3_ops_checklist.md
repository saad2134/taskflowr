# Example 3: Operations Checklist Generation

## 🎯 User Input
```
Generate weekly operations checklist for customer support team:
- Daily monitoring tasks
- Weekly reporting requirements  
- Quality assurance checks
- Team coordination meetings
- Performance metrics review
Also draft team announcement about new process.
```

## 🔄 Agent Workflow

### Coordinator Analysis
**Intent:** Hybrid (automation + communication)
**Subtasks:**
1. Create operational checklists and procedures → Automation Agent
2. Draft team announcement → Communication Agent

### Automation Agent Outputs
```json
{
  "structured_outputs": {
    "checklists": [
      {
        "title": "Daily Monitoring Tasks",
        "items": [
          "Review system alerts and incidents",
          "Monitor response time metrics", 
          "Check ticket backlog status",
          "Review customer satisfaction scores"
        ]
      },
      {
        "title": "Weekly Reporting Checklist", 
        "items": [
          "Compile weekly performance metrics",
          "Generate team productivity report",
          "Prepare quality assurance summary",
          "Document improvement opportunities"
        ]
      }
    ],
    "workflows": [
      {
        "name": "Weekly Operations Process",
        "steps": ["Daily monitoring", "Mid-week check-in", "Weekly reporting", "Team meeting", "Process improvement"],
        "dependencies": {"data_collection": "before reporting"}
      }
    ]
  }
}
```

### Communication Agent Outputs
```json
{
  "communication_outputs": {
    "announcements": [
      {
        "type": "team_announcement", 
        "key_message": "New weekly operations process implementation",
        "action_items": [
          "Review new checklists and procedures",
          "Attend training session on Thursday",
          "Provide feedback by end of week"
        ]
      }
    ],
    "emails": [
      {
        "subject": "New Weekly Operations Process",
        "body": "Team, we're implementing a new weekly operations process to improve efficiency...",
        "tone": "friendly"
      }
    ]
  }
}
```

### Final Deliverable
**Status:** ✅ Completed
**Components:**
- Comprehensive operations checklists
- Weekly workflow procedures  
- Team announcement draft
- Implementation guidance
- Success metrics tracking

## 📈 Business Value

- ✅ Standardized operations
- ✅ Clear accountability
- ✅ Improved efficiency
- ✅ Team alignment
- ✅ Continuous improvement framework