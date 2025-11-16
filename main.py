#!/usr/bin/env python3
"""
TaskFlowr Main Demo Runner
Fixed import structure
"""

import asyncio
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

async def run_demo():
    """Run TaskFlowr demo with fixed imports"""
    try:
        # Import directly from the agent module
        from agent.coordinator import create_coordinator
        
        print("🚀 TaskFlowr Multi-Agent System Demo")
        print("=" * 60)
        
        # Use mock mode to avoid API issues
        coordinator = create_coordinator(use_mock=True)
        
        demo_requests = [
            {
                "title": "Sales Report & Team Communication", 
                "request": "Create a sales report for Q4 2024 including monthly figures, top products, regional analysis, and email summary to sales team"
            },
            {
                "title": "Employee Onboarding Package",
                "request": "Generate onboarding checklist for new software engineers with 30-60-90 day plan, technical setup procedures, and welcome email template"
            },
            {
                "title": "Executive Metrics Briefing", 
                "request": "Analyze monthly performance metrics and prepare executive briefing with key takeaways and recommendations"
            }
        ]
        
        for i, demo in enumerate(demo_requests, 1):
            print(f"\n🎯 Demo {i}: {demo['title']}")
            print("=" * 60)
            print(f"📝 Request: {demo['request']}")
            print("-" * 60)
            
            result = await coordinator.process_user_request(demo['request'])
            
            print(f"✅ Status: {result['status']}")
            print(f"🤖 Agents Used: {list(result['component_results'].keys())}")
            
            # Show detailed outputs
            if 'automation' in result['component_results']:
                auto_data = result['component_results']['automation']
                if 'structured_outputs' in auto_data:
                    outputs = auto_data['structured_outputs']
                    checklists = outputs.get('checklists', [])
                    workflows = outputs.get('workflows', [])
                    print(f"📋 Automation Generated: {len(checklists)} checklists, {len(workflows)} workflows")
                    
                    # Show first checklist items
                    if checklists:
                        print(f"\n🔧 Sample Checklist: {checklists[0].get('title', 'Checklist')}")
                        for item in checklists[0].get('items', [])[:3]:
                            print(f"   • {item}")
            
            if 'communication' in result['component_results']:
                comm_data = result['component_results']['communication']
                if 'communication_outputs' in comm_data:
                    outputs = comm_data['communication_outputs']
                    emails = outputs.get('emails', [])
                    summaries = outputs.get('summaries', [])
                    print(f"📧 Communication Generated: {len(emails)} emails, {len(summaries)} summaries")
                    
                    # Show email preview
                    if emails:
                        print(f"\n✉️  Sample Email Subject: {emails[0].get('subject', 'No subject')}")
                        if emails[0].get('body'):
                            preview = emails[0]['body'][:100] + "..." if len(emails[0]['body']) > 100 else emails[0]['body']
                            print(f"   Preview: {preview}")
            
            print(f"\n📄 Final Output Preview:")
            print("-" * 40)
            # Show first 300 chars of final output
            preview = result['final_output'][:300] + "..." if len(result['final_output']) > 300 else result['final_output']
            print(preview)
            print("=" * 60)
            
            # Add a pause between demos
            if i < len(demo_requests):
                input("\nPress Enter to continue to next demo...")
                print()
    
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're running from the taskflowr root directory")
        print("💡 Directory structure should be: taskflowr/agent/coordinator.py")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main entry point"""
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped by user")
    finally:
        print("\n✨ TaskFlowr demo completed!")

if __name__ == "__main__":
    main()