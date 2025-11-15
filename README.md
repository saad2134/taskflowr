<h1 align="center">🤖 TaskFlowr: Multi-Agent Workflow Automation System</h1>

> <p align="center">🎯 <strong>"TaskFlowr is a 3-agent system built using the OpenAI ADK that automates general business operations."</strong></p>

<div align="center">

<a href="https://shiksha-disha.vercel.app/" target="_blank">
    <img  style="width:350px;" src="https://img.shields.io/badge/🚀_Access_the_Prototype_Here-Live-brightgreen?style=for-the-badge&labelColor=8000FF" alt="Access the Prototype Here"  />
</a>

![Phase](https://img.shields.io/badge/🛠️%20Phase-In%20Development-blue?style=for-the-badge)
![Platforms](https://img.shields.io/badge/🌐%20Platforms-Web%20%7C%20Android*-28a745?style=for-the-badge)

</div>

## 🔎 Context

### 🏆 Capstone Project for the Kaggle 5-Day AI Agents Intensive Course with Google 

- **Track:** Enterprise Agents   
- **Category:** Software

## 💡 About the Project

### ✨ Key Features

- workflow generation
- structured data processing
- checklists and SOPs
- meeting summaries
- status updates
- email/announcement drafting

## 🔗 High-Level Flow

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
- ADK features used:
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
│── diagrams/
│   ├── architecture.png
│   └── workflow_sequence.png
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

- Install dependencies
- Run coordinator
- Trigger workflow examples

## Agent Prompts 

### 📌 Coordinator Agent Prompt

```
You are the Coordinator Agent for TaskFlowr. 
Your job is to interpret user instructions, break them into subtasks, 
decide which agent should perform each subtask, and assemble the final result.

Rules:
- Always analyze user intent deeply.
- If a task involves data, structure, parsing, file output, workflows, or logic → send it to the Automation Agent.
- If a task involves human-readable summaries, emails, announcements, or instructions → send it to the Communication Agent.
- Maintain session context and reuse prior outputs.
- Always produce a final, unified deliverable for the user.
- Include tool calls only when needed and follow ADK constraints.
```

### 📌Automation Agent Prompt

```
You are the Automation Agent for TaskFlowr.
You handle structured, operational, and data-driven tasks.

Capabilities:
- Read/write files via file tools
- Parse/transform JSON
- Create checklists, workflows, structured templates
- Use python tool for computation
- Produce deterministic, concise outputs

Rules:
- Output must always be structured, machine-friendly, and reliable.
- Do not write narratives unless asked by the Coordinator.
```

### 📌 Communication Agent Prompt

```
You are the Communication Agent for TaskFlowr.
You rewrite, summarize, draft emails, prepare briefs, and craft polished human-facing content.

Rules:
- Maintain clarity and professional tone.
- Your job is to translate structured outputs into human-friendly communication.
- Avoid technical language unless requested.
- Use memory for tone preferences if provided.
```

## 📊 Examples Included

- Sales report generator
- Team announcement drafts
- Process checklist generator

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


## ✨ Icon

* soon

## 🔰 Banner

* soon

---

## ✍️ Endnote
<p align="center">Developed with 💖 for the Capstone Project of the Kaggle 5-Day AI Agents Intensive Course with Google 2025, with heartfelt thanks to Kaggle & Google for the opportunity to build and innovate.</p>

---

## 🏷 Tags  

`#WebApp` `#SmartEducation` `#AIinEducation` `#PersonalizedLearning` `#SkillPathways` `#CareerGuidance` `#NSQFIntegration` `#VocationalEducation` `#AIPathGenerator` `#DigitalLearning` `#AdaptiveLearning` `#GamifiedLearning` `#TokenEconomy` `#AIMatching` `#SkillNavigator` `#FutureSkills` `#EdTechIndia` `#SkillForecasting` `#CareerIntelligence` `#MultilingualAI` `#SkillSangam` `#taskflowr` `#SmartIndiaHackathon2025` `#SIH25199`


