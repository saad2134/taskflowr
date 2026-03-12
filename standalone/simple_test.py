#!/usr/bin/env python3
"""
Simple test without complex imports
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

async def simple_test():
    """Simple test that definitely works"""
    try:
        # Import the coordinator directly
        from agent.coordinator import create_coordinator
        
        print("🧪 Simple TaskFlowr Test")
        print("=" * 40)
        
        # Create coordinator with mock data
        coordinator = create_coordinator(use_mock=True)
        
        # Test a simple request
        test_request = "Create a daily standup meeting checklist"
        print(f"📝 Testing: {test_request}")
        
        result = await coordinator.process_user_request(test_request)
        
        print(f"✅ Success! Status: {result['status']}")
        print(f"🤖 Agents used: {list(result['component_results'].keys())}")
        
        # Show what was generated
        if 'automation' in result['component_results']:
            auto_data = result['component_results']['automation']
            if 'structured_outputs' in auto_data:
                checklists = auto_data['structured_outputs'].get('checklists', [])
                if checklists:
                    print(f"📋 Generated {len(checklists)} checklists")
                    print("Sample items:")
                    for item in checklists[0].get('items', [])[:3]:
                        print(f"  • {item}")
        
        print("\n🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you're in the taskflowr root directory")

if __name__ == "__main__":
    asyncio.run(simple_test())