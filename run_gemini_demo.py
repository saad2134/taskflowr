#!/usr/bin/env python3
"""
TaskFlowr with Gemini 2.5 Flash Demo
"""

import asyncio
import os
import sys
import getpass

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

async def run_gemini_demo():
    """Run demo with real Gemini 2.5 Flash"""
    try:
        from agent.coordinator import create_coordinator
        
        print("🚀 TaskFlowr with Gemini 2.5 Flash")
        print("=" * 50)
        
        # Get API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            api_key = getpass.getpass("🔑 Enter your Google AI Studio API key: ")
        
        if not api_key:
            print("❌ No API key provided. Using mock mode.")
            use_mock = True
        else:
            use_mock = False
        
        coordinator = create_coordinator(api_key, use_mock)
        
        print(f"\n🤖 Mode: {'Gemini 2.5 Flash' if not use_mock else 'Mock Data'}")
        print("=" * 50)
        
        # Demo requests
        demos = [
            "Create a comprehensive Q4 sales report with regional analysis and executive summary",
            "Generate a 30-60-90 day onboarding plan for new engineers with welcome email template",
            "Prepare weekly operations checklist for customer support team with performance metrics"
        ]
        
        for i, demo in enumerate(demos, 1):
            print(f"\n🎯 Demo {i}: {demo}")
            print("-" * 50)
            
            result = await coordinator.process_user_request(demo)
            
            print(f"✅ Status: {result['status']}")
            print(f"🤖 Agents: {list(result['component_results'].keys())}")
            
            # Show actual outputs
            if 'automation' in result['component_results']:
                auto_data = result['component_results']['automation']
                if 'structured_outputs' in auto_data:
                    outputs = auto_data['structured_outputs']
                    print(f"📋 Checklists: {len(outputs.get('checklists', []))}")
                    print(f"🔄 Workflows: {len(outputs.get('workflows', []))}")
            
            print(f"\n📄 Final Output Preview:")
            print(result['final_output'][:500] + "..." if len(result['final_output']) > 500 else result['final_output'])
            print("=" * 50)
            
            if i < len(demos):
                input("\nPress Enter for next demo...")
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have google-generativeai installed: pip install google-generativeai")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_gemini_demo())