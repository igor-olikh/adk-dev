import pytest
import yaml
from pathlib import Path

class TestOnboardingAgentResponses:
    """Test suite to verify the onboarding agent can properly respond to requests"""
    
    def test_agent_can_handle_onboarding_requests(self):
        """Test that the agent has the necessary configuration to handle onboarding requests"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Verify the agent has the right tools for onboarding
        tools = agent_config.get("tools", [])
        required_tools = ["create_profile_tool", "schedule_meeting_tool", "get_directory_tool"]
        
        for tool in required_tools:
            assert tool in tools, f"Agent must have {tool} to handle onboarding requests"
        
        # Verify the agent has instructions that guide it on how to respond
        instructions = agent_config.get("instructions", "")
        assert "onboarding" in instructions.lower(), "Instructions must mention onboarding"
        assert "help" in instructions.lower(), "Instructions must mention helping users"
        assert "profile" in instructions.lower() or "meeting" in instructions.lower(), "Instructions must mention available actions"
    
    def test_agent_has_starter_prompts(self):
        """Test that the agent has starter prompts to guide user interactions"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Check if starter prompts are configured
        if "starter_prompts" in agent_config:
            starter_prompts = agent_config["starter_prompts"]
            
            # If starter prompts are configured, they should be properly structured
            if starter_prompts.get("is_default_prompts") is False:
                prompts = starter_prompts.get("prompts", [])
                assert len(prompts) > 0, "If custom starter prompts are configured, there should be at least one"
                
                for prompt in prompts:
                    assert "id" in prompt, "Each starter prompt should have an id"
                    assert "title" in prompt, "Each starter prompt should have a title"
                    assert "prompt" in prompt, "Each starter prompt should have a prompt text"
                    assert "state" in prompt, "Each starter prompt should have a state"
    
    def test_agent_has_guidelines(self):
        """Test that the agent has guidelines for tool invocation"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Check if guidelines are configured
        if "guidelines" in agent_config:
            guidelines = agent_config["guidelines"]
            assert len(guidelines) > 0, "If guidelines are configured, there should be at least one"
            
            for guideline in guidelines:
                assert "display_name" in guideline, "Each guideline should have a display_name"
                assert "condition" in guideline, "Each guideline should have a condition"
                assert "action" in guideline, "Each guideline should have an action"
                assert "tool" in guideline, "Each guideline should have a tool"
    
    def test_agent_has_collaboration_capability(self):
        """Test that the agent can collaborate with other agents"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        collaborators = agent_config.get("collaborators", [])
        assert len(collaborators) > 0, "Agent should have at least one collaborator for complex requests"
        
        # Verify the HR specialist agent exists and is properly configured
        assert "hr_specialist_agent" in collaborators, "Agent should have hr_specialist_agent as collaborator"
        
        # Check that the collaborator agent exists and has instructions
        hr_agent_file = "agents/hr_specialist_agent.yaml"
        assert Path(hr_agent_file).exists(), "HR specialist agent should exist"
        
        with open(hr_agent_file, "r") as f:
            hr_agent_config = yaml.safe_load(f)
        
        assert "instructions" in hr_agent_config, "HR specialist agent should have instructions"
        assert len(hr_agent_config["instructions"].strip()) > 0, "HR specialist agent instructions should not be empty"
    
    def test_agent_has_knowledge_base_access(self):
        """Test that the agent has access to knowledge base for policy information"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        knowledge_bases = agent_config.get("knowledge_bases", [])
        assert len(knowledge_bases) > 0, "Agent should have access to at least one knowledge base"
        
        # Verify the onboarding docs knowledge base exists and is properly configured
        assert "onboarding_docs" in knowledge_bases, "Agent should have access to onboarding_docs knowledge base"
        
        # Check that the knowledge base exists and references valid documents
        kb_file = "knowledge-bases/onboarding_docs.yaml"
        assert Path(kb_file).exists(), "Onboarding docs knowledge base should exist"
        
        with open(kb_file, "r") as f:
            kb_config = yaml.safe_load(f)
        
        documents = kb_config.get("documents", [])
        assert len(documents) > 0, "Knowledge base should reference at least one document"
        
        for doc_path in documents:
            assert Path(doc_path).exists(), f"Referenced document {doc_path} should exist"
    
    def test_agent_tools_are_functional(self):
        """Test that all agent tools are functional and can be called"""
        try:
            from tools.create_profile_tool import create_profile
            from tools.schedule_meeting_tool import schedule_meeting
            from tools.get_directory_tool import get_directory_info
            
            # Test create profile tool
            profile_result = create_profile("Jane Doe", "jane.doe@example.com", "Software Engineer")
            assert isinstance(profile_result, str), "Create profile tool should return a string"
            assert len(profile_result) > 0, "Create profile tool should return a non-empty result"
            
            # Test schedule meeting tool
            meeting_result = schedule_meeting(
                "Welcome Meeting", 
                ["jane.doe@example.com", "manager@example.com"], 
                "2024-01-15T14:00:00",
                30
            )
            assert isinstance(meeting_result, str), "Schedule meeting tool should return a string"
            assert len(meeting_result) > 0, "Schedule meeting tool should return a non-empty result"
            assert "Successfully scheduled" in meeting_result, "Schedule meeting tool should indicate success"
            
            # Test get directory tool
            directory_result = get_directory_info("alice@example.com")
            assert isinstance(directory_result, str), "Get directory tool should return a string"
            assert len(directory_result) > 0, "Get directory tool should return a non-empty result"
            
        except ImportError as e:
            pytest.fail(f"Could not import agent tools: {e}")
        except Exception as e:
            pytest.fail(f"Error testing agent tools: {e}")
    
    def test_agent_configuration_follows_ibm_standards(self):
        """Test that the agent configuration follows IBM watsonx Orchestrate standards"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Check spec version
        assert agent_config["spec_version"] == "v1", "Agent should use spec_version v1"
        
        # Check kind
        assert agent_config["kind"] == "native", "Agent should be of kind 'native'"
        
        # Check LLM configuration
        assert "llm" in agent_config, "Agent should specify an LLM"
        llm = agent_config["llm"]
        assert "watsonx" in llm, "Agent should use a watsonx LLM"
        
        # Check style
        assert "style" in agent_config, "Agent should specify a style"
        style = agent_config["style"]
        assert style in ["default", "react", "planner"], f"Agent style should be one of: default, react, planner, got: {style}"
        
        # Check that all required fields are present and non-empty
        required_fields = ["name", "description", "instructions"]
        for field in required_fields:
            assert field in agent_config, f"Agent should have {field} field"
            assert agent_config[field] is not None, f"Agent {field} should not be None"
            assert len(agent_config[field].strip()) > 0, f"Agent {field} should not be empty"
    
    def test_agent_can_handle_typical_onboarding_scenarios(self):
        """Test that the agent has the capability to handle typical onboarding scenarios"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        instructions = agent_config.get("instructions", "").lower()
        description = agent_config.get("description", "").lower()
        
        # Check that the agent can handle profile creation
        assert "profile" in instructions or "profile" in description, "Agent should mention profile creation capability"
        
        # Check that the agent can handle meeting scheduling
        assert "meeting" in instructions or "meeting" in description, "Agent should mention meeting scheduling capability"
        
        # Check that the agent can handle directory lookups
        assert "directory" in instructions or "directory" in description, "Agent should mention directory lookup capability"
        
        # Check that the agent can collaborate for complex issues
        assert "escalate" in instructions or "collaborate" in instructions or "specialist" in instructions, "Agent should mention collaboration capability"
        
        # Check that the agent provides step-by-step guidance
        assert "step" in instructions or "guide" in instructions or "help" in instructions, "Agent should mention providing guidance" 