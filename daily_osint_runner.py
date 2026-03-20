import os
import json
from datetime import datetime
from pathlib import Path

# Import the phases
from news_shock_scout import NewsShockScout
from commodity_monitor import CommodityMonitor
from scenario_prototyper import ScenarioEngine
from macro_convergence_engine import MacroConvergenceEngine

class DailyOsintRunner:
    """
    Master Orchestrator for the OSINT Engine.
    Kører Fase 0 (News Scout) for at finde sorte svaner.
    Kører Fase 1 (Pulse) og trigger automatisk Fase 3 (Scenario) hvis et chok detekteres.
    Kører Fase 5 (Macro Convergence) hvis to eller flere chok detekteres!
    """
    def __init__(self):
        self.news_scout = NewsShockScout()
        self.pulse_monitor = CommodityMonitor()
        self.scenario_engine = ScenarioEngine()
        self.macro_engine = MacroConvergenceEngine()
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.commodities = [
            "Japansk Korea Marker (JKM) LNG spotpris",
            "Brent Crude Oil",
            "Platts Dubai Crude Oil",
            "Helium spotpris",
            "Svovl eksportpris fra den persiske golf"
        ]

    def run(self):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starter Daglig OSINT Engine...")
        
        daily_report = {
            "timestamp": datetime.now().isoformat(),
            "pulse_checks": [],
            "scenario_analyses": [],
            "macro_convergence": None
        }
        
        active_shocks = []
        
        # 0. Kør Fase 0: News Shock Scout
        print(f"\n[Fase 0] Søger live efter udokumenterede Black Swan hændelser...")
        news_shocks = self.news_scout.scan_news_for_shocks()
        if news_shocks:
            print(f"  -> Fandt {len(news_shocks)} ulmende chok i globale nyhedsstrømme!")
            for ns in news_shocks:
                daily_report["pulse_checks"].append(ns)
                active_shocks.append(ns)
                
                # Immediately execute Phase 3 for this shock
                c_name = ns.get("commodity", "Ukendt makro-chok")
                e_desc = f"Nyhedsudbrud ({c_name}): {ns.get('analysis_note', '')}"
                print(f"[Fase 3] ALERT! Eksekverer strategisk scenario-analyse for {c_name}...")
                
                scenario_result = self.scenario_engine.analyze_scenario(e_desc)
                scenario_result["trigger_commodity"] = c_name
                daily_report["scenario_analyses"].append(scenario_result)
                print(f"  -> Scenario analyse fuldført.")
        else:
            print(f"  -> Ingen Black Swans detekteret i det generelle nyhedsbillede.")

        # 1. Kør Fase 1: Commodity Pulse
        for commodity in self.commodities:
            print(f"\n[Fase 1] Overvåger: {commodity}")
            pulse_result = self.pulse_monitor.check_commodity_delta(commodity)
            daily_report["pulse_checks"].append(pulse_result)
            
            is_shock = pulse_result.get("is_shock", False)
            delta = pulse_result.get("delta_percentage", 0)
            note = pulse_result.get("analysis_note", "")
            
            print(f"  -> Delta: {delta}% | Chok: {is_shock}")
            
            # 2. Hvis der er et chok, kør Fase 3: Scenario Engine
            if is_shock:
                event_desc = f"Råvaren '{commodity}' har netop oplevet et historisk unormalt pris-chok på {delta}% over 30 dage. Årsagsvurdering (hvis kendt): {note}"
                print(f"[Fase 3] ALERT! Eksekverer strategisk scenario-analyse for {commodity}...")
                
                scenario_result = self.scenario_engine.analyze_scenario(event_desc)
                scenario_result["trigger_commodity"] = commodity
                daily_report["scenario_analyses"].append(scenario_result)
                print(f"  -> Scenario analyse fuldført.")
                
                active_shocks.append(pulse_result)
            else:
                print(f"  -> Ingen unormale markedsbevægelser registreret (business as usual).")
                
        # 2.5 Kør Fase 5: Macro Convergence ("The Killer Cocktail")
        if len(active_shocks) >= 2:
            print(f"\n[Fase 5] CRITICAL ALERT! {len(active_shocks)} samtidige chok detekteret. Genererer 'Killer Cocktail' Makro-Analyse...")
            macro_result = self.macro_engine.analyze_convergence(active_shocks)
            daily_report["macro_convergence"] = macro_result
            print(f"  -> Makro-Analyse fuldført.")
                
        # 3. Gem det aggregerede output
        output_file = self.data_dir / "daily_osint_report.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(daily_report, f, indent=2, ensure_ascii=False)
            
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Daglig OSINT Engine gennemført succesfuldt. Rapporten er gemt i {output_file}")


if __name__ == "__main__":
    runner = DailyOsintRunner()
    runner.run()
