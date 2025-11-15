<h1 align="center">🤖 TaskFlowr: Multi-Agent Workflow Automation System</h1>

> <p align="center">🎯 <strong>"TaskFlowr is a 3-agent system built using the OpenAI ADK that automates general business operations."</strong></p>

<div align="center">

<a href="https://www.kaggle.com/code/saad2134/taskflowr-multi-agent-workflow-automation-system" target="_blank">
    <img style="width:350px;" 
         src="https://img.shields.io/badge/🚀_Access_the_Kaggle_Notebook-Link-brightgreen?style=for-the-badge&labelColor=20BEFF" 
         alt="Access the Kaggle Notebook" />
</a>

</div>

## 🔎 Context

### 🏆 Capstone Project for the Kaggle 5-Day AI Agents Intensive Course with Google 

- **Track:** Enterprise Agents   
- **Category:** Software


## 🎯 Execution Instructions for Judges

### Primary Evaluation Method: Kaggle Notebook

**Judges should start here:** 
1. Go to the Kaggle Notebook: `notebooks/taskflowr_kaggle_notebook.ipynb`
2. The notebook contains complete, runnable demonstrations
3. All dependencies are pre-configured for Kaggle environment
4. Shows live agent interactions and outputs

### Key Things Judges Will See:

1. **Multi-agent coordination in action**
2. **Structured business outputs** (checklists, reports, emails)
3. **ADK features demonstrated** (tools, memory, A2A communication)
4. **Enterprise-ready workflows**
5. **Comprehensive evaluation results**

### Running Locally (Alternative):

```bash
# Quick start
git clone https://github.com/saad2134/taskflowr
cd taskflowr
pip install -r requirements.txt
export GOOGLE_API_KEY=your_key_here
python -m agent.coordinator
```

## 💡 About the Project

### ✨ Key Features

- workflow generation
- structured data processing
- checklists and SOPs
- meeting summaries
- status updates
- email/announcement drafting

### 🔗 High-Level Flow

1. User sends an instruction
2. Coordinator interprets and decomposes
3. Automation Agent handles structured ops
4. Communication Agent prepares human-facing output
5. Coordinator compiles & returns final deliverable
6. Logs + observability captured

## 🧠 Architecture

TaskFlowr uses:

- **Coordinator Agent** – orchestrates workflows
- **Automation Agent** – structured operations
- **Communication Agent** – summarization + messaging

### 🧠 1. Coordinator Agent (Orchestrator)

Role: Central brain. Routes tasks, manages sessions, merges outputs.

Key responsibilities:
- Interpret user intent
- Decompose tasks
- Decide which sub-agent handles which part
- Merge/assemble final results
- Maintain session memory
- Trigger evaluation hooks

ADK features used:
- Prompt-to-action logic
- Memory
- Observability
- A2A for routing

### ⚙️ 2. Automation Agent (Operations Engine)

Role: Performs structured and technical tasks.

Responsibilities:
- Data extraction, transformation
- Running JSON workflows
- Generating checklists, SOPs, structured outputs
- Writing files (reports, logs)
- Using Python tool for small computations
- Using file, shell, and JSON tools

ADK features used:
- Agent tools
- File read/write
- JSON transformations
- Python tool (safe)
- Sessions

### 🗣️ 3. Communication Agent (Messaging & Summaries)

Role: Handles all natural-language outputs.

Responsibilities:
- Drafting emails
- Summaries and briefs
- Meeting notes
- Tone adjustments
- Creating announcements, instructions, SOP narratives

ADK features used:
- Memory for tone preference
- Text refinement
- A2A communication with Coordinator

## ✨ ADK Features Demonstrated

- Tools (file, JSON, python)
- Multi-agent A2A communication
- Sessions
- Memory
- Observability & evaluation
- Deployment with Agent Engine

## 📦 Folder Structure

