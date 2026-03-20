import os
import json
import logging
from config import DEFAULT_PRO_MODEL
from grounding_service import GroundingService

class MacroConvergenceEngine:
    """
    Fase 5: 'The Killer Cocktail'.
    Analyserer tidsmæssigt sammenfaldende chok for at identificere aggregerede trusler 
    mod global verdenshandel, forsyningskæder og sikkerhedspolitik i horisonten 2026/2027.
    Brug af SCQA (Situation, Complication, Question, Answer) og top-down Minto-pyramide tænkning.
    """
    def __init__(self, grounding=None):
        self.grounding = grounding or GroundingService()
        self.logger = logging.getLogger(__name__)

    def analyze_convergence(self, shocks: list) -> dict:
        print("\n[Macro Engine] Initialiserer SCQA analyse for krydsende chokbølger...")
        
        # Format the shocks into a readable string
        shock_details = []
        for s in shocks:
            shock_details.append(f"- {s.get('commodity', 'Ukendt')}: Steget {s.get('delta_percentage', 0)}% (Note: {s.get('analysis_note', '')})")
        shock_context = "\n".join(shock_details)

        prompt = f"""Du er en exceptionelt skarp senior intelligence analytiker og partner i et globalt management consulting hus (tænk McKinsey møder CIA).
Dit mindset er 'top-down' (Minto Pyramid Principle) og din kommunikation er ekstremt skarp, uden fyldord.
Du benytter SCQA frameworket (Situation, Complication, Question, Answer) i din tænkning, men outputtet skal være direkte, handlingsanvisende ledelsesinformation.

Vi observerer lige nu en "Killer Cocktail" af samtidige, ekstreme markeds- og udbudschok på følgende råvarer/indikatorer over de seneste 30 dage:

{shock_context}

Din Opgave:
Analyser de synergistiske (*ikke* blot additive) konsekvenser af disse kombikrise-chok. Hvad sker der, når disse systemer fejler *samtidig*?
Ret blikket mod 2026/2027: Hvordan vil dette ændre verdensordenen, global frihandel (eller mangel på samme) og fødevare/energi/tech-sikkerhed to år ude i fremtiden?

ANBEFALINGSSPLIT: Du skal levere to meget forskellige strategiske anbefalinger:
1. National Sikkerhed: Fokus på EU, Danmark og NATO niveau.
2. Aktieinvestor: Fokus på porteføljerisiko og defensive positioner.

Returner et JSON objekt der overholder nedenstående struktur NØJAGTIGT.
Sproget skal være dansk, klinisk, strategisk tungt og præcist.

JSON struktur forventet:
{{
  "cocktail_name": "Et rammende 2-4 ords overskrift for den samlede krise",
  "scqa_situation": "Kort og faktuel opsummering af status quo (Situationen). Max 2 sætninger.",
  "scqa_complication": "Hvorfor er denne kombination af chok så farlig? Hvad er den uforudsete dominoeffekt (Komplikationen)? Max 2 sætninger.",
  "outlook_2026_2027": "Den barske, usminkede horisont for 2026/2027: Hvem vinder, hvem taber? Max 3-4 sætninger.",
  "strategic_recommendation_geopolitical": "Konkret anbefaling til nationale beslutningstagere (EU/NATO).",
  "strategic_recommendation_investor": "Konkret anbefaling til aktieinvestorer.",
  "kilde_url": "URL til den vigtigste kilde der understøtter din analyse"
}}
"""
        return self.grounding.query(prompt, use_search=True)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test simulation
    test_shocks = [
        {"commodity": "Helium", "delta_percentage": 45, "analysis_note": "Massiv forsyningssvigt pga geopolitik."},
        {"commodity": "Svovl", "delta_percentage": 60, "analysis_note": "Eksportstop fra den persiske golf."},
        {"commodity": "LNG", "delta_percentage": 110, "analysis_note": "Hormuz farvandet lukket ned for civil trafik."}
    ]
    engine = MacroConvergenceEngine()
    print(json.dumps(engine.analyze_convergence(test_shocks), indent=2, ensure_ascii=False))
