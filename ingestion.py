import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class IngestionEngine:
    """
    Ansvarlig for "The Vacuum": At samle ustruktureret information.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment or passed to constructor.")
        
        self.client = genai.Client(api_key=self.api_key)
        # In March 2026, we use the centralized PRO model for best reasoning
        self.model_id = DEFAULT_PRO_MODEL

    def vacuum(self, raw_text):
        """
        Processes unstructured text to extract hard facts and claimed sources.
        """
        prompt = f"""
        Du er en kynisk OSINT-analytiker. Din opgave er at 'støvsuge' den følgende tekst for rådata og påståede kilder.
        
        REGLER:
        1. Strip alt journalistisk spin, adjektiver og følelser.
        2. Identificér konkrete påstande (tal, begivenheder, datoer).
        3. Identificér hvem der påstås at være kilden til dataene.
        4. Hvis der nævnes en primær entitet (f.eks. et ministerium eller en virksomhed), så notér det.
        
        OUTPUT FORMAT (JSON):
        {{
            "claims": [
                {{
                    "fact": "Beskrivelse af det hårde faktum",
                    "claimed_source": "Hvem påstås at have sagt det?",
                    "entity": "Den underliggende organisation/myndighed",
                    "priority": 1-5 (5 er højest)
                }}
            ],
            "metadata": {{
                "context": "Kort opsummering af emnet"
            }}
        }}

        TEKST:
        {raw_text}
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
            return {{"error": "Failed to parse JSON from model", "raw": response.text}}

if __name__ == "__main__":
    # Test sample
    test_text = """
    Rygterne svirrer i Taipei, men nu bekræfter anonyme kilder i det taiwanske økonomiministerium, 
    at man i al hemmelighed har bedt TSMC om at reducere strømforbruget med 15% i de kommende to uger. 
    Det sker efter at en LNG-tanker blev tvunget til at vende om i Det Sydkinesiske Hav i går.
    Analytikere frygter at dette blot er toppen af isbjerget.
    """
    
    ingestor = Ingestor()
    results = ingestor.vacuum(test_text)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save test results to data
    DATA_DIR = Path("data")
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_DIR / "ingestion_test.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
