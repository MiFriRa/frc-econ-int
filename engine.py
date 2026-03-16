import os
import json
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ingestion import Ingestor
from verification import Verifier

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client()
MODEL_NAME = "gemini-3.1-pro-preview" 

def load_json_file(filepath: Path) -> list:
    """Universel funktion til at indlæse trackers og kilder."""
    if not filepath.exists():
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Fejl: Kunne ikke læse {filepath}. Sørg for at det er gyldig JSON.")
            return []

class LiveFeedLogger:
    def __init__(self, filename="data/live_feed.json"):
        self.path = Path(filename)
        self.path.parent.mkdir(exist_ok=True)
        if not self.path.exists():
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def log(self, event_type, title, content):
        feed = load_json_file(self.path)
        event = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "type": event_type,
            "title": title,
            "content": content
        }
        feed.insert(0, event)
        # Keep only last 20 events
        feed = feed[:20]
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(feed, f, indent=2, ensure_ascii=False)
        print(f"[{event_type}] {title}: {content}")

def run_full_pipeline(trackers_file: str = "trackers.json"):
    """
    Den fulde FRC OSINT pipeline: Scout -> Vacuum -> Truth Check.
    """
    logger = LiveFeedLogger()
    logger.log("SYSTEM", "Pipeline startet", "Starter fuld OSINT-proces.")
    
    trackers_path = Path(trackers_file)
    trackers = load_json_file(trackers_path)
    
    if not trackers:
        logger.log("ERROR", "Ingen trackers", "Tilføj opgaver til trackers.json.")
        return []

    ingestor = Ingestor()
    verifier = Verifier()
    final_results = []
    
    for tracker in trackers:
        logger.log("SCOUT", f"Overvåger {tracker['id']}", f"Scanner {', '.join(tracker['kilder'])}")
        
        # 1. SCOUT PHASE
        system_instruction = f"""
        Du er en kynisk OSINT-analytiker. 
        Tjek dags dato ({os.getenv('CURRENT_DATE', 'marts 2026')}).
        Mål: {tracker['beskrivelse']}
        Alarmkriterie: {tracker['alarm_kriterier']}
        """
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            tools=[{"google_search": {}}] 
        )
        
        prompt = f"Hent status for {tracker['id']}. Vurder mod: {tracker['alarm_kriterier']}. Returner JSON med tracker_id, status, aktuel_data, kilde_url, observation."
        
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=config
            )
            
            raw_text = response.text.strip()
            # Clean up potential markdown formatting if model ignores mime type
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "", 1).replace("```", "", 1).strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.replace("```", "", 1).replace("```", "", 1).strip()

            scout_data = json.loads(raw_text)
            
            # Handle list response if it happens
            if isinstance(scout_data, list) and len(scout_data) > 0:
                scout_data = scout_data[0]
            
            if scout_data.get('status') == 'ALARM':
                logger.log("ALARM", f"Kritisk fund i {tracker['id']}", scout_data.get('observation'))
                
                # 2. VACUUM PHASE
                logger.log("VACUUM", "Udtrækker påstande", f"Analyserer data fra {scout_data.get('kilde_url')}")
                extracted = ingestor.vacuum(scout_data.get('aktuel_data'))
                
                # 3. TRUTH CHECK PHASE
                verified_claims = []
                for claim in extracted.get("claims", []):
                    if claim.get("priority", 0) >= 4:
                        logger.log("VERIFY", "Verificerer påstand", claim.get("fact"))
                        v_result = verifier.verify_claim(claim)
                        verified_claims.append(v_result)
                        
                        v_status = v_result.get("verification_status")
                        if v_status == "DEBUNKED":
                            logger.log("DEBUNKED", "Påstand afkræftet", v_result.get("evidence"))
                            scout_data["status"] = "STABIL"
                            scout_data["observation"] += f" [DEBUNKED: {v_result.get('evidence')}]"
                        elif v_status == "VERIFIED":
                            logger.log("CONFIRMED", "Påstand bekræftet", v_result.get("evidence"))
                
                scout_data["verified_claims"] = verified_claims
            
            final_results.append(scout_data)
            
        except Exception as e:
            logger.log("ERROR", f"Fejl i {tracker['id']}", str(e))

    logger.log("SYSTEM", "Pipeline fuldført", f"Behandlede {len(trackers)} trackers.")
    return final_results

def save_results(results: list, filename: str = "data/scout_results.json"):
    """Gemmer resultaterne i en fil i data/ mappen."""
    output_path = Path(filename)
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Resultater gemt i {output_path}")

if __name__ == "__main__":
    print("--- FRC OSINT Engine: Fuld Pipeline startet ---\n")
    results = run_full_pipeline()
    if results:
        save_results(results)
    print("\n--- Scanning fuldført ---")
