from datetime import date
from nih_grant_matcher.models import Opportunity
from nih_grant_matcher.scoring import MLRelevanceScorer

def test_ml_opportunity_scores_high() -> None:
    opportunity = Opportunity(source_id="1", opportunity_number="RFA-TEST-1", title="Deep learning for clinical prediction from EHR data", agency_code="HHS-NIH11", agency_name="National Institutes of Health", status="posted", close_date=date(2026, 12, 1), description="This NOFO supports machine learning and predictive modeling for patient outcomes.")
    scored = MLRelevanceScorer().score(opportunity, today=date(2026, 7, 6))
    assert scored.score >= 70
    assert scored.classification == "High"
    assert "machine learning" in scored.matched_terms

def test_generic_biomedical_opportunity_stays_low() -> None:
    opportunity = Opportunity(source_id="2", opportunity_number="PAR-TEST-2", title="Community health implementation research", agency_code="HHS-NIH11", agency_name="National Institutes of Health", status="posted", close_date=date(2026, 12, 1), description="Supports prevention, capacity building, health disparities, and clinical trial readiness.")
    scored = MLRelevanceScorer().score(opportunity, today=date(2026, 7, 6))
    assert scored.score < 45
    assert scored.classification == "Watchlist"
