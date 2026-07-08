from datetime import date

from nih_grant_matcher.filters import is_current_nih_hhs_opportunity
from nih_grant_matcher.normalizer import normalize_nih_guide
from nih_grant_matcher.scoring import MLRelevanceScorer


def test_nih_guide_primed_ai_normalizes_and_scores() -> None:
    item = {
        "rowid": "43008",
        "type": "active",
        "title": "Logistics Center for Precision Medicine with AI: Integrating Imaging with Multimodal Data (PRIMED-AI) (U24 Clinical Trials Not Allowed)",
        "docnum": "RFA-RM-27-015",
        "parentIC": "NIH",
        "primaryIC": "RMOD",
        "reldate": "2026-06-30T00:00:00.000Z",
        "expdate": "2026-10-03T00:00:00.000Z",
        "opendate": "2026-09-02T00:00:00.000Z",
        "doctype": "RFA",
        "ac": ["U24"],
        "purpose": "The PRIMED-AI Program will support AI-based clinical decision support tools integrating imaging with multimodal data.",
        "ggid": "360543",
    }

    opportunity = normalize_nih_guide(item)
    scored = MLRelevanceScorer().score(opportunity, today=date(2026, 7, 7))

    assert opportunity.source_id == "nih-guide:43008"
    assert opportunity.agency_code == "RMOD"
    assert opportunity.close_date == date(2026, 10, 3)
    assert is_current_nih_hhs_opportunity(opportunity, today=date(2026, 7, 7))
    assert "AI" in scored.matched_terms
    assert scored.score >= 45


def test_nih_guide_url_uses_notice_folder() -> None:
    opportunity = normalize_nih_guide({"rowid": "1", "docnum": "NOT-OD-26-001", "title": "Notice", "type": "notices"})
    assert "/notice-files/NOT-OD-26-001.html" in opportunity.source_url

