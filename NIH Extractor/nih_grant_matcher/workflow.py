from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .agents import GrantParserAgent, IngestionAgent, MLRelevanceAgent, NihGuideIngestionAgent
from .clients import GrantsGovClient, NihGuideClient
from .config import MatcherConfig
from .filters import is_current_nih_hhs_opportunity
from .models import Opportunity, ScoredOpportunity
from .scoring import MLRelevanceScorer
from .store import OpportunityStore


@dataclass(frozen=True)
class RunSummary:
    fetched: int
    saved: int
    source: str


def fetch_score_opportunities(config: MatcherConfig, source: str = "nih-guide", keyword: str = "") -> tuple[list[ScoredOpportunity], int]:
    parser = GrantParserAgent()
    relevance = MLRelevanceAgent(MLRelevanceScorer(config))
    opportunities: list[Opportunity] = []
    fetched = 0

    if source in ("nih-guide", "both"):
        guide_opportunities = NihGuideIngestionAgent(NihGuideClient(), config).ingest(keyword=keyword)
        opportunities.extend(guide_opportunities)
        fetched += len(guide_opportunities)

    if source in ("grants.gov", "both"):
        enriched = IngestionAgent(GrantsGovClient(), config).ingest(keyword=keyword)
        opportunities.extend(parser.parse(hit, detail) for hit, detail in enriched)
        fetched += len(enriched)

    scored = [relevance.score(opp) for opp in _dedupe_opportunities(opportunities)]
    current = [item for item in scored if is_current_nih_hhs_opportunity(item.opportunity)]
    current.sort(key=lambda item: (-item.score, item.opportunity.close_date is None, item.opportunity.close_date or item.scored_at.date()))
    return current, fetched


def run_and_save(config: MatcherConfig, source: str = "nih-guide", keyword: str = "") -> tuple[list[ScoredOpportunity], RunSummary]:
    scored, fetched = fetch_score_opportunities(config, source=source, keyword=keyword)
    store = OpportunityStore(config.db_path)
    try:
        saved = store.upsert_many(scored)
    finally:
        store.close()
    return scored, RunSummary(fetched=fetched, saved=saved, source=source)


def load_saved(db_path: str, min_score: float = 0.0, limit: int = 500) -> list[ScoredOpportunity]:
    store = OpportunityStore(db_path)
    try:
        return store.top_scored(min_score=min_score, limit=limit)
    finally:
        store.close()


def _dedupe_opportunities(opportunities: Iterable[Opportunity]) -> list[Opportunity]:
    deduped: dict[str, Opportunity] = {}
    for opportunity in opportunities:
        key = opportunity.opportunity_number or opportunity.source_id
        existing = deduped.get(key)
        if existing is None or opportunity.source_id.startswith("nih-guide:"):
            deduped[key] = opportunity
    return list(deduped.values())

