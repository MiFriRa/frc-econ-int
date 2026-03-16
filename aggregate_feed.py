import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")

def aggregate_feed():
    feed = []
    
    # Load Ingestion
    ingestion_file = DATA_DIR / "ingestion_test.json"
    if ingestion_file.exists():
        with open(ingestion_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for claim in data.get("claims", []):
                feed.append({
                    "type": "INGESTION",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "title": f"Rådata udvundet: {claim['entity']}",
                    "content": claim['fact'],
                    "priority": claim['priority']
                })
                
    # Load Verification
    verification_file = DATA_DIR / "verification_test.json"
    if verification_file.exists():
        with open(verification_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            feed.append({
                "type": "VERIFICATION",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "title": f"Verifikation afsluttet: {data.get('verification_status')}",
                "content": data.get('evidence'),
                "url": data.get('source_url'),
                "priority": 5 if data.get('verification_status') == 'VERIFIED' else 3
            })
            
    # Sort by priority or timestamp (here just append)
    # In a real app, we'd have timestamps in the files
    
    with open(DATA_DIR / "live_feed.json", "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    aggregate_feed()
