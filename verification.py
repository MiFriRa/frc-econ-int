import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv
from grounding_service import GroundingService

from config import DEFAULT_PRO_MODEL

load_dotenv()

class VerificationEngine:
    """
    Fase 2: Sandhedstjekket (The Truth Check).
    Verificerer påstande via Search Grounding direkte hos primære entiteter.
    """
    def __init__(self, grounding=None):
        self.grounding = grounding or GroundingService()

    def verify_claim(self, claim):
        """
        Uses Search Grounding to find documentation for a specific claim.
        """
        fact = claim.get("fact")
        entity = claim.get("entity")
        
        return self.grounding.query(prompt)

if __name__ == "__main__":
    # Test with result from ingestion_test.json
    DATA_DIR = Path("data")
    if (DATA_DIR / "ingestion_test.json").exists():
        with open(DATA_DIR / "ingestion_test.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            claims = data.get("claims", [])
            
            if claims:
                verifier = Verifier()
                print(f"Verificerer: {claims[0]['fact']}")
                result = verifier.verify_claim(claims[0])
                print(json.dumps(result, indent=2, ensure_ascii=False))
                
                with open(DATA_DIR / "verification_test.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
