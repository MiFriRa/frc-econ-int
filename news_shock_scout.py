import os
import json
from google import genai
from google.genai import types
from datetime import datetime

from config import DEFAULT_PRO_MODEL

class NewsShockScout:
    """
    Fase 0: Proactive Intelligence.
    Søger automatisk globale nyhedsstrømme for at identificere uventede 
    geopolitiske eller makroøkonomiske chok, som vi ikke overvåger i forvejen.
    Udvinder kernekilder og omdanner dem til strukturerede 'chok-signaler'.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY er ikke sat.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = DEFAULT_PRO_MODEL 

    def scan_news_for_shocks(self) -> list:
        print("\n[News Scout] Scanner globale markeder for uventede 'Black Swan' hændelser (seneste 24-48 timer)...")
        
        prompt = f"""Klokken er nu {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Du er en top-tier OSINT analytiker.
Brug Search Grounding til at scanne den globale nyhedsstrøm (især uden for USA) inden for de seneste 24-48 timer for at identificere 1-2 voldsomme nye økonomiske, forsyningsmæssige eller geopolitiske chok (Black Swans, ekstrem mangel, pludselige krigshandlinger mod infrastruktur, pris-chok).

Din Opgave:
1. Kondensér nyhedsstrømmen ned til de absolutte kernekilder.
2. Udtræk den præcise information og analyser chokkets umiddelbare effekt.
3. Formidl det klart og klinisk i et JSON array, der kan parses af vores maskine.

FORMAT:
[
  {{
    "commodity": "Kort navn på emnet/råvaren (f.eks. 'Taiwan Semiconductors' eller 'Uran')",
    "analysis_note": "Klar formidling af chokket, årsagen dertil og kernekilden der bekræfter det.",
    "delta_percentage": 100, // Et løst estimat af hvor 'farligt' det er på en skala fra 1-100 (100 = maksimalt kritisk chok)
    "is_shock": true, // Altid true for disse alerts
    "sources_used": ["URL 1", "URL 2"]
  }}
]

Returner KUN det rene, udledte JSON array. Ingen markdown ticks i starten og slutningen hvis muligt, ellers ignoreres de. 
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.4, 
                    tools=[{"google_search": {}}]
                )
            )
            
            # The prompt requested JSON Array format which aligns perfectly with Phase 1's format!
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            print(f"[FEJL i News Scout] {e}")
            return []

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    scout = NewsShockScout()
    shocks = scout.scan_news_for_shocks()
    print(json.dumps(shocks, indent=2, ensure_ascii=False))
