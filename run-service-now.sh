#!/bin/bash
set -e

# chmod +x run-service-now.sh

# Source .env file if it exists
if [ -f .env ]; then
    source .env
fi

# Activate the wxo-cloud environment
echo "Activating wxo-cloud environment..."

# If WO_API_KEY is set, provide it when prompted
if [ -n "$WO_API_KEY" ]; then
    echo "API key found in environment variables"
    echo "$WO_API_KEY" | orchestrate env activate wxo-cloud
else
    echo "Warning: WO_API_KEY not found in .env file"
    echo "Please provide your API key when prompted"
    orchestrate env activate wxo-cloud
fi

# Check if service-now connection exists and remove it if it does
echo "Checking for existing service-now connection..."
if orchestrate connections list | grep -q "service-now"; then
    echo "Removing existing service-now connection..."
    orchestrate connections remove --app-id service-now
else
    echo "No existing service-now connection found"
fi

# Add the service-now connection
echo "Adding service-now connection..."
orchestrate connections add -a service-now --app-id service-now
