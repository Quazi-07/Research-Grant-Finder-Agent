from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

@dataclass(frozen=True)
class Opportunity:
    source_id: str
    opportunity_number: str
    title: str
    agency_code: str
    agency_name: str
    status: str
    open_date: date | None = None
    close_date: date | None = None
    description: str = ""
    eligibility: tuple[str, ...] = ()
    funding_instruments: tuple[str, ...] = ()
    funding_categories: tuple[str, ...] = ()
    award_ceiling: float | None = None
    award_floor: float | None = None
    source_url: str = ""
    attachments: tuple[str, ...] = ()
    raw: dict[str, Any] = field(default_factory=dict)
    @property
    def searchable_text(self) -> str:
        parts = [self.title, self.description, " ".join(self.eligibility), " ".join(self.funding_instruments), " ".join(self.funding_categories), self.agency_name]
        return "\n".join(p for p in parts if p)

@dataclass(frozen=True)
class ScoreBreakdown:
    keyword_score: float
    semantic_score: float
    nih_score: float
    urgency_score: float
    completeness_score: float
    centrality_score: float
    generic_penalty: float

@dataclass(frozen=True)
class ScoredOpportunity:
    opportunity: Opportunity
    score: float
    classification: str
    reasons: tuple[str, ...]
    matched_terms: tuple[str, ...]
    breakdown: ScoreBreakdown
    scored_at: datetime
