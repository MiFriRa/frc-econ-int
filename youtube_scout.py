import os
import json
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import DEFAULT_FLASH_LITE_MODEL

load_dotenv()

# Initialize Gemini Client
client = genai.Client()
MODEL_NAME = DEFAULT_FLASH_LITE_MODEL

def analyze_youtube_video(url):
    """Analyserer en YouTube-video direkte med Gemini 3.1 Flash Lite."""
    
    system_instruction = """
    Du er en ultra-præcis OSINT-analytiker for Frimer-Rasmussen Consulting (Resurf-Journalist stil).
    Din opgave er at levere 'Bottom Line Up Front' (BLUF) baseret på indholdet i den angivne YouTube-video.
    
    REGLER:
    1. Tonen er KLINISK, NEUTRAL og OBJEKTIV. Ingen hype, ingen "røgslør" eller "sandkasse" retorik.
    2. Identificér konkrete geopolitiske, økonomiske eller forsyningskædemæssige point.
    3. Træk alle specifikke rapporter, organisationer, tænketanke, databaser eller nye kilder ud, der nævnes som reference.
    
    OUTPUT FORMAT (STRENGT JSON):
    {
        "url": "Indsæt videoens URL",
        "bluf": "Kort, præcis opsummering af kernepointerne (maks 3-4 sætninger).",
        "potential_trackers": [
            "Ny organisation nævnt",
            "Specifik rapport nævnt",
            "Datasæt refereret"
        ]
    }
    """
    
    prompt = f"Gennemgå indholdet af denne YouTube-video og træk de vigtigste geopolitiske/økonomiske pointer ud ifølge instruktionerne.\n\nVideo URL: {url}"
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        temperature=0.0 # Strict output
    )
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config
        )
        
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1).replace("```", "", 1).strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "", 1).replace("```", "", 1).strip()
            
        return json.loads(raw_text)
    except Exception as e:
        print(f"[ERROR] Gemini analyse fejlede for URL {url}: {e}")
        return {
            "url": url,
            "bluf": "Analyse fejlede.",
            "potential_trackers": []
        }

def run_youtube_scout(urls):
    print("--- FRC OSINT Engine: YouTube Scout (Direct Integration) Starter ---\n")
    
    output_path = Path("data/youtube_insights.json")
    output_path.parent.mkdir(exist_ok=True)
    
    # Load eksisterende resultater
    results = []
    processed_urls = set()
    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                results = json.load(f)
                processed_urls = {item.get("url") for item in results if item.get("url")}
                print(f"[INFO] Fandt {len(processed_urls)} allerede analyserede videoer. Springer dem over.\n")
        except Exception as e:
            print(f"[WARNING] Kunne ikke læse eksisterende fil: {e}. Starter forfra.")

    new_count = 0
    for url in urls:
        if url in processed_urls:
            continue
            
        print(f"-> Analyserer video via Gemini: {url}...")
        
        analysis = analyze_youtube_video(url)
        results.append(analysis)
        processed_urls.add(url)
        new_count += 1
        
        print(f"   [BLUF]: {analysis.get('bluf')}")
        trackers = analysis.get("potential_trackers", [])
        if trackers:
            print(f"   [POTENTIELLE KILDER/TRACKERS]: {', '.join(trackers)}\n")
        else:
            print("   [Ingen specifikke nye kilder fundet]\n")
            
        # Gem efter hver video for at undgå datatab ved frys
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
    if new_count == 0:
        print("--- Ingen nye videoer at analysere. Alt er up-to-date. ---")
    else:
        print(f"--- Scouting fuldført. {new_count} nye resultater gemt i {output_path} ---")
    
    return results

if __name__ == "__main__":
    # Liste over videoer at overvåge
    test_urls = [
        "https://youtu.be/FyVpj9SmXIA?is=YmGlfIeHaaDrSuem",
        "https://youtu.be/zPiBYdpd1-8?is=RCbbY65TS4FcEn_P",
        "https://youtu.be/NUDk2p4hJDI?is=SRinroyDfDYG2cZG",
        "https://youtu.be/pd8-Loxu3DQ?is=Ofj0BvICMGXVYb1N",
        "https://youtu.be/aZDgnfCngWk?is=co9IoboM2BSEbxxC",
        "https://youtu.be/rN_K3p_022g?is=mYm6H_V6L8h_W3jA" # Ny video test
    ]
    run_youtube_scout(test_urls)
