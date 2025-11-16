#!/usr/bin/env python3
"""
Coordinator Agent - Main orchestrator for TaskFlowr multi-agent system
Using Gemini 2.5 Flash (free model)
"""

import os
import json
import asyncio
from datetime import datetime
import random

# Gemini imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Gemini API not available, using mock data")


class CoordinatorAgent:
    """Main coordinator that orchestrates workflow between specialized agents"""
    
    def __init__(self, api_key=None, use_mock=False):
        self.use_mock = use_mock or not GEMINI_AVAILABLE
        
        if not self.use_mock and GEMINI_AVAILABLE:
            try:
                # Configure Gemini with the free 2.5 Flash model
                if api_key:
                    genai.configure(api_key=api_key)
                else:
                    # Try to get from environment
                    api_key = os.getenv('GOOGLE_API_KEY')
                    if api_key:
                        genai.configure(api_key=api_key)
                    else:
                        raise ValueError("No API key provided")
                
                # Test the API key
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                print("✅ Using Gemini 2.0 Flash API")
                self.use_mock = False
            except Exception as e:
                print(f"⚠️  Gemini API setup failed: {e}, using mock data")
                self.use_mock = True
        else:
            self.use_mock = True
            print("🤖 Using mock data for demonstration")
        
        # System prompt for coordinator
        self.system_prompt = self._load_coordinator_prompt()
        
        # Initialize sub-agents
        from .automation_agent import AutomationAgent
        from .communication_agent import CommunicationAgent
        
        self.automation_agent = AutomationAgent(api_key, self.use_mock)
        self.communication_agent = CommunicationAgent(api_key, self.use_mock)
        
        # Session memory
        self.session_memory = {
            "user_preferences": {},
            "workflow_history": [],
            "current_context": {}
        }
    
    def _load_coordinator_prompt(self):
        """Load the coordinator system prompt"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "coordinator_prompt.txt")
            with open(prompt_path, "r", encoding='utf-8') as f:
                return f.read()
        except:
            return """You are the Coordinator Agent for TaskFlowr. Your job is to interpret user instructions, break them into subtasks, and route them to specialized agents.

Rules:
- Analyze user intent and decompose complex tasks
- Route data/automation tasks to Automation Agent
- Route communication/summary tasks to Communication Agent  
- Maintain session context
- Assemble final deliverables

