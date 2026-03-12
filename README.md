# TaskFlowr - Multi-Agent Workflow Automation System

> A complete full-stack implementation of a 3-agent system built using the OpenAI ADK that automates general business operations.

## Project Structure

```
taskflowr/
├── backend/          # FastAPI backend with REST API
├── frontend/         # Next.js React frontend
├── docs/             # Full-stack documentation
├── standalone/       # Original ADK-only version
└── docker-compose.yml
```

## Quick Start

### Full-Stack Version (Recommended)

```bash
# Start all services with Docker
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/v1
# API Docs: http://localhost:8000/api/v1/docs
```

### Standalone Version (Original ADK)

See `standalone/README.md` for instructions on running the original ADK-only version.

## Features

### Full-Stack
- **REST API** with JWT authentication
- **React Dashboard** for managing tasks and workflows
- **External Connectors**: Slack, Gmail, Teams, Webhooks
- **PostgreSQL Database** for persistence

### Standalone (ADK Only)
- Multi-agent coordination (Coordinator, Automation, Communication)
- Workflow automation
- Structured data processing

## Documentation

- [Full-Stack Implementation Guide](docs/FULLSTACK.md)
- [Standalone Version](standalone/README.md)

## License

MIT License - see standalone/LICENSE
