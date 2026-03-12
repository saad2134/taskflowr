#!/bin/bash

# TaskFlowr Deployment Script
echo "🚀 Deploying TaskFlowr Multi-Agent System..."

# Check for API key
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ ERROR: GOOGLE_API_KEY environment variable not set"
    echo "Please set your Google API key:"
    echo "export GOOGLE_API_KEY=your_api_key_here"
    exit 1
fi

# Create necessary directories
mkdir -p logs data outputs

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run health check
echo "🔍 Running system health check..."
python -c "
from agent.coordinator import create_coordinator
coordinator = create_coordinator()
print('✅ System health check passed')
"

# Start the coordinator agent
echo "🎯 Starting TaskFlowr Coordinator Agent..."
echo "📝 Logs will be saved to logs/taskflowr.log"
echo "🕒 Starting at: $(date)"

# Run the coordinator
python -m agent.coordinator