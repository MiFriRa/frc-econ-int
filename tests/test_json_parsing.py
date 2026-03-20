import pytest
import json
from grounding_service import GroundingService
from unittest.mock import MagicMock

def test_json_cleaning():
    # Mocking the client to return markdown-wrapped JSON
    service = GroundingService(api_key="fake_key")
    service.client = MagicMock()
    
    # Simulate a response with markdown triple backticks
    mock_response = MagicMock()
    mock_response.text = '```json\n{"status": "ALARM", "observation": "Test"}\n```'
    service.client.models.generate_content.return_value = mock_response
    
    result = service.query("test prompt", use_search=False)
    assert result["status"] == "ALARM"
    assert result["observation"] == "Test"

def test_json_list_handling():
    service = GroundingService(api_key="fake_key")
    service.client = MagicMock()
    
    # Simulate a response that is a list of one object
    mock_response = MagicMock()
    mock_response.text = '[{"status": "STABIL"}]'
    service.client.models.generate_content.return_value = mock_response
    
    result = service.query("test prompt", use_search=False)
    assert isinstance(result, dict)
    assert result["status"] == "STABIL"

def test_invalid_json_handling():
    service = GroundingService(api_key="fake_key")
    service.client = MagicMock()
    
    # Simulate a non-JSON response
    mock_response = MagicMock()
    mock_response.text = 'This is not JSON'
    service.client.models.generate_content.return_value = mock_response
    
    result = service.query("test prompt", use_search=False)
    assert "error" in result
    assert result["raw"] == 'This is not JSON'
