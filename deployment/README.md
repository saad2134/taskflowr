# TaskFlowr Deployment Guide

## 🚀 Quick Deployment

### Option 1: Local Development
```bash
# 1. Clone repository
git clone https://github.com/saad2134/taskflowr
cd taskflowr

# 2. Set up environment
export GOOGLE_API_KEY=your_api_key_here

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the system
python -m agent.coordinator
```

### Option 2: Docker Deployment
```bash
# Build image
docker build -t taskflowr .

# Run container
docker run -e GOOGLE_API_KEY=your_api_key_here -p 8080:8080 taskflowr
```

### Option 3: Vertex AI Agent Engine
```bash
# Deploy to Google Cloud
gcloud ai agents create --config=deployment/agent_engine_config.json
```

## 📋 Prerequisites

- Python 3.9+
- Google API key with Gemini access
- 1GB+ RAM
- Internet connectivity

## 🔧 Configuration

### Environment Variables
```
GOOGLE_API_KEY=your_gemini_api_key
ENVIRONMENT=production|development
LOG_LEVEL=INFO|DEBUG
```

### Model Settings

- Primary: ```gemini-2.0-flash-exp```
- Fallback: ```gemini-1.5-flash```

## 📊 Monitoring

- Logs: ```logs/taskflowr.log```
- Metrics: Built-in observability agent
- Health: ```GET /health``` endpoint

## 🛠️ Troubleshooting

### Common Issues

1. API Key Errors
    - Verify GOOGLE_API_KEY is set
    - Check Gemini API access
2. Import Errors
    - Ensure PYTHONPATH includes project root
    - Verify all dependencies installed
3. Performance Issues
    - Check network connectivity
    - Monitor memory usage
    - Review agent response times

## 📞 Support

For deployment issues:

1. Check logs in logs/ directory
2. Verify API key permissions
3. Ensure all dependencies are installed

> See main README for usage examples and agent documentation.
