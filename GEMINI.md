# GEMINI.md - Frimer-Rasmussen Consulting OSINT Engine

Velkommen til `frc-econ-int` projektet. Dette dokument er din guide som AI-agent til at forstå arkitekturen og de forventede standarder.

## Projekt Kontekst
Dette er en autonom, konfigurationsdrevet OSINT-motor designet til at overvåge geopolitiske og økonomiske indikatorer (f.eks. Brent-Dubai spread, TSMC energistatus).

## Teknisk Stack
- **Sprog**: Python 3.10+
- **LLM**: Gemini 3.1 Pro (via `google-genai` SDK)
- **Framework**: Konfigurationsdrevet arkitektur (logik i Python, intelligens i JSON)
- **OS**: Windows 11 (PowerShell / WSL2)

## Arkitektur & Design
Vi adskiller **motoren** fra **intelligensen**:
- `trackers.json`: Definition af hvad der skal overvåges.
- `verified_sources.json`: Verificerede kilder.
- **Python Scripts**: Agnostiske funktioner der læser JSON og udfører Search Grounding.

## Windows 11 Udvikling
- Brug altid PowerShell-kompatible kommandoer.
- Vær opmærksom på Windows-stier (brug `pathlib` eller `os.path.join`).
- Lokale virtuelle miljøer ligger typisk i `.venv/`.

## Axiomer (Vores Grundlov)
Alle ændringer skal overholde de globale aksiomer i @[AXIOMS.md](file:///C:/Users/mikke/.gemini/antigravity/rules/AXIOMS.md).
1. **Glæde**: Premium æstetik og UX.
2. **Nytte**: Fokus på høj-impact OSINT data.
3. **Kvalitet**: Robust og ren kode.
4. **Sikkerhed**: Ingen secrets i koden.
5. **Transparens**: Forklar dine beslutninger.
6. **Ansvarlighed**: Tænk langsigtet.
7. **Commander's Intent**: Forstå det strategiske mål bag opgaven.
8. **Kontinuerlig Verifikation**: Test alt.

## Datahåndtering
- Rådata fra kilder gemmes i `data/` mappen.
- `data/` er ignoreret i git for at undgå clutter og bias i kildehistorikken.
