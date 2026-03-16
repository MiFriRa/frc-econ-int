Kravspecifikation v2.0: Konfigurationsdrevet OSINT-motor  
1\. Formål  
At drive en autonom, bias-fri OSINT-maskine, der både proaktivt overvåger specifikke geopolitiske/økonomiske indikatorer (via et kontrolpanel) og reaktivt udtrækker, verificerer og lagrer nye primærkilder fra ustruktureret globalt medieindhold.  
2\. Arkitektur & Værktøjer  
 \* LLM Motor: Gemini 3.1 Pro via det nye google-genai SDK (inkl. multimodal indtagelse af video/billede/tekst).  
 \* Verifikationslag: Google Search Grounding som indbygget tool for realtidsopslag (dags dato: marts 2026).  
 \* Styring (Konfigurationsdrevet): Python-koden er agnostisk. Al intelligens og overvågning styres via rene JSON-filer (trackers.json og verified\_sources.json).  
 \* Infrastruktur: Modulære Python-funktioner, der kan køres sekventielt som et dagligt cronjob. Output leveres udelukkende i maskinlæsbar JSON.  
3\. Systemets Fire Faser (Pipelinens flow)  
 \* Fase 0: Den Proaktive Scout (Overvågning)  
   \* Input: Læser dynamisk fra trackers.json (f.eks. "Brent-Dubai spread", "TSMC energistatus").  
   \* Handling: Sender isolerede Search Grounding-prompter for hver indikator og evaluerer op mod et defineret alarm\_kriterie.  
   \* Output: Status-alarmer (ALARM / STABIL / MANGLER DATA).  
 \* Fase 1: Støvsugeren (Ingestion & Extraction)  
   \* Input: Ustruktureret medieindhold (YouTube-links, screenshots, X-posts fra f.eks. Al Jazeera, CCTV).  
   \* Handling: Frasorterer journalistisk spin og udtrækker udelukkende de rå data og de påståede primærkilder.  
 \* Fase 2: Sandhedstjekket (Entity Verification)  
   \* Input: JSON-listen med påstande fra Fase 1\.  
   \* Handling: Bruger Search Grounding til at finde den originale afsender.  
   \* Vigtigt: Troværdighed vurderes ud fra entiteten (f.eks. Kinas Toldmyndigheder), ikke platformen eller TLD'et (Telegram og X er gyldige kanaler for officielle udmeldinger).  
 \* Fase 3: Kilde-Ledger (Feedback-loopet)  
   \* Input: Verificerede kilder fra Fase 2\.  
   \* Handling: Tilføjer automatisk nye, bekræftede entiteter til verified\_sources.json, så Fase 0 fremadrettet kan inkludere dem i den proaktive morgenscanning.  
4\. Systemets Begrænsninger (Guardrails)  
 \* Ingen hardkodning: Ny logik, nye kilder eller nye asymmetriske indikatorer tilføjes KUN i JSON-filerne, aldrig i Python-scriptet.  
 \* Nul holdninger: Modellen må under ingen omstændigheder levere politiske analyser eller gætteri. Kun rådata, prisforskelle og direkte citater.  
 \* Ingen vestlig standard-bias: Systemet må ikke nedprioritere en asiatisk eller mellemøstlig datakilde blot fordi den mangler et .gov-domæne eller udgives på ikke-vestlige sociale medier.

Dette blueprint sikrer, at du har en robust, agnostisk motor, der kan vokse uendeligt, uden at koden knækker undervejs.