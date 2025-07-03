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

# Configure the service-now connection
echo "Configuring service-now connection..."
if [ -n "$SERVICE_NOW_URL" ]; then
    echo "Using ServiceNow URL from .env file: $SERVICE_NOW_URL"
    orchestrate connections configure -a service-now --env live --type team --kind basic --url "$SERVICE_NOW_URL"
else
    echo "Warning: SERVICE_NOW_URL not found in .env file"
    echo "Please provide the ServiceNow instance URL when prompted"
    orchestrate connections configure -a service-now --env live --type team --kind basic
fi

# Set credentials for the service-now connection
echo "Setting ServiceNow credentials..."
if [ -n "$SERVICE_NOW_PASSWORD" ]; then
    echo "Using ServiceNow password from .env file"
    orchestrate connections set-credentials -a service-now --env live -u admin -p "$SERVICE_NOW_PASSWORD"
else
    echo "Warning: SERVICE_NOW_PASSWORD not found in .env file"
    echo "Please provide the ServiceNow password when prompted"
    orchestrate connections set-credentials -a service-now --env live -u admin
fi
