import pytest
import json
from macro_convergence_engine import MacroConvergenceEngine
from unittest.mock import MagicMock

def test_macro_convergence_output_structure():
    # Mocking GroundingService behavior
    mock_grounding = MagicMock()
    mock_grounding.query.return_value = {
        "cocktail_name": "Test Crisis",
        "scqa_situation": "Sit",
        "scqa_complication": "Comp",
        "outlook_2026_2027": "Out",
        "strategic_recommendation_geopolitical": "Geo Recommendation",
        "strategic_recommendation_investor": "Investor Recommendation",
        "kilde_url": "http://example.com"
    }
    
    engine = MacroConvergenceEngine(grounding=mock_grounding)
    shocks = [{"commodity": "Oil", "delta_percentage": 50}]
    
    result = engine.analyze_convergence(shocks)
    
    # Verify all required keys are present for v3.1
    assert "strategic_recommendation_geopolitical" in result
    assert "strategic_recommendation_investor" in result
    assert "cocktail_name" in result
    assert "kilde_url" in result
    assert "scqa_situation" in result
