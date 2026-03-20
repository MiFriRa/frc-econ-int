Kravspecifikation v3.1: Strategisk Beslutnings-Motor (Swiss Style)

1. Formål
At drive en autonom, bias-fri OSINT-maskine, der omdanner rå markedsdata til strategiske beslutningsgrundlag. Systemet prioriterer nu "Top-Down Thinking" (Beslutning -> Kontekst -> Evidens) og leverer differentierede anbefalinger til både geopolitiske og finansielle beslutningstagere.

Intention (løst beskrevet)
Med det nuværende dashboard får jeg et opsummeret overblik over vigtige strategiske oplysninger. Det er godt med de seriøse kilder.

Jeg savner dels realtime information. Krigen mod Iran påvirker alle global samhandel allerede nu tre uger inde i krigen.
Eksempler på centrale råvarer: Hvad koster Brent, Platt fra golfen, LNG fra golfen, helium fra golden og andre centrale råvarer. Store udsving er vigtige. F.eks. steg LNG med 24% på en gang i denne uge(!)

Eksempler der er vigtige (bare i denne uge).
LNG fra Qatar (20-30% af global produktion er lukket ned (vil påvirke Taiwan semi-produktion)
Eksport af svovl fra den Persiske Golf til Kina er lukket ned (vil påvirke Kina kunstgødning produktion
Eksport af helium fra Qater er lukket ned (vil påvirke global semi-produktion)

Jeg tror at det jeg savner er en ramme for forklaringer. Store udsving i råvarepriser vil påvirke hvad direkte hvor hurtigt og i hvilket omfang. Og hvilke effekter opstår der i først, anden og tredje orden.

Eksempel: LNG fra Qatar stopper 100%. Det påvirker 20-30% af den globale produktion, herunder Taiwan energiforsyning. Taiwan har energi til 7-11 dage i lagre og er afhængge af løbende forsyninger. TSMC bruger 10% af Taiwans strøm. Uden TSMC ingen økonomi i Taiwan. Uden TSMC ingen semi-produktion af AI-chips. Det påvirker hele USA it-service økonomi, som bliver forsinket i sin udbygning. Det er den eneste sektor i vækst i USA. Derfor vil USA gå ind i en recession.

# Opgave.
Jeg har behov for en gennemtænkt plan for *hvordan* er sådan overblik kan skabes. Samtidig ved jeg ikke særligt meget om disse sammenhænge, så servicen skal kunne pege (gennem officielle kilder) hvad de forventede effekter er.
Jeg ved der er masser af dygtige eksperter som udgiver officielle og gratis analyser. Udfordringen er at jeg heller ikke kender kilderne eller eksperterne.
Så med udgangspunkt i udsving i råvarepriser og globale nyheder, skal jeg have en service, som kan hjælpe mig med at tænke på fremtidige scenarier: hvor bevæger verden sig hen?

2. Arkitektur & Værktøjer
 * LLM Motor: Gemini 3.1 Pro via det nye google-genai SDK (inkl. multimodal indtagelse af video/billede/tekst).
 * Verifikationslag: Google Search Grounding som indbygget tool for realtidsopslag (dags dato: marts 2026).
 * Styring (Konfigurationsdrevet): Python-koden er agnostisk. Al intelligens og overvågning styres via rene JSON-filer (trackers.json og verified_sources.json).
 * Infrastruktur: Modulære Python-funktioner, der kan køres sekventielt som et dagligt cronjob. Output leveres udelukkende i maskinlæsbar JSON.

3. Systemets Fire Faser (Pipelinens flow)
 * Fase 0: Den Proaktive Scout (Overvågning)
   * Input: Læser dynamisk fra trackers.json (f.eks. "Brent-Dubai spread", "TSMC energistatus").
   * Handling: Sender isolerede Search Grounding-prompter for hver indikator og evaluerer op mod et defineret alarm_kriterie.
   * Output: Status-alarmer (ALARM / STABIL / MANGLER DATA).
 * Fase 1: Støvsugeren (Ingestion & Extraction)
   * Input: Ustruktureret medieindhold (YouTube-links, screenshots, X-posts fra f.eks. Al Jazeera, CCTV).
   * Handling: Frasorterer journalistisk spin og udtrækker udelukkende de rå data og de påståede primærkilder.
 * Fase 2: Sandhedstjekket (Entity Verification)
   * Input: JSON-listen med påstande fra Fase 1.
   * Handling: Bruger Search Grounding til at finde den originale afsender.
   * Vigtigt: Troværdighed vurderes ud fra entiteten (f.eks. Kinas Toldmyndigheder), ikke platformen eller TLD'et (Telegram og X er gyldige kanaler for officielle udmeldinger).
 * Fase 3: Kilde-Ledger (Feedback-loopet)
   * Input: Verificerede kilder fra Fase 2.
   * Handling: Tilføjer automatisk nye, bekræftede entiteter til verified_sources.json.
 * Fase 4: Strategisk Formidling (Executive Layer)
   * Handling: Genererer et klinisk, "Swiss Style" dashboard og PDF-rapporter.
   * Feature: Dual-Track anbefalinger (National Sikkerhed vs. Investor).
   * Feature: Fuld Data-Provenance (Verification Timestamps og Kilde-URL'er).

4. Systemets Begrænsninger (Guardrails)
 * Ingen hardkodning: Ny logik, nye kilder eller nye asymmetriske indikatorer tilføjes KUN i JSON-filerne, aldrig i Python-scriptet.
 * Nul holdninger: Modellen må under ingen omstændigheder levere politiske analyser eller gætteri. Kun rådata, prisforskelle og direkte citater.
 * Ingen vestlig standard-bias: Systemet må ikke nedprioritere en asiatisk eller mellemøstlig datakilde blot fordi den mangler et .gov-domæne eller udgives på ikke-vestlige sociale medier.

Dette blueprint sikrer, at du har en robust, agnostisk motor, der kan vokse uendeligt, uden at koden knækker undervejs.