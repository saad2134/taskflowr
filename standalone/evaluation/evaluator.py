#!/usr/bin/env python3
"""
Evaluation system for TaskFlowr - Based on Day 4B codelab
"""

import json
import asyncio
from typing import Dict, List, Any
from agent.coordinator import create_coordinator


class TaskFlowrEvaluator:
    """Evaluates TaskFlowr system against test cases"""
    
    def __init__(self):
        self.coordinator = create_coordinator()
        self.test_cases = self._load_test_cases()
        
    def _load_test_cases(self) -> List[Dict]:
        """Load evaluation test cases"""
        try:
            with open('evaluation/test_cases.json', 'r') as f:
                return json.load(f)
        except:
            return self._get_default_test_cases()
    
    def _get_default_test_cases(self) -> List[Dict]:
        """Default test cases for evaluation"""
        return [
            {
                "id": "TC001",
                "name": "Sales Report Generation",
                "input": "Create Q4 sales report with monthly figures, top products, regional analysis, and executive summary",
                "expected_outputs": ["checklist", "summary", "structured_data"],
                "category": "data_processing"
            },
            {
                "id": "TC002", 
                "name": "Team Communication",
                "input": "Draft team announcement about new process and create onboarding checklist for new members",
                "expected_outputs": ["email", "announcement", "checklist"],
                "category": "communication"
            },
            {
                "id": "TC003",
                "name": "Workflow Automation", 
                "input": "Generate weekly operations checklist with monitoring tasks, reporting, and quality checks",
                "expected_outputs": ["workflow", "checklist", "procedures"],
                "category": "automation"
            }
        ]
    
    async def evaluate_system(self) -> Dict[str, Any]:
        """Run comprehensive system evaluation"""
        print("🧪 Starting TaskFlowr Evaluation...")
        
        results = {
            "total_tests": len(self.test_cases),
            "passed_tests": 0,
            "failed_tests": 0,
            "test_results": [],
            "average_response_time": 0,
            "success_rate": 0
        }
        
        total_time = 0
        
        for test_case in self.test_cases:
            print(f"\n🔬 Running Test: {test_case['name']}")
            
            start_time = asyncio.get_event_loop().time()
            test_result = await self._run_single_test(test_case)
            end_time = asyncio.get_event_loop().time()
            
            response_time = end_time - start_time
            total_time += response_time
            
            test_result["response_time"] = response_time
            results["test_results"].append(test_result)
            
            if test_result["status"] == "passed":
                results["passed_tests"] += 1
                print(f"✅ PASSED - {response_time:.2f}s")
            else:
                results["failed_tests"] += 1
                print(f"❌ FAILED - {response_time:.2f}s")
        
        # Calculate metrics
        results["average_response_time"] = total_time / len(self.test_cases)
        results["success_rate"] = (results["passed_tests"] / results["total_tests"]) * 100
        
        print(f"\n📊 EVALUATION SUMMARY:")
        print(f"Tests Passed: {results['passed_tests']}/{results['total_tests']}")
        print(f"Success Rate: {results['success_rate']:.1f}%")
        print(f"Average Response Time: {results['average_response_time']:.2f}s")
        
        return results
    
    async def _run_single_test(self, test_case: Dict) -> Dict:
        """Run a single test case"""
        try:
            # Process the test input
            result = await self.coordinator.process_user_request(test_case["input"])
            
            # Evaluate the result
            evaluation = self._evaluate_result(result, test_case)
            
            return {
                "test_id": test_case["id"],
                "test_name": test_case["name"],
                "status": "passed" if evaluation["all_expected_found"] else "failed",
                "input": test_case["input"],
                "output_preview": result["final_output"][:200] + "..." if len(result["final_output"]) > 200 else result["final_output"],
                "evaluation_details": evaluation,
                "component_results": list(result.get("component_results", {}).keys())
            }
            
        except Exception as e:
            return {
                "test_id": test_case["id"],
                "test_name": test_case["name"], 
                "status": "error",
                "error": str(e),
                "input": test_case["input"]
            }
    
    def _evaluate_result(self, result: Dict, test_case: Dict) -> Dict:
        """Evaluate if result contains expected outputs"""
        evaluation = {
            "expected_outputs": test_case["expected_outputs"],
            "found_outputs": [],
            "all_expected_found": False
        }
        
        final_output = result["final_output"].lower()
        component_results = result.get("component_results", {})
        
        # Check for expected output types in final output
        for expected in test_case["expected_outputs"]:
            if self._check_output_type(final_output, expected):
                evaluation["found_outputs"].append(expected)
        
        # Check component results
        if "automation" in component_results:
            auto_outputs = component_results["automation"].get("structured_outputs", {})
            if auto_outputs.get("checklists"):
                if "checklist" not in evaluation["found_outputs"]:
                    evaluation["found_outputs"].append("checklist")
        
        if "communication" in component_results:
            comm_outputs = component_results["communication"].get("communication_outputs", {})
            if comm_outputs.get("emails"):
                if "email" not in evaluation["found_outputs"]:
                    evaluation["found_outputs"].append("email")
        
        # Determine if all expected outputs were found
        evaluation["all_expected_found"] = all(
            expected in evaluation["found_outputs"] 
            for expected in test_case["expected_outputs"]
        )
        
        return evaluation
    
    def _check_output_type(self, text: str, output_type: str) -> bool:
        """Check if text contains evidence of specific output type"""
        patterns = {
            "checklist": ["checklist", "steps", "tasks", "todo", "items"],
            "summary": ["summary", "key takeaways", "executive", "overview"],
            "email": ["dear", "subject:", "regards", "sincerely"],
            "announcement": ["announce", "update", "team", "news"],
            "structured_data": ["json", "table", "data", "figures"],
            "workflow": ["workflow", "process", "steps", "flow"],
            "procedures": ["procedure", "guideline", "instruction", "how to"]
        }
        
        if output_type in patterns:
            return any(pattern in text for pattern in patterns[output_type])
        
        return False


async def main():
    """Run evaluation"""
    evaluator = TaskFlowrEvaluator()
    results = await evaluator.evaluate_system()
    
    # Save results
    with open('evaluation/evaluation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Evaluation results saved to evaluation_results.json")

if __name__ == "__main__":
    asyncio.run(main())