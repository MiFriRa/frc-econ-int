import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class Verifier:
    """
    Fase 2: Sandhedstjekket (The Truth Check).
    Verificerer påstande via Search Grounding direkte hos primære entiteter.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-3.1-pro-preview"

    def verify_claim(self, claim):
        """
        Uses Search Grounding to find documentation for a specific claim.
        """
        fact = claim.get("fact")
        entity = claim.get("entity")
        
        prompt = f"""
        Verificér følgende påstand ved at søge direkte efter officielle kilder fra {entity}.
        
        PÅSTAND: {fact}
        
        FIND:
        1. Officielle pressemeddelelser, tolddata, eller ministerielle udmeldinger.
        2. Bekræft eller afkræft om hændelsen har fundet sted.
        3. Find den oprindelige kilde-URL.
        
        OUTPUT FORMAT (JSON):
        {{
            "verification_status": "VERIFIED" | "DEBUNKED" | "UNCONFIRMED",
            "evidence": "Kort beskrivelse af hvad du fandt",
            "source_url": "URL til den primære kilde",
            "confidence": 0.0 - 1.0
        }}
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="application/json"
            )
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": response.text}

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
