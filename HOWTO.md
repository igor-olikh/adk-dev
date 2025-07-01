# 🚀 HOWTO.md

## 1. Prerequisites

- Python 3.11–3.13  
- Docker (Rancher or Colima), and at least 16GB RAM, 8 CPU cores, 25GB disk  
- Access to the `ibm-watsonx-orchestrate` Python package  

## 2. Clone & Install

```bash
git clone <your-repo-url> hr-onboarding-agent
cd hr-onboarding-agent
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade ibm-watsonx-orchestrate fastapi uvicorn pytest
```

## 3. Launch Watsonx Orchestrate Developer Edition

```bash
orchestrate server start --env-file=.env
orchestrate env activate local
```

## 4. Run Mock Services

```bash
uvicorn mocks.hr_service:app --port 8001 --reload &
uvicorn mocks.directory_service:app --port 8002 --reload &
```

## 5. Import Connections

```bash
orchestrate connections import --file connections/hr_api_connection.yaml
orchestrate connections import --file connections/directory_api_connection.yaml

orchestrate connections set-credentials --app-id hr_api_conn --env draft --api-key dummy_hr_key
orchestrate connections set-credentials --app-id dir_api_conn --env draft --api-key dummy_dir_key
```

## 6. Import Tools

```bash
orchestrate tools import -k python -f tools/create_profile_tool.yaml
orchestrate tools import -k openapi -f tools/schedule_meeting_tool.yaml
orchestrate tools import -k python -f tools/get_directory_tool.yaml
```

## 7. Import Knowledge Base

```bash
orchestrate knowledge-bases import -f knowledge-bases/onboarding_docs.yaml
```

## 8. Import Flow & Agents

```bash
orchestrate tools import -k flow -f flows/onboarding_flow.yaml
orchestrate agents import --file agents/onboarding_agent.yaml
orchestrate agents import --file agents/hr_specialist_agent.yaml
```

## 9. Run Tests

```bash
pytest tests/
```

## 10. Evaluate the Onboarding Agent

```bash
orchestrate evaluate agent onboarding_agent --config evaluations/onboarding_tests.json
```

## 11. Start the Chat UI

```bash
orchestrate chat start
```

Then click the **Begin Onboarding** starter prompt.

## 12. Clean Up

```bash
orchestrate server stop
pkill uvicorn
```

---

## ✅ What You’ll Learn

- Setting up **connections**, **tools**, **knowledge bases**, **flows**, **guidelines**, and **starter prompts**
- Integrating **mock services** (HR + Directory)
- Running **pytest** for mock integration
- Using `orchestrate evaluate` for performance checks
- Launching a **local chat UI** with end-to-end onboarding flow

---

For CI/CD snippets, shell automation, or VS Code debugging tips, let me know.