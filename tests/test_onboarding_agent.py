import pytest
import requests
import subprocess
import time
import os
from pathlib import Path

class TestOnboardingAgent:
    """Test suite for the onboarding agent functionality"""
    
    def setup_method(self):
        """Setup method to start mock services before each test"""
        self.hr_process = None
        self.dir_process = None
        
        # Start mock HR service
        try:
            self.hr_process = subprocess.Popen(
                ["python", "-m", "uvicorn", "mocks.hr_service:app", "--host", "0.0.0.0", "--port", "8001"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(2)  # Wait for service to start
        except Exception as e:
            print(f"Warning: Could not start HR service: {e}")
        
        # Start mock Directory service
        try:
            self.dir_process = subprocess.Popen(
                ["python", "-m", "uvicorn", "mocks.directory_service:app", "--host", "0.0.0.0", "--port", "8002"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(2)  # Wait for service to start
        except Exception as e:
            print(f"Warning: Could not start Directory service: {e}")
    
    def teardown_method(self):
        """Teardown method to stop mock services after each test"""
        if self.hr_process:
            self.hr_process.terminate()
            self.hr_process.wait()
        
        if self.dir_process:
            self.dir_process.terminate()
            self.dir_process.wait()
    
    def test_agent_configuration_files_exist(self):
        """Test that all required configuration files exist"""
        required_files = [
            "agents/onboarding_agent.yaml",
            "agents/hr_specialist_agent.yaml",
            "tools/create_profile_tool.yaml",
            "tools/schedule_meeting_tool.yaml",
            "tools/get_directory_tool.yaml",
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml",
            "knowledge-bases/onboarding_docs.yaml"
        ]
        
        for file_path in required_files:
            assert Path(file_path).exists(), f"Required file {file_path} does not exist"
    
    def test_agent_yaml_structure(self):
        """Test that the onboarding agent YAML has the correct structure"""
        import yaml
        
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Check required fields
        assert agent_config["spec_version"] == "v1"
        assert agent_config["kind"] == "native"
        assert agent_config["name"] == "onboarding_agent"
        assert "llm" in agent_config
        assert "style" in agent_config
        assert "description" in agent_config
        assert "instructions" in agent_config
        assert "tools" in agent_config
        assert "knowledge_bases" in agent_config
        assert "collaborators" in agent_config
    
    def test_tools_yaml_structure(self):
        """Test that tool YAML files have the correct structure"""
        import yaml
        
        tool_files = [
            "tools/create_profile_tool.yaml",
            "tools/schedule_meeting_tool.yaml",
            "tools/get_directory_tool.yaml"
        ]
        
        for tool_file in tool_files:
            with open(tool_file, "r") as f:
                tool_config = yaml.safe_load(f)
            
            assert tool_config["spec_version"] == "v1"
            assert tool_config["kind"] == "tool"
            assert tool_config["toolkit"] == "python"
            assert "name" in tool_config
            assert "connection" in tool_config
            assert "entrypoint" in tool_config
            assert "description" in tool_config
    
    def test_connections_yaml_structure(self):
        """Test that connection YAML files have the correct structure"""
        import yaml
        
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        for conn_file in connection_files:
            with open(conn_file, "r") as f:
                conn_config = yaml.safe_load(f)
            
            assert conn_config["spec_version"] == "v1"
            assert conn_config["kind"] == "connection"
            assert "app_id" in conn_config
            assert "environments" in conn_config
    
    def test_knowledge_base_yaml_structure(self):
        """Test that knowledge base YAML has the correct structure"""
        import yaml
        
        with open("knowledge-bases/onboarding_docs.yaml", "r") as f:
            kb_config = yaml.safe_load(f)
        
        assert kb_config["spec_version"] == "v1"
        assert kb_config["kind"] == "knowledge_base"
        assert kb_config["name"] == "onboarding_docs"
        assert "description" in kb_config
        assert "documents" in kb_config
        
        # Check that the referenced document exists
        doc_path = kb_config["documents"][0]
        assert Path(doc_path).exists(), f"Referenced document {doc_path} does not exist"
    
    def test_mock_hr_service_connectivity(self):
        """Test that the mock HR service is accessible"""
        try:
            response = requests.get("http://localhost:8001/docs", timeout=5)
            assert response.status_code == 200, "HR service should be accessible"
        except requests.exceptions.ConnectionError:
            pytest.skip("HR service not running - skipping connectivity test")
    
    def test_mock_directory_service_connectivity(self):
        """Test that the mock Directory service is accessible"""
        try:
            response = requests.get("http://localhost:8002/docs", timeout=5)
            assert response.status_code == 200, "Directory service should be accessible"
        except requests.exceptions.ConnectionError:
            pytest.skip("Directory service not running - skipping connectivity test")
    
    def test_create_profile_tool_functionality(self):
        """Test that the create profile tool can be imported and called"""
        try:
            from tools.create_profile_tool import create_profile
            
            # Test the tool function
            result = create_profile("John Doe", "john.doe@example.com", "Software Engineer")
            assert isinstance(result, str), "Tool should return a string result"
            assert len(result) > 0, "Tool should return a non-empty result"
            
        except ImportError as e:
            pytest.fail(f"Could not import create_profile_tool: {e}")
        except Exception as e:
            pytest.fail(f"Error testing create_profile_tool: {e}")
    
    def test_schedule_meeting_tool_functionality(self):
        """Test that the schedule meeting tool can be imported and called"""
        try:
            from tools.schedule_meeting_tool import schedule_meeting
            
            # Test the tool function
            result = schedule_meeting(
                "Onboarding Meeting",
                ["hr@example.com", "manager@example.com"],
                "2024-01-15T10:00:00",
                60
            )
            assert isinstance(result, str), "Tool should return a string result"
            assert len(result) > 0, "Tool should return a non-empty result"
            assert "Successfully scheduled" in result, "Tool should indicate successful scheduling"
            
        except ImportError as e:
            pytest.fail(f"Could not import schedule_meeting_tool: {e}")
        except Exception as e:
            pytest.fail(f"Error testing schedule_meeting_tool: {e}")
    
    def test_get_directory_tool_functionality(self):
        """Test that the get directory tool can be imported and called"""
        try:
            from tools.get_directory_tool import get_directory_info
            
            # Test the tool function
            result = get_directory_info("alice@example.com")
            assert isinstance(result, str), "Tool should return a string result"
            assert len(result) > 0, "Tool should return a non-empty result"
            
        except ImportError as e:
            pytest.fail(f"Could not import get_directory_tool: {e}")
        except Exception as e:
            pytest.fail(f"Error testing get_directory_tool: {e}")
    
    def test_agent_has_required_components(self):
        """Test that the onboarding agent has all required components configured"""
        import yaml
        
        with open("agents/onboarding_agent.yaml", "r") as f:
            agent_config = yaml.safe_load(f)
        
        # Check that all referenced tools exist
        for tool_name in agent_config.get("tools", []):
            tool_file = f"tools/{tool_name}.yaml"
            assert Path(tool_file).exists(), f"Referenced tool {tool_name} does not exist"
        
        # Check that all referenced knowledge bases exist
        for kb_name in agent_config.get("knowledge_bases", []):
            kb_file = f"knowledge-bases/{kb_name}.yaml"
            assert Path(kb_file).exists(), f"Referenced knowledge base {kb_name} does not exist"
        
        # Check that all referenced collaborators exist
        for collab_name in agent_config.get("collaborators", []):
            collab_file = f"agents/{collab_name}.yaml"
            assert Path(collab_file).exists(), f"Referenced collaborator {collab_name} does not exist" 