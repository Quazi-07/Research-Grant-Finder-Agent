from datetime import date
from nih_grant_matcher.models import Opportunity
from nih_grant_matcher.scoring import MLRelevanceScorer
from nih_grant_matcher.store import OpportunityStore

def test_store_upserts_and_reads_scored_opportunity(tmp_path) -> None:
    store = OpportunityStore(tmp_path / "grants.sqlite3")
    opportunity = Opportunity(source_id="abc", opportunity_number="RFA-ABC", title="Machine learning for health", agency_code="HHS-NIH11", agency_name="National Institutes of Health", status="posted", close_date=date(2026, 12, 1), description="Machine learning and predictive models for health data.")
    scored = MLRelevanceScorer().score(opportunity, today=date(2026, 7, 6))
    try:
        store.upsert_scored(scored)
        results = store.top_scored(min_score=0, limit=10)
    finally:
        store.close()
    assert len(results) == 1
    assert results[0].opportunity.source_id == "abc"
    assert results[0].score == scored.score
