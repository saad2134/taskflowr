# TaskFlowr - Full-Stack Implementation Guide

## Overview

TaskFlowr is a multi-agent workflow automation system built with Google's ADK. This document describes the complete full-stack implementation with REST API, React frontend, and external connectors.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                       │
│  ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────────┐        │
│  │Dashboard │ │ Tasks   │ │ Workflows │ │ Connectors │        │
│  └─────────┘ └─────────┘ └──────────┘ └────────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API (JWT Auth)
┌────────────────────────────┴────────────────────────────────────┐
│                      Backend (FastAPI)                           │
│  ┌──────────┐ ┌─────────┐ ┌───────────┐ ┌─────────────────┐    │
│  │ Auth API │ │Tasks API│ │Workflow API│ │Connectors API   │    │
│  └──────────┘ └─────────┘ └───────────┘ └─────────────────┘    │
│                              │                                    │
│  ┌───────────────────────────┴───────────────────────────────┐ │
│  │                   Agent Service Layer                       │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │ │
│  │  │Coordinator  │  │Automation   │  │Communication   │   │ │
│  │  │  Agent      │  │  Agent      │  │    Agent       │   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                    Database (PostgreSQL)                         │
│  Users │ Tasks │ Workflows │ Executions │ Connectors │ Webhooks │
└─────────────────────────────────────────────────────────────────┘

External Integrations:
┌──────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐
│  Slack   │ │  Gmail  │ │  Teams  │ │ Webhooks │
└──────────┘ └─────────┘ └─────────┘ └──────────┘
```

## Project Structure

```
taskflowr/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/        # API endpoints
│   │   │       ├── auth.py
│   │   │       ├── tasks.py
│   │   │       ├── workflows.py
│   │   │       ├── executions.py
│   │   │       └── connectors.py
│   │   ├── core/              # Core utilities
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/                # Database
│   │   │   └── session.py
│   │   ├── models/            # SQLAlchemy models
│   │   │   └── user.py
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   └── agent_service.py
│   │   ├── connectors/        # External integrations
│   │   │   └── registry.py
│   │   └── main.py            # FastAPI app
│   └── requirements.txt
│
├── frontend/                   # Next.js frontend
│   ├── app/
│   │   ├── dashboard/         # Dashboard pages
│   │   │   ├── tasks/
│   │   │   ├── workflows/
│   │   │   ├── executions/
│   │   │   ├── connectors/
│   │   │   └── settings/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   └── ui/                # UI components
│   ├── lib/
│   │   ├── api.ts             # API client
│   │   ├── store.ts           # State management
│   │   └── utils.ts
│   ├── package.json
│   └── tailwind.config.js
│
├── docker-compose.yml          # Local development
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md                   # This file
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

### Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/saad2134/taskflowr
cd taskflowr

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/v1
# API Docs: http://localhost:8000/api/v1/docs
```

### Manual Setup

#### Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
cp .template.env .env
# Edit .env with your values

# Run the backend
uvicorn app.main:app --reload
```

#### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Run the frontend
npm run dev
```

## API Reference

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register a new user |
| `/api/v1/auth/login` | POST | Login and get tokens |
| `/api/v1/auth/refresh` | POST | Refresh access token |
| `/api/v1/auth/me` | GET | Get current user |

### Tasks

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/tasks` | GET | List all tasks |
| `/api/v1/tasks` | POST | Create a new task |
| `/api/v1/tasks/{id}` | GET | Get task details |
| `/api/v1/tasks/{id}` | PUT | Update a task |
| `/api/v1/tasks/{id}` | DELETE | Delete a task |
| `/api/v1/tasks/{id}/execute` | POST | Execute a task |
| `/api/v1/tasks/execute` | POST | Execute task directly |

### Workflows

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/workflows` | GET | List all workflows |
| `/api/v1/workflows` | POST | Create a new workflow |
| `/api/v1/workflows/{id}` | GET | Get workflow details |
| `/api/v1/workflows/{id}` | PUT | Update a workflow |
| `/api/v1/workflows/{id}` | DELETE | Delete a workflow |
| `/api/v1/workflows/{id}/execute` | POST | Execute a workflow |
| `/api/v1/workflows/{id}/activate` | POST | Activate a workflow |
| `/api/v1/workflows/{id}/pause` | POST | Pause a workflow |

### Executions

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/executions` | GET | List all executions |
| `/api/v1/executions/{id}` | GET | Get execution details |
| `/api/v1/executions/{id}/cancel` | POST | Cancel an execution |
| `/api/v1/executions/{id}/logs` | GET | Get execution logs |

### Connectors

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/connectors` | GET | List all connectors |
| `/api/v1/connectors` | POST | Create a connector |
| `/api/v1/connectors/{id}` | GET | Get connector details |
| `/api/v1/connectors/{id}` | PUT | Update a connector |
| `/api/v1/connectors/{id}` | DELETE | Delete a connector |
| `/api/v1/connectors/test` | POST | Test a connector |

### Webhooks

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/webhooks` | GET | List all webhooks |
| `/api/v1/webhooks` | POST | Create a webhook |
| `/api/v1/webhooks/{id}` | DELETE | Delete a webhook |

## Example Usage

### Create and Execute a Task

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Create a task
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Generate Report", "description": "Create a sales report", "input_data": {"instruction": "Generate a sales report for Q4"}}'

# Execute the task
curl -X POST http://localhost:8000/api/v1/tasks/TASK_ID/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input_data": {}}'
```

### Using Connectors

```bash
# Create a Slack connector
curl -X POST http://localhost:8000/api/v1/connectors \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Slack", "connector_type": "slack", "credentials": {"bot_token": "xoxb-..."}}'

# Test the connector
curl -X POST http://localhost:8000/api/v1/connectors/test \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"connector_type": "slack", "credentials": {"bot_token": "xoxb-..."}}'
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | postgresql://taskflowr:taskflowr@localhost:5432/taskflowr |
| `SECRET_KEY` | JWT secret key | (random) |
| `GOOGLE_API_KEY` | Google API key for ADK | - |
| `NEXT_PUBLIC_API_URL` | Frontend API URL | /api |

## Connectors

### Slack Integration

1. Create a Slack App at https://api.slack.com/apps
2. Add Bot Token Scopes: `chat:write`, `channels:read`
3. Install the app to your workspace
4. Use the Bot Token (xoxb-) to create a connector

### Microsoft Teams Integration

1. Create an Incoming Webhook in your Teams channel
2. Use the webhook URL to create a Teams connector

### Gmail Integration

Configure SMTP settings or use Gmail API OAuth2 credentials.

## Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Configure PostgreSQL with SSL
- [ ] Set up HTTPS/TLS
- [ ] Configure CORS for production domains
- [ ] Set up monitoring and logging
- [ ] Configure backup for database

### Docker Production Build

```bash
# Build images
docker build -t taskflowr-backend -f Dockerfile.backend ./backend
docker build -t taskflowr-frontend -f Dockerfile.frontend ./frontend

# Run containers
docker-compose -f docker-compose.prod.yml up -d
```

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style

```bash
# Backend linting
cd backend
ruff check .

# Frontend linting
cd frontend
npm run lint
```

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open a GitHub issue.
