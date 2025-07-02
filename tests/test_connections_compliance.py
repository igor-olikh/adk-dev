import pytest
import yaml
from pathlib import Path

class TestConnectionsCompliance:
    """Test suite to verify connection configurations comply with IBM watsonx Orchestrate ADK requirements"""
    
    def test_connection_files_exist(self):
        """Test that all required connection files exist"""
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        for file_path in connection_files:
            assert Path(file_path).exists(), f"Connection file {file_path} does not exist"
    
    def test_connection_yaml_structure(self):
        """Test that connection YAML files have the correct structure according to IBM documentation"""
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        for conn_file in connection_files:
            with open(conn_file, "r") as f:
                conn_config = yaml.safe_load(f)
            
            # Check required top-level fields according to IBM documentation
            assert "spec_version" in conn_config, f"Connection {conn_file} must have spec_version field"
            assert conn_config["spec_version"] == "v1", f"Connection {conn_file} must use spec_version v1"
            
            assert "kind" in conn_config, f"Connection {conn_file} must have kind field"
            assert conn_config["kind"] == "connection", f"Connection {conn_file} kind must be 'connection'"
            
            assert "app_id" in conn_config, f"Connection {conn_file} must have app_id field"
            assert conn_config["app_id"] is not None, f"Connection {conn_file} app_id cannot be None"
            assert len(conn_config["app_id"].strip()) > 0, f"Connection {conn_file} app_id cannot be empty"
            
            assert "environments" in conn_config, f"Connection {conn_file} must have environments field"
            assert isinstance(conn_config["environments"], dict), f"Connection {conn_file} environments must be a dictionary"
    
    def test_environment_configuration(self):
        """Test that environment configurations are properly structured"""
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        for conn_file in connection_files:
            with open(conn_file, "r") as f:
                conn_config = yaml.safe_load(f)
            
            environments = conn_config["environments"]
            
            # Check that at least one environment is configured
            assert len(environments) > 0, f"Connection {conn_file} must have at least one environment configured"
            
            # Check each environment configuration
            for env_name, env_config in environments.items():
                assert "kind" in env_config, f"Environment {env_name} in {conn_file} must have kind field"
                assert env_config["kind"] in ["basic", "bearer", "api_key", "oauth_auth_on_behalf_of_flow", "key_value", "kv"], \
                    f"Environment {env_name} in {conn_file} must have valid kind: basic, bearer, api_key, oauth_auth_on_behalf_of_flow, key_value, or kv"
                
                assert "type" in env_config, f"Environment {env_name} in {conn_file} must have type field"
                assert env_config["type"] in ["team", "member"], \
                    f"Environment {env_name} in {conn_file} must have valid type: team or member"
                
                # Check for server_url (required for OpenAPI tools and Python tools)
                assert "server_url" in env_config, f"Environment {env_name} in {conn_file} must have server_url field"
                assert env_config["server_url"] is not None, f"Environment {env_name} in {conn_file} server_url cannot be None"
                assert len(env_config["server_url"].strip()) > 0, f"Environment {env_name} in {conn_file} server_url cannot be empty"
                
                # Validate server_url format
                server_url = env_config["server_url"]
                assert server_url.startswith(("http://", "https://")), f"Environment {env_name} in {conn_file} server_url must be a valid URL"
    
    def test_hr_api_connection_specific_configuration(self):
        """Test specific configuration for HR API connection"""
        with open("connections/hr_api_connection.yaml", "r") as f:
            conn_config = yaml.safe_load(f)
        
        # Check app_id
        assert conn_config["app_id"] == "hr_api_conn", "HR API connection should have app_id 'hr_api_conn'"
        
        # Check draft environment
        draft_env = conn_config["environments"]["draft"]
        assert draft_env["kind"] == "api_key", "HR API connection should use api_key authentication"
        assert draft_env["type"] == "team", "HR API connection should use team credentials"
        assert draft_env["server_url"] == "http://localhost:8001/", "HR API connection should point to localhost:8001"
    
    def test_directory_api_connection_specific_configuration(self):
        """Test specific configuration for Directory API connection"""
        with open("connections/directory_api_connection.yaml", "r") as f:
            conn_config = yaml.safe_load(f)
        
        # Check app_id
        assert conn_config["app_id"] == "dir_api_conn", "Directory API connection should have app_id 'dir_api_conn'"
        
        # Check draft environment
        draft_env = conn_config["environments"]["draft"]
        assert draft_env["kind"] == "api_key", "Directory API connection should use api_key authentication"
        assert draft_env["type"] == "team", "Directory API connection should use team credentials"
        assert draft_env["server_url"] == "http://localhost:8002/", "Directory API connection should point to localhost:8002"
    
    def test_connection_references_in_tools(self):
        """Test that tools properly reference the connections"""
        tool_files = [
            "tools/create_profile_tool.yaml",
            "tools/schedule_meeting_tool.yaml",
            "tools/get_directory_tool.yaml"
        ]
        
        expected_connections = {
            "create_profile_tool": "hr_api_conn",
            "schedule_meeting_tool": "hr_api_conn", 
            "get_directory_tool": "dir_api_conn"
        }
        
        for tool_file in tool_files:
            with open(tool_file, "r") as f:
                tool_config = yaml.safe_load(f)
            
            tool_name = tool_config["name"]
            expected_connection = expected_connections.get(tool_name)
            
            if expected_connection:
                assert "connection" in tool_config, f"Tool {tool_name} should have connection field"
                assert tool_config["connection"] == expected_connection, \
                    f"Tool {tool_name} should reference connection '{expected_connection}', got '{tool_config.get('connection')}'"
    
    def test_connection_app_id_uniqueness(self):
        """Test that connection app_ids are unique"""
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        app_ids = set()
        for conn_file in connection_files:
            with open(conn_file, "r") as f:
                conn_config = yaml.safe_load(f)
            
            app_id = conn_config["app_id"]
            assert app_id not in app_ids, f"Connection app_id '{app_id}' is not unique"
            app_ids.add(app_id)
    
    def test_connection_server_urls_are_valid(self):
        """Test that connection server URLs are valid and accessible"""
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        expected_urls = {
            "hr_api_conn": "http://localhost:8001/",
            "dir_api_conn": "http://localhost:8002/"
        }
        
        for conn_file in connection_files:
            with open(conn_file, "r") as f:
                conn_config = yaml.safe_load(f)
            
            app_id = conn_config["app_id"]
            server_url = conn_config["environments"]["draft"]["server_url"]
            
            assert server_url == expected_urls[app_id], \
                f"Connection {app_id} should have server_url '{expected_urls[app_id]}', got '{server_url}'"
            
            # Validate URL format
            assert server_url.startswith("http://"), f"Server URL should start with http://: {server_url}"
            assert "localhost" in server_url, f"Server URL should contain localhost: {server_url}"
            assert server_url.endswith("/"), f"Server URL should end with /: {server_url}"
    
    def test_connection_compliance_with_ibm_documentation(self):
        """Test that connections fully comply with IBM watsonx Orchestrate ADK documentation"""
        connection_files = [
            "connections/hr_api_connection.yaml",
            "connections/directory_api_connection.yaml"
        ]
        
        for conn_file in connection_files:
            with open(conn_file, "r") as f:
                conn_config = yaml.safe_load(f)
            
            # Verify compliance with IBM documentation requirements
            
            # 1. spec_version must be v1
            assert conn_config["spec_version"] == "v1", "Connection must use spec_version v1"
            
            # 2. kind must be "connection"
            assert conn_config["kind"] == "connection", "Connection kind must be 'connection'"
            
            # 3. app_id must be present and unique
            assert "app_id" in conn_config, "Connection must have app_id field"
            assert len(conn_config["app_id"].strip()) > 0, "Connection app_id cannot be empty"
            
            # 4. environments must be configured
            assert "environments" in conn_config, "Connection must have environments configuration"
            assert len(conn_config["environments"]) > 0, "Connection must have at least one environment"
            
            # 5. Each environment must have required fields
            for env_name, env_config in conn_config["environments"].items():
                # kind must be one of the valid types
                valid_kinds = ["basic", "bearer", "api_key", "oauth_auth_on_behalf_of_flow", "key_value", "kv"]
                assert env_config["kind"] in valid_kinds, f"Environment kind must be one of: {valid_kinds}"
                
                # type must be team or member
                assert env_config["type"] in ["team", "member"], "Environment type must be 'team' or 'member'"
                
                # server_url must be present for OpenAPI and Python tools
                assert "server_url" in env_config, "Environment must have server_url for tool access"
                assert len(env_config["server_url"].strip()) > 0, "Environment server_url cannot be empty" 