Always provide structured, actionable outputs."""
    
    async def process_user_request(self, user_input: str, context: dict = None):
        """
        Main entry point for processing user requests
        """
        print(f"🔄 Coordinator received request: {user_input}")
        
        # Update session context
        if context:
            self.session_memory["current_context"].update(context)
        
        # Analyze intent and decompose task
        task_analysis = await self._analyze_intent(user_input)
        
        # Route to appropriate agents
        results = await self._route_to_agents(task_analysis, user_input)
        
        # Assemble final output
        final_output = await self._assemble_final_output(results, user_input)
        
        # Log workflow
        self._log_workflow(user_input, task_analysis, results)
        
        return final_output
    
    async def _analyze_intent(self, user_input: str) -> dict:
        """Analyze user intent and decompose tasks using Gemini 2.5 Flash"""
        if self.use_mock:
            return self._mock_analyze_intent(user_input)
        
        try:
            # Use Gemini 2.5 Flash for analysis
            prompt = f"""
            SYSTEM: {self.system_prompt}
            
            USER REQUEST: {user_input}
            
            Analyze this request and determine the best way to handle it using our multi-agent system.
            
            Return ONLY a JSON object with:
            - intent_category (data_processing, communication, workflow, hybrid)
            - needs_automation (true/false) 
            - needs_communication (true/false)
            - primary_agent (automation/communication/both)
            
            JSON:
            """
            
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
                
            analysis = json.loads(response_text)
            return analysis
            
        except Exception as e:
            print(f"Gemini analysis error: {e}, using mock analysis")
            return self._mock_analyze_intent(user_input)
    
    def _mock_analyze_intent(self, user_input: str) -> dict:
        """Mock intent analysis for demonstration"""
        user_lower = user_input.lower()
        
        # Simple rule-based analysis
        automation_keywords = ['data', 'report', 'checklist', 'process', 'workflow', 'template', 'metrics', 'analysis']
        communication_keywords = ['email', 'summary', 'announcement', 'draft', 'communicate', 'briefing', 'welcome']
        
        needs_auto = any(word in user_lower for word in automation_keywords)
        needs_comm = any(word in user_lower for word in communication_keywords)
        
        return {
            "intent_category": "hybrid" if needs_auto and needs_comm else "automation" if needs_auto else "communication",
            "needs_automation": needs_auto,
            "needs_communication": needs_comm,
            "primary_agent": "both" if needs_auto and needs_comm else "automation" if needs_auto else "communication"
        }
    
    async def _route_to_agents(self, task_analysis: dict, user_input: str) -> dict:
        """Route subtasks to appropriate agents"""
        results = {}
        
        if task_analysis.get("needs_automation", False):
            print("🔄 Routing to Automation Agent...")
            results["automation"] = await self.automation_agent.process_automation_task(
                user_input, self.session_memory
            )
        
        if task_analysis.get("needs_communication", False):
            print("🔄 Routing to Communication Agent...")
            results["communication"] = await self.communication_agent.process_communication_task(
                user_input, self.session_memory
            )
        
        return results
    
    async def _assemble_final_output(self, agent_results: dict, original_request: str) -> dict:
        """Assemble final output from agent results using Gemini 2.5 Flash"""
        if self.use_mock:
            final_text = self._create_detailed_final_output(agent_results, original_request)
        else:
            try:
                # Use Gemini 2.5 Flash to create a professional final output
                assembly_prompt = f"""
                Create a professional business deliverable that combines these agent outputs:
                
                ORIGINAL REQUEST: {original_request}
                
                AUTOMATION AGENT OUTPUTS: {json.dumps(agent_results.get('automation', {}), indent=2)}
                COMMUNICATION AGENT OUTPUTS: {json.dumps(agent_results.get('communication', {}), indent=2)}
                
                Structure the response as a business report with:
                - Executive Summary
                - Key Findings/Outputs  
                - Actionable Recommendations
                - Next Steps
                
                Keep it professional and concise.
                """
                
                response = self.model.generate_content(assembly_prompt)
                final_text = response.text
                
            except Exception as e:
                print(f"Gemini final assembly error: {e}, using detailed output")
                final_text = self._create_detailed_final_output(agent_results, original_request)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "original_request": original_request,
            "final_output": final_text,
            "component_results": agent_results,
            "status": "completed"
        }
    
    def _create_detailed_final_output(self, agent_results: dict, original_request: str) -> str:
        """Create detailed final output using actual agent results"""
        output_parts = []
        output_parts.append(f"# 🚀 TaskFlowr Multi-Agent Deliverable\n")
        output_parts.append(f"**Request:** {original_request}")
        output_parts.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        output_parts.append(f"**Model:** Gemini 2.0 Flash")
        output_parts.append("")
        
        output_parts.append("## 📊 Executive Summary")
        agents_used = list(agent_results.keys())
        if agents_used:
            output_parts.append(f"TaskFlowr successfully processed your request using {', '.join(agents_used)} specialized agents.")
            output_parts.append("Below you'll find the structured outputs and communication drafts generated by our AI agents.")
        output_parts.append("")
        
        # Show Automation Agent results in detail
        if 'automation' in agent_results:
            auto_data = agent_results['automation']
            output_parts.append("## 🛠️ Automation Agent Outputs")
            output_parts.append("*Specialized in structured data, workflows, and operational tasks*")
            output_parts.append("")
            
            if 'raw_response' in auto_data:
                # Show the actual Gemini-generated content
                output_parts.append("### Generated Content")
                output_parts.append(auto_data['raw_response'])
                output_parts.append("")
            
            if 'structured_outputs' in auto_data:
                outputs = auto_data['structured_outputs']
                
                if outputs.get('checklists'):
                    output_parts.append("### 📋 Checklists Generated")
                    for i, checklist in enumerate(outputs['checklists'][:3], 1):
                        output_parts.append(f"**Checklist {i}: {checklist.get('title', 'Task Checklist')}**")
                        for item in checklist.get('items', [])[:8]:
                            output_parts.append(f"• {item}")
                        output_parts.append("")
        
        # Show Communication Agent results in detail
        if 'communication' in agent_results:
            comm_data = agent_results['communication']
            output_parts.append("## 💬 Communication Agent Outputs")
            output_parts.append(f"*Tone: {comm_data.get('tone_used', 'professional').title()}*")
            output_parts.append("")
            
            if 'raw_response' in comm_data:
                output_parts.append("### Generated Communications")
                output_parts.append(comm_data['raw_response'])
                output_parts.append("")
        
        output_parts.append("## 🎯 Capstone Project Features Demonstrated")
        output_parts.append("✅ **Multi-Agent Architecture** - Coordinator + Specialized Agents")
        output_parts.append("✅ **A2A Communication** - Agent-to-Agent task routing")
        output_parts.append("✅ **Gemini 2.0 Flash Integration** - Free, powerful model")
        output_parts.append("✅ **Structured Outputs** - Checklists, workflows, templates")
        output_parts.append("✅ **Business Communication** - Professional emails, summaries")
        output_parts.append("✅ **Session Memory** - Context-aware processing")
        output_parts.append("")
        
        output_parts.append("---")
        output_parts.append("*Generated by TaskFlowr - Capstone Project for Kaggle 5-Day AI Agents Intensive*")
        
        return '\n'.join(output_parts)
    
    def _log_workflow(self, user_input: str, analysis: dict, results: dict):
        """Log workflow for observability"""
        workflow_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "analysis": analysis,
            "results_keys": list(results.keys()),
            "status": "completed"
        }
        self.session_memory["workflow_history"].append(workflow_entry)


def create_coordinator(api_key=None, use_mock=False):
    """Create coordinator instance"""
    return CoordinatorAgent(api_key, use_mock)


# Main execution with proper imports
if __name__ == "__main__":
    async def main():
        """Main function with proper error handling"""
        import getpass
        
        # Check if we should use real Gemini
        use_mock = os.getenv('USE_MOCK', 'false').lower() == 'true'
        api_key = None
        
        if not use_mock:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                try:
                    api_key = getpass.getpass("🔑 Enter your Google AI Studio API key (press Enter for mock mode): ")
                    if not api_key:
                        use_mock = True
                        print("🤖 Using mock data mode")
                except:
                    use_mock = True
                    print("🤖 Using mock data mode")
        
        coordinator = create_coordinator(api_key, use_mock)
        
        # Test requests
        test_requests = [
            "Create a sales report for Q4 and email summary to team",
            "Generate onboarding checklist for new engineers and draft welcome email", 
            "Analyze monthly metrics and prepare executive briefing"
        ]
        
        for i, request in enumerate(test_requests, 1):
            print(f"\n{'='*50}")
            print(f"🎯 Test {i}: {request}")
            print(f"{'='*50}")
            
            result = await coordinator.process_user_request(request)
            print(f"✅ Status: {result['status']}")
            print(f"🤖 Components: {list(result['component_results'].keys())}")
            
            # Show preview of final output
            preview = result['final_output'][:300] + "..." if len(result['final_output']) > 300 else result['final_output']
            print(f"\n📄 Output Preview:\n{preview}")
            
            print(f"\n{'='*50}")

    asyncio.run(main())