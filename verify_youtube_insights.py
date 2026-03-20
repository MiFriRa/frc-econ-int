import json
from pathlib import Path
from verification import Verifier

def bridge_youtube_to_verification():
    print("--- FRC OSINT Engine: YouTube Verification Bridge Starter ---\n")
    
    insights_path = Path("data/youtube_insights.json")
    if not insights_path.exists():
        print("[ERROR] Ingen youtube_insights.json fundet. Kør youtube_scout.py først.")
        return

    with open(insights_path, "r", encoding="utf-8") as f:
        insights = json.load(f)

    # Saml alle unikke trackers
    all_trackers = set()
    for item in insights:
        for tracker in item.get("potential_trackers", []):
            all_trackers.add(tracker)

    output_path = Path("data/scout_verification_results.json")
    verified_results = []
    processed_trackers = set()

    # Load eksisterende resultater
    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                verified_results = json.load(f)
                processed_trackers = {res.get("tracker_name") for res in verified_results}
                print(f"[INFO] Fandt {len(processed_trackers)} allerede verificerede kilder. Springer dem over.")
        except Exception as e:
            print(f"[WARNING] Kunne ikke læse eksisterende resultater: {e}")

    new_trackers = [t for t in sorted(list(all_trackers)) if t not in processed_trackers]
    print(f"[INFO] Mangler at verificere {len(new_trackers)} ud af {len(all_trackers)} kilder.\n")
    
    verifier = Verifier()

    for tracker in new_trackers:
        print(f"-> Verificerer kilde hos: {tracker}...")
        
        claim = {
            "entity": tracker,
            "fact": f"Søg efter nylige (2025-2026) officielle rapporter, hvidbøger eller kritiske udmeldinger fra {tracker} vedrørende globale forsyningskæder, halvledere eller geopolitik."
        }
        
        try:
            result = verifier.verify_claim(claim)
            result["tracker_name"] = tracker
            verified_results.append(result)
            
            print(f"   [STATUS]: {result.get('verification_status')}")
            
            # Gem efter hver kilde
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(verified_results, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"   [ERROR] Fejl under verificering af {tracker}: {e}")

    print(f"\n--- Verificering fuldført. Alle resultater i {output_path} ---")

if __name__ == "__main__":
    bridge_youtube_to_verification()
