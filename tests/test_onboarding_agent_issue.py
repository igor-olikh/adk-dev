import pytest
import yaml
from pathlib import Path

class TestOnboardingAgentIssue:
    """Test suite specifically for the onboarding agent issue where it returns no results"""
    
    def test_agent_has_instructions_field(self):
        """Test that the onboarding agent has the required instructions field"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # This was the main issue - the agent was missing instructions
        assert "instructions" in agent_config, "Agent must have instructions field"
        assert agent_config["instructions"] is not None, "Instructions field cannot be empty"
        assert len(agent_config["instructions"].strip()) > 0, "Instructions field cannot be empty"
        
        # Verify the instructions contain helpful content
        instructions = agent_config["instructions"]
        assert "onboarding" in instructions.lower(), "Instructions should mention onboarding"
        assert "help" in instructions.lower(), "Instructions should mention helping users"
    
    def test_agent_has_proper_description(self):
        """Test that the onboarding agent has a proper description"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        assert "description" in agent_config, "Agent must have description field"
        assert agent_config["description"] is not None, "Description field cannot be empty"
        assert len(agent_config["description"].strip()) > 0, "Description field cannot be empty"
        
        # Verify the description is comprehensive
        description = agent_config["description"]
        assert "onboarding" in description.lower(), "Description should mention onboarding"
        assert "profile" in description.lower() or "meeting" in description.lower() or "directory" in description.lower(), "Description should mention available capabilities"
    
    def test_agent_has_all_required_fields(self):
        """Test that the onboarding agent has all required fields according to IBM documentation"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        required_fields = [
            "spec_version",
            "kind", 
            "name",
            "llm",
            "style",
            "description",
            "instructions"
        ]
        
        for field in required_fields:
            assert field in agent_config, f"Agent must have {field} field"
            assert agent_config[field] is not None, f"{field} field cannot be None"
            if isinstance(agent_config[field], str):
                assert len(agent_config[field].strip()) > 0, f"{field} field cannot be empty"
    
    def test_agent_references_exist(self):
        """Test that all referenced tools, knowledge bases, and collaborators exist"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Check tools
        for tool_name in agent_config.get("tools", []):
            tool_file = f"tools/{tool_name}.yaml"
            assert Path(tool_file).exists(), f"Referenced tool {tool_name} does not exist"
            
            # Check that the tool YAML is valid
            with open(tool_file, "r") as f:
                tool_config = yaml.safe_load(f)
            assert tool_config["name"] == tool_name, f"Tool YAML name should match {tool_name}"
        
        # Check knowledge bases
        for kb_name in agent_config.get("knowledge_bases", []):
            kb_file = f"knowledge-bases/{kb_name}.yaml"
            assert Path(kb_file).exists(), f"Referenced knowledge base {kb_name} does not exist"
            
            # Check that the knowledge base YAML is valid
            with open(kb_file, "r") as f:
                kb_config = yaml.safe_load(f)
            assert kb_config["name"] == kb_name, f"Knowledge base YAML name should match {kb_name}"
        
        # Check collaborators
        for collab_name in agent_config.get("collaborators", []):
            collab_file = f"agents/{collab_name}.yaml"
            assert Path(collab_file).exists(), f"Referenced collaborator {collab_name} does not exist"
            
            # Check that the collaborator YAML is valid
            with open(collab_file, "r") as f:
                collab_config = yaml.safe_load(f)
            assert collab_config["name"] == collab_name, f"Collaborator YAML name should match {collab_name}"
    
    def test_knowledge_base_document_path_is_correct(self):
        """Test that the knowledge base document path is correct"""
        with open("knowledge-bases/onboarding_docs.yaml", "r") as f:
            kb_config = yaml.safe_load(f)
        
        # This was another issue - the document path was incorrect
        doc_path = kb_config["documents"][0]
        assert Path(doc_path).exists(), f"Knowledge base document {doc_path} does not exist"
        
        # Verify it's pointing to the correct location
        expected_path = "knowledge-bases/docs/onboarding_policy.pdf"
        assert doc_path == expected_path, f"Document path should be {expected_path}, got {doc_path}"
    
    def test_connections_have_proper_app_ids(self):
        """Test that connections have proper app_id fields"""
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        for conn_file in connection_files:
            with open(conn_file, "r") as f:
                conn_config = yaml.safe_load(f)
            
            # According to IBM documentation, connections must have app_id field
            assert "app_id" in conn_config, f"Connection {conn_file} must have app_id field"
            assert conn_config["app_id"] is not None, f"Connection {conn_file} app_id cannot be None"
            assert len(conn_config["app_id"].strip()) > 0, f"Connection {conn_file} app_id cannot be empty"
    
    def test_tools_have_proper_error_handling(self):
        """Test that tools have proper error handling"""
        # Import and test the tools to ensure they handle errors gracefully
        try:
            from tools.create_profile_tool import create_profile
            from tools.schedule_meeting_tool import schedule_meeting
            from tools.get_directory_tool import get_directory_info
            
            # Test with missing services (should return error messages, not crash)
            result1 = create_profile("Test User", "test@example.com", "Test Title")
            assert isinstance(result1, str), "Tool should return string result"
            assert len(result1) > 0, "Tool should return non-empty result"
            
            result2 = schedule_meeting("Test Meeting", ["test@example.com"], "2024-01-15T10:00:00")
            assert isinstance(result2, str), "Tool should return string result"
            assert len(result2) > 0, "Tool should return non-empty result"
            assert "Successfully scheduled" in result2, "Tool should indicate success"
            
            result3 = get_directory_info("test@example.com")
            assert isinstance(result3, str), "Tool should return string result"
            assert len(result3) > 0, "Tool should return non-empty result"
            
        except ImportError as e:
            pytest.fail(f"Could not import tools: {e}")
        except Exception as e:
            pytest.fail(f"Error testing tools: {e}")
    
    def test_agent_configuration_is_complete(self):
        """Test that the agent configuration is complete and ready for use"""
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Verify the agent has all necessary components for onboarding
        assert len(agent_config.get("tools", [])) >= 3, "Agent should have at least 3 tools"
        assert len(agent_config.get("knowledge_bases", [])) >= 1, "Agent should have at least 1 knowledge base"
        assert len(agent_config.get("collaborators", [])) >= 1, "Agent should have at least 1 collaborator"
        
        # Verify the tools are appropriate for onboarding
        tools = agent_config.get("tools", [])
        expected_tools = ["create_profile_tool", "schedule_meeting_tool", "get_directory_tool"]
        for expected_tool in expected_tools:
            assert expected_tool in tools, f"Agent should have {expected_tool}"
        
        # Verify the knowledge base is appropriate
        knowledge_bases = agent_config.get("knowledge_bases", [])
        assert "onboarding_docs" in knowledge_bases, "Agent should have onboarding_docs knowledge base"
        
        # Verify the collaborator is appropriate
        collaborators = agent_config.get("collaborators", [])
        assert "hr_specialist_agent" in collaborators, "Agent should have hr_specialist_agent collaborator" 