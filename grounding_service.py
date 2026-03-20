import os
import json
import logging
from google import genai
from google.genai import types
from config import DEFAULT_PRO_MODEL

class GroundingService:
    """
    Centralized service for Google Search Grounding across all OSINT phases.
    Ensures consistent JSON extraction and error handling.
    """
    def __init__(self, api_key=None, model_id=DEFAULT_PRO_MODEL):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment.")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = model_id
        self.logger = logging.getLogger(__name__)

    def query(self, prompt: str, system_instruction: str = None, use_search: bool = True) -> dict:
        """
        Executes a grounded search query and returns structured JSON.
        """
        config_args = {
            "response_mime_type": "application/json"
        }
        if system_instruction:
            config_args["system_instruction"] = system_instruction
        if use_search:
            config_args["tools"] = [types.Tool(google_search=types.GoogleSearch())]

        config = types.GenerateContentConfig(**config_args)

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
            
            raw_text = response.text.strip()
            # Robust JSON cleaning
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "", 1).replace("```", "", 1).strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.replace("```", "", 1).replace("```", "", 1).strip()

            data = json.loads(raw_text)
            
            # Ensure we returning a dict if it's a list
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return data

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON Decode Error: {e}. Raw text: {response.text}")
            return {"error": "Invalid JSON response from model", "raw": response.text}
        except Exception as e:
            self.logger.error(f"Grounding Error: {e}")
            return {"error": str(e)}
