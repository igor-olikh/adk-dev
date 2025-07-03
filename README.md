# HR Onboarding Assistant – watsonx Orchestrate ADK

A modular, end-to-end onboarding agent built with IBM watsonx Orchestrate ADK. Automates new-hire setup: profile creation, meeting invites, directory lookups, policy Q&A, and escalation workflows. Includes mock services, tests, evaluation flow, and starter prompts—designed as a hands-on learning reference.

---

## 🚀 Features

- **Mocked HR & Directory services** using FastAPI—no external dependencies  
- **Connections**: secure credential management for API integrations  
- **Tools**: Python and OpenAPI tools for external interactions  
- **Knowledge Base**: ingest onboarding policy PDFs for document chat  
- **Flow Tool**: orchestrate multi-step onboarding operations  
- **Guidelines**: smart tool invocation based on query patterns  
- **Collaborators**: escalate to specialist agents when needed  
- **Starter Prompts**: intuitive chat entry points for users  
- **Evaluation Framework**: define test scenarios and measure results  
- **Chat UI**: launch a local interface with starter prompts

---

## 🧠 Learning Outcomes

You'll learn how to:
- Define and manage **connections**, **tools**, **KBs**, **flows**, **guidelines** and **starter prompts**
- Integrate and test with **mock services**
- Validate agent behavior with **pytest** and ADK evaluation
- Run an interactive chat UI using **orchestrate chat**

---

## 📌 Getting Started

1. Follow **[HOWTO.md](HOWTO.md)** to install dependencies, run services, import resources, run tests, and launch chat.
2. Adjust mocks or tools to fit your environment—swap in real APIs without changing agent logic.
3. Extend agents with new features or integrate with real-world systems via additional connections/tools.

## 🔧 ServiceNow Integration Setup

The `run-service-now.sh` script provides automated setup for ServiceNow integration with watsonx Orchestrate. This script configures the complete ServiceNow environment including connections, tools, and agents.

### Prerequisites

Create a `.env` file in the project root with the following variables:
```bash
WO_API_KEY=your_orchestrate_api_key_here
SERVICE_NOW_URL=your_servicenow_instance_url_here
SERVICE_NOW_PASSWORD=your_servicenow_password_here
```

### What the Script Does

The `run-service-now.sh` script performs the following automated setup:

1. **Environment Activation**: Activates the wxo-cloud environment using the API key from `.env`
2. **Connection Management**: 
   - Removes existing service-now connection if present
   - Adds new service-now connection
   - Configures connection with ServiceNow URL and credentials
3. **Tool Imports**:
   - Healthcare tools: `get_my_claims.py`, `get_healthcare_benefits.py`, `search_healthcare_providers.py`
   - ServiceNow tools: `create_service_now_incident.py`, `get_my_service_now_incidents.py`, `get_service_now_incident_by_number.py`
4. **Agent Imports**: Imports `service_now_agent.yaml` and `customer_care_agent.yaml`

### Usage

```bash
# Make the script executable
chmod +x run-service-now.sh

# Run the setup script
./run-service-now.sh
```

The script provides clear feedback at each step and handles both automated and manual credential input scenarios.

---

## 🛡️ Strategic Value

This project demonstrates automation of repetitive and manual HR tasks. It showcases watsonx Orchestrate's capabilities for enterprise-grade efficiency, compliance, and scalability in HR workflows.

---

### 🔗 Related Resources

- IBM watsonx Orchestrate documentation (getting-started, agents, tools, evaluation)  
- IBM HR agent case studies (e.g., 12,000 hours saved per quarter in HR operations)

---

## 📝 License

This repository is made available under the Apache‑2.0 License.

---

👍 Contributions welcome. Feel free to open issues or create PRs to extend mock services, test coverage, or CI/CD support.