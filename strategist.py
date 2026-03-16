import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class Strategist:
    """
    Fase 4: Strategic Implications Matrix.
    Syntetiserer OSINT-fund til høj-niveau strategiske konsekvenser.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-3.1-pro-preview"

    def analyze(self, scout_results, feed_items, hypothesis):
        """
        Analyzes the connection between raw results and the strategic hypothesis.
        """
        prompt = f"""
        Du er en strategisk rådgiver (Resurf Strategist style). Din opgave er at vurdere sandsynligheden 
        af en specifik strategisk hypotese baseret på friske OSINT-data.
        
        STRATEGISK HYPOTESE:
        {hypothesis}
        
        AKTUELLE OSINT FINDINGS (SCOUT):
        {json.dumps(scout_results, indent=2, ensure_ascii=False)}
        
        LIVE FEED EVENTS:
        {json.dumps(feed_items, indent=2, ensure_ascii=False)}
        
        OPGAVE:
        1. Identificér kausale links mellem fundene (f.eks. TSMC energi -> Nvidia output).
        2. Opstil en 'Strategic Implications Matrix' med binære konsekvenser (Hvis X, så Y).
        3. Giv en samlet sandsynlighedsvurdering (0-100%) for hypotesen.
        4. Hold tonen klinisk, kynisk og uden 'fluff'.
        
        OUTPUT FORMAT (JSON):
        {{
            "matrix": [
                {{
                    "event": "Begivenhed/Trigger",
                    "implication": "Strategisk konsekvens",
                    "risk_level": "Høj|Medium|Lav"
                }}
            ],
            "probability_score": 85,
            "executive_summary": "Kort, præcis opsummering af den strategiske situation.",
            "second_order_effects": ["Effekt 1", "Effekt 2"]
        }}
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": response.text}

if __name__ == "__main__":
    # Test sample with user's actual hypothesis
    DATA_DIR = Path("data")
    scout_file = DATA_DIR / "scout_results.json"
    feed_file = DATA_DIR / "live_feed.json"
    
    scout_data = []
    if scout_file.exists():
        with open(scout_file, "r", encoding="utf-8") as f:
            scout_data = json.load(f)
            
    feed_data = []
    if feed_file.exists():
        with open(feed_file, "r", encoding="utf-8") as f:
            feed_data = json.load(f)
            
    hypothesis = """
    Mangel på elektricitet hos TSMC vil påvirke Nvidia leverancer negativt. 
    Dette vil føre til et fald i Tech/AI handlen og lede til en global recession. 
    Det øger risikoen for at Kina agerer mod USA i Golfen (via Rusland/Iran proxy) 
    mod amerikanske og israelske mål. Ukraine mangler samtidig våben.
    """
    
    strategist = Strategist()
    print("Analyserer strategiske implikationer...")
    analysis = strategist.analyze(scout_data, feed_data, hypothesis)
    
    with open(DATA_DIR / "strategic_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print("Strategisk analyse gemt i data/strategic_analysis.json")
