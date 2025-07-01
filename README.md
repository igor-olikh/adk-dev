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

## 📁 Repository Structure

```text
adk-dev/
├── agents/
│   ├── hr_specialist_agent.yaml
│   └── onboarding_agent.yaml
├── connections/
│   ├── directory_api_connection.yaml
│   └── hr_api_connection.yaml
├── docs/
│   ├── .steps-create-agent
│   └── .steps-start-server
├── evaluations/
│   └── onboarding_tests.json
├── flows/
│   └── onboarding_flow.yaml
├── knowledge-bases/
│   └── onboarding_docs.yaml
├── mocks/
│   ├── directory_service.py
│   ├── hr_service.py
│   └── __pycache__/
├── tests/
├── tools/
│   ├── create_profile_tool.yaml
│   ├── get_directory_tool.yaml
│   ├── schedule_meeting_tool.yaml
│   ├── test_directory.py
│   └── test_hr.py
├── HOWTO.md
├── poetry.lock
├── poetry.toml
├── pyproject.toml
└── README.md
```

See full structure above for file details.

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