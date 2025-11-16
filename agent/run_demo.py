#!/usr/bin/env python3
"""
TaskFlowr Demo Runner - Clean version without async errors
"""

import asyncio
import os
import sys

# Add the agent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

async def run_demo():
    """Run TaskFlowr demo without async cleanup issues"""
    from coordinator import create_coordinator
    
    print("🚀 TaskFlowr Multi-Agent System Demo")
    print("=" * 50)
    
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
        print("=" * 50)
        print(f"📝 Request: {demo['request']}")
        print("-" * 50)
        
        result = await coordinator.process_user_request(demo['request'])
        
        print(f"✅ Status: {result['status']}")
        print(f"🤖 Agents Used: {list(result['component_results'].keys())}")
        print(f"\n📊 FINAL OUTPUT:")
        print("=" * 50)
        print(result['final_output'])
        print("=" * 50)
        
        # Show some raw data from agents
        if 'automation' in result['component_results']:
            auto_data = result['component_results']['automation']
            if 'structured_outputs' in auto_data:
                outputs = auto_data['structured_outputs']
                print(f"\n📋 Automation Generated: {len(outputs.get('checklists', []))} checklists, {len(outputs.get('workflows', []))} workflows")
        
        if 'communication' in result['component_results']:
            comm_data = result['component_results']['communication']
            if 'communication_outputs' in comm_data:
                outputs = comm_data['communication_outputs']
                print(f"📧 Communication Generated: {len(outputs.get('emails', []))} emails, {len(outputs.get('summaries', []))} summaries")
        
        print("\n" + "=" * 50)

def main():
    """Main entry point without async cleanup issues"""
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n\n👋 Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("\n✨ TaskFlowr demo completed!")

if __name__ == "__main__":
    main()