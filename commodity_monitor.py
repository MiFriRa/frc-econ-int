import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import DEFAULT_PRO_MODEL

load_dotenv()

class CommodityMonitor:
    """
    Fase 1: Commodity Pulse.
    Bruger Gemini Search Grounding til at finde dagspriser og 30-dages historiske priser
    på kritiske råvarer, og lader AI'en foretage en kontekstuel vurdering af, om deltaet udgør et unormalt chok.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = DEFAULT_PRO_MODEL

    def check_commodity_delta(self, commodity_name):
        prompt = f"""
        Du er en klinisk finans- og råvare-analytiker. Dit job er LIGEFREMT at returnere rådata og vurdere statistiske afvigelser.
        
        OPGAVE:
        Brug Google Search Grounding til at undersøge råvaren: {commodity_name}.
        
        TRIN 1: PRISDATA
        Find:
        1. Den aktuelle spotpris i dag.
        2. Prisen for præcis 30 dage siden (1 måned siden).
        Beregn ændringen (delta) i procent.
        
        TRIN 2: DYNAMISK CHOK-VURDERING
        Overvej råvarens normale volatilitet. En ændring på 15% på en måned kan være normalt for naturgas, men ekstremt for kobber.
        Spørg dig selv: "Er en ændring på X% over 30 dage historisk unormalt for netop {commodity_name}?"
        Sæt 'is_shock' til true, HVIS og KUN HVIS ændringen ligger uden for det historiske normal-spektrum for denne specifikke råvare.
        
        OUTPUT FORMAT (JSON):
        {{
            "commodity": "{commodity_name}",
            "current_price_value": <float>,
            "price_30_days_ago_value": <float>,
            "currency_unit": "USD/Barrel, USD/MMBtu etc.",
            "delta_percentage": <float>,
            "sources_used": ["URL 1", "URL 2"],
            "is_shock": <boolean, true if the delta is historically abnormal for THIS specific commodity>,
            "analysis_note": "Kort note (max 2 sætninger) om årsagen til prisændringen, og HVORFOR dette evt. vurderes som et unormalt chok."
        }}
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_mime_type="application/json",
                temperature=0.0
            )
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": response.text}

if __name__ == "__main__":
    monitor = CommodityMonitor()
    
    # Testliste udvidet med både Brent og Platts Dubai som forskellige indikatorer
    commodities_to_check = [
        "Japansk Korea Marker (JKM) LNG spotpris",
        "Brent Crude Oil",
        "Platts Dubai Crude Oil"
    ]
    
    results = []
    
    for commodity in commodities_to_check:
        print(f"Søger efter markedsdata: 30-dages delta for {commodity}...")
        res = monitor.check_commodity_delta(commodity)
        results.append(res)
        print(f"--> Delta fundet: {res.get('delta_percentage', 'N/A')}% (Chok: {res.get('is_shock', False)})")
        print("---")
        
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "commodity_pulse_result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print(f"Data gemt i data/commodity_pulse_result.json")
