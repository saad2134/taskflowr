# Example 1: Sales Report Generation

## 🎯 User Input
```
Create a comprehensive sales report for Q4 2024 including:
- Monthly sales figures
- Top performing products  
- Regional performance analysis
- Growth metrics compared to Q3
- Executive summary for leadership
- Email draft to sales team with key findings
```

## 🔄 Agent Workflow

### Coordinator Analysis
**Intent:** Hybrid (data processing + communication)
**Subtasks:**
1. Process sales data and generate structured report → Automation Agent
2. Create executive summary and team email → Communication Agent

### Automation Agent Outputs
```json
{
  "structured_outputs": {
    "checklists": [
      {
        "title": "Sales Report Generation Checklist",
        "items": [
          "Collect monthly sales data",
          "Calculate growth metrics", 
          "Identify top products",
          "Analyze regional performance",
          "Generate comparison with Q3"
        ]
      }
    ],
    "templates": [
      {
        "type": "sales_report",
        "fields": ["month", "revenue", "growth", "top_products", "regions"],
        "format": "JSON"
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
        "subject": "Q4 2024 Sales Performance Update",
        "greeting": "Dear Sales Team,",
        "body": "I'm pleased to share our Q4 2024 sales performance results...",
        "closing": "Best regards,\nSales Leadership"
      }
    ],
    "summaries": [
      {
        "type": "executive_summary",
        "key_points": [
          "Q4 revenue increased 15% over Q3",
          "Product X emerged as top performer",
          "European region showed strongest growth",
          "Recommend continued focus on high-margin products"
        ]
      }
    ]
  }
}
```

### Final Deliverable
**Status:** ✅ Completed
**Components Integrated:**
- Structured sales data report
- Executive summary with key takeaways
- Team communication email
- Actionable insights and recommendations

## 📊 Key Features Demonstrated

- ✅ Multi-agent coordination
- ✅ Structured data processing  
- ✅ Business communication
- ✅ Workflow automation
- ✅ Enterprise-ready outputs