```
taskflowr/
│── agent/
│   ├── coordinator.py
│   ├── automation_agent.py
│   ├── communication_agent.py
│   └── prompts/
│       ├── coordinator_prompt.txt
│       ├── automation_prompt.txt
│       └── communication_prompt.txt
│
│── mcp_tools/
│   ├── file_tools.json
│   ├── json_tools.json
│   └── python_tools.json
│
│── notebooks/
│   └── taskflowr_kaggle_notebook.ipynb
│
│── evaluation/
│   ├── test_cases.json
│   ├── evaluator.py
│   └── expected_outputs/
│
│── deployment/
│   ├── Dockerfile
│   ├── agent_engine_config.json
│   ├── start.sh
│   └── README_DEPLOY.md
│
│── examples/
│   ├── example_1_sales_report.md
│   ├── example_2_team_announcement.md
│   └── example_3_ops_checklist.md
│
│── README.md
│── requirements.txt
└── LICENSE

```

## 🚀 Quick Start

### Prerequisites

```
# Clone the repository
git clone https://github.com/saad2134/taskflowr
cd taskflowr

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_API_KEY=your_gemini_api_key_here
```

### Running the System

```
# Method 1: Run the main coordinator
python -m agent.coordinator

# Method 2: Run via Kaggle notebook (primary method)
# Open notebooks/taskflowr_kaggle_notebook.ipynb on Kaggle

# Method 3: Deploy to Vertex AI Agent Engine
cd deployment
./start.sh
```

### Detail Deployment Guide
- See [deployment/](deployment/)'s README for detail guide on running, troubleshooting & deploying the project.

## 📊 Examples Included

- Sales report generator [examples/example_1_sales_report.md](examples/example_1_sales_report.md)
- Team announcement drafts [examples/example_2_team_announcement.md](examples/example_2_team_announcement.md) 
- Process checklist generator [examples/example_3_ops_checklist.md](examples/example_3_ops_checklist.md)  

## 📊 **Repo Stats**

<div align="center">
  
![Repo Size](https://img.shields.io/github/repo-size/saad2134/taskflowr)
![Last Commit](https://img.shields.io/github/last-commit/saad2134/taskflowr)
![Open Issues](https://img.shields.io/github/issues/saad2134/taskflowr)
![Open PRs](https://img.shields.io/github/issues-pr/saad2134/taskflowr)
![License](https://img.shields.io/github/license/saad2134/taskflowr)
![Forks](https://img.shields.io/github/forks/saad2134/taskflowr?style=social)
![Stars](https://img.shields.io/github/stars/saad2134/taskflowr?style=social)
![Watchers](https://img.shields.io/github/watchers/saad2134/taskflowr?style=social)
![Contributors](https://img.shields.io/github/contributors/saad2134/taskflowr)
![Languages](https://img.shields.io/github/languages/count/saad2134/taskflowr)
![Top Language](https://img.shields.io/github/languages/top/saad2134/taskflowr)

</div>

## ⭐ Star History

<a href="https://www.star-history.com/#saad2134/taskflowr&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=saad2134/taskflowr&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=saad2134/taskflowr&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=saad2134/taskflowr&type=Date" />
 </picture>
</a>

## 🔰 Cover Image

![thumbnail](https://github.com/user-attachments/assets/c152f34c-aca3-435e-a1de-282a120bb8a6)

---

## ✍️ Endnote
<p align="center">Developed with 💖 for the Capstone Project of the Kaggle 5-Day AI Agents Intensive Course with Google 2025, with heartfelt thanks to Kaggle & Google for the opportunity to build and innovate.</p>

---

## 🏷 Tags  

`#TaskFlowr` `#AIWorkflows` `#AutomationAgent` `#MultiAgentSystems` `#ProductivityTools` `#AgentOrchestration` `#WorkflowAutomation` `#AIAgents` `#SmartOps` `#TaskCoordination` `#AgenticFramework` `#PythonAutomation` `#DeveloperTools` `#OpenSourceAI` `#AIEngineering` `#MCPTools` `#SystemDesign` `#KaggleNotebook` `#EnterpriseAI` 

