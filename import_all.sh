#!/bin/bash
set -e

# Import connections
for conn_file in ./connections/*.yaml; do
  echo "Importing connection: $conn_file"
  orchestrate connections import --file "$conn_file"
done

echo "\n# Set credentials for connections (update these as needed)"
# Example: set credentials for hr_api_conn and dir_api_conn if you have API keys in .env
if [ -f .env ]; then
  HR_API_KEY=$(grep '^HR_API_KEY[[:space:]]*=' .env | sed 's/^[^=]*=[[:space:]]*//')
  DIR_API_KEY=$(grep '^DIR_API_KEY[[:space:]]*=' .env | sed 's/^[^=]*=[[:space:]]*//')
  if [ ! -z "$HR_API_KEY" ]; then
    orchestrate connections set-credentials --app-id hr_api_conn --env draft --api-key "$HR_API_KEY"
  fi
  if [ ! -z "$DIR_API_KEY" ]; then
    orchestrate connections set-credentials --app-id dir_api_conn --env draft --api-key "$DIR_API_KEY"
  fi
fi

# Import tools
for tool_yaml in ./tools/*.yaml; do
  TOOL_NAME=$(grep '^name:' "$tool_yaml" | awk '{print $2}')
  TOOL_PY=$(echo "$tool_yaml" | sed 's/.yaml$/.py/')
  if [ -f "$TOOL_PY" ]; then
    echo "Importing tool: $tool_yaml ($TOOL_PY)"
    orchestrate tools import \
      -k python \
      -f "$TOOL_PY" \
      -p "./tools" \
      -a $(grep '^connection:' "$tool_yaml" | awk '{print $2}')
  fi
done

# Import knowledge bases
for kb_yaml in ./knowledge-bases/*.yaml; do
  echo "Importing knowledge base: $kb_yaml"
  orchestrate knowledge-bases import -f "$kb_yaml"
done

# Import agents
for agent_yaml in ./agents/*.yaml; do
  echo "Importing agent: $agent_yaml"
  orchestrate agents import -f "$agent_yaml"
done

echo "\nAll imports completed." 