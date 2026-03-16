import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SOURCES_FILE = BASE_DIR / "verified_sources.json"
VERIFICATION_RESULTS = DATA_DIR / "verification_test.json"
INGESTION_RESULTS = DATA_DIR / "ingestion_test.json"

def update_sources():
    if not SOURCES_FILE.exists() or not VERIFICATION_RESULTS.exists() or not INGESTION_RESULTS.exists():
        print("Missing files for source update.")
        return

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = json.load(f)

    with open(VERIFICATION_RESULTS, "r", encoding="utf-8") as f:
        v_result = json.load(f)

    with open(INGESTION_RESULTS, "r", encoding="utf-8") as f:
        i_result = json.load(f)

    # Simple logic: If a claim was debunked, decrease reliability of the claimed source
    # If verified, increase reliability (up to 1.0)
    status = v_result.get("verification_status")
    
    # Map ingestion claims to sources
    for claim in i_result.get("claims", []):
        source_name = claim.get("claimed_source")
        if not source_name:
            continue
            
        # Check if source exists in ledger
        existing_source = next((s for s in sources if s["entitet"].lower() == source_name.lower()), None)
        
        if existing_source:
            current_reliability = existing_source.get("pålidelighed", 0.5)
            if status == "VERIFIED":
                 existing_source["pålidelighed"] = min(1.0, round(current_reliability + 0.05, 2))
            elif status == "DEBUNKED":
                 existing_source["pålidelighed"] = max(0.0, round(current_reliability - 0.1, 2))
        else:
            # Add new source with initial reliability
            reliability = 0.5
            if status == "VERIFIED": reliability = 0.55
            elif status == "DEBUNKED": reliability = 0.4
            
            sources.append({
                "entitet": source_name,
                "type": "Extract",
                "status": "Auto-discov",
                "pålidelighed": reliability
            })

    # Save updated ledger
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)
    
    print("Source ledger updated successfully.")

if __name__ == "__main__":
    update_sources()
