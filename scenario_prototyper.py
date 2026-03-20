import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import DEFAULT_PRO_MODEL

load_dotenv()

class ScenarioEngine:
    """
    Fase 3: Scenario Engine Prototype.
    Beregner 1., 2. og 3. ordens effekter af geopolitiske chok via Search Grounding.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment.")
        
        self.client = genai.Client(api_key=self.api_key)
        # Using Gemini 3.1 Pro via the centralized config
        self.model_id = DEFAULT_PRO_MODEL

    def analyze_scenario(self, event_description):
        prompt = f"""
        Du er en strategisk OSINT analytiker. 
        Analyser følgende hændelse og dens globale, systemiske ringvirkninger ved hjælp af officielle kilder og tænketanke (Search Grounding).
        
        HÆNDELSE: {event_description}
        
        KRAV TIL KILDER:
        1. Brug Google Search Grounding til at finde de mest relevante og opdaterede eksperter/tænketanke.
        2. VIGTIGT: Husk at søge bredt og brug mere end bare kilder fra USA. Inkludér europæiske, asiatiske eller mellemøstlige kilder (f.eks. nationale selskaber eller ministerier), men bevar en kritisk distance til deres politiske natur.
        3. KIG IKKE PÅ YOUTUBE VIDEOER ELLER SOCIALE MEDIER. Brug kun officielle instanser.
        
        Gennemtænk de afledte effekter nøje og strukturer dem stringent.
        
        OUTPUT FORMAT (JSON):
        {{
            "event": "Kort resumé af hændelsen",
            "intelligence_brief": "Et helt kort (2-3 linjer) 'intelligence brief', som indeholder: 1. En introduktion, 2. Et overblik over situationen, 3. Den overordnede konsekvens.",
            "primary_sources": ["Liste af 2-3 primære kilder/tænketanke der blev fundet (husk non-US kilder)"],
            "first_order_effect": {{
                "description": "1. ordens effekt (Direkte påvirkning): Hvem køber råvaren/produktet, og hvordan rammes de lige nu?",
                "evidence": "Bevis/data fundet"
            }},
            "second_order_effect": {{
                "description": "2. ordens effekt (Industriel konsekvens): Hvilken specifik produktion/supply-chain stopper som følge?",
                "evidence": "Bevis/data fundet"
            }},
            "third_order_effect": {{
                "description": "3. ordens effekt (Makro-økonomisk skred): Hvordan rammer dette de bredere globale markeder og vækst?",
                "evidence": "Bevis/data fundet"
            }},
            "strategic_implication": "En konkluderende sætning om den langsigtede strategiske risiko"
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
    engine = ScenarioEngine()
    test_event = "Eksport af helium fra Qatar lukkes 100% og øjeblikkeligt."
    print(f"Beregner scenarie: '{test_event}'...")
    result = engine.analyze_scenario(test_event)
    
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "scenario_prototype_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        
    print("Analyse fuldført! Resultat gemt i data/scenario_prototype_result.json")
    print(json.dumps(result, indent=2, ensure_ascii=False))
