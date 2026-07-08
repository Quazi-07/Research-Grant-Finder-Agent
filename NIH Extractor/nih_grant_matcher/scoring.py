from __future__ import annotations
import math, re
from collections import Counter
from datetime import date, datetime
from .config import GENERIC_BIOMEDICAL_TERMS, MatcherConfig
from .models import Opportunity, ScoreBreakdown, ScoredOpportunity

TOKEN_RE = re.compile(r"[a-z0-9]+")
AI_WORD_RE = re.compile(r"\bai\b", re.IGNORECASE)
def _term_frequency(text: str) -> Counter[str]:
    return Counter(TOKEN_RE.findall(text.lower()))
def _cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    numerator = sum(left[token] * right[token] for token in set(left) & set(right))
    left_norm = math.sqrt(sum(v * v for v in left.values()))
    right_norm = math.sqrt(sum(v * v for v in right.values()))
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0

class MLRelevanceScorer:
    def __init__(self, config: MatcherConfig | None = None) -> None:
        self.config = config or MatcherConfig()
        self.example_vectors = [_term_frequency(example) for example in self.config.semantic_examples]
    def score(self, opportunity: Opportunity, today: date | None = None) -> ScoredOpportunity:
        today = today or date.today()
        text = opportunity.searchable_text.lower()
        title = opportunity.title.lower()
        matched_terms, keyword_score, centrality_score = [], 0.0, 0.0
        if AI_WORD_RE.search(opportunity.searchable_text):
            matched_terms.append("AI")
            keyword_score += 18
            centrality_score += 12 if AI_WORD_RE.search(opportunity.title) else 4
        for phrase, weight in self.config.keywords.items():
            if phrase in text:
                matched_terms.append(phrase)
                keyword_score += weight
                centrality_score += min(weight * (0.8 if phrase in title else 0.25), 12 if phrase in title else 4)
        vector = _term_frequency(opportunity.searchable_text)
        semantic_score = min(max((_cosine(vector, ex) for ex in self.example_vectors), default=0.0) * 80, 20)
        nih_score = 10.0 if self._is_nih_hhs(opportunity) else 0.0
        urgency_score = self._deadline_score(opportunity.close_date, today)
        completeness_score = self._completeness_score(opportunity)
        generic_penalty = self._generic_penalty(text, matched_terms)
        score = max(0.0, min(100.0, keyword_score + semantic_score + nih_score + urgency_score + completeness_score + min(centrality_score, 18) - generic_penalty))
        return ScoredOpportunity(opportunity=opportunity, score=round(score, 1), classification=self._classification(score), reasons=tuple(self._reasons(opportunity, matched_terms, semantic_score, urgency_score, generic_penalty)), matched_terms=tuple(matched_terms), breakdown=ScoreBreakdown(round(keyword_score, 1), round(semantic_score, 1), round(nih_score, 1), round(urgency_score, 1), round(completeness_score, 1), round(min(centrality_score, 18), 1), round(generic_penalty, 1)), scored_at=datetime.utcnow())
    @staticmethod
    def _is_nih_hhs(opportunity: Opportunity) -> bool:
        combined = f"{opportunity.agency_code} {opportunity.agency_name}".lower()
        return "nih" in combined or "national institutes of health" in combined or "hhs" in combined
    @staticmethod
    def _deadline_score(close_date: date | None, today: date) -> float:
        if close_date is None:
            return 3.0
        days = (close_date - today).days
        if days < 0:
            return -20.0
        if days <= 14:
            return 4.0
        if days <= 90:
            return 8.0
        if days <= 240:
            return 6.0
        return 3.0
    @staticmethod
    def _completeness_score(opportunity: Opportunity) -> float:
        fields = [opportunity.description, opportunity.close_date, opportunity.eligibility, opportunity.funding_instruments, opportunity.funding_categories, opportunity.award_ceiling, opportunity.source_url]
        return sum(1.0 for field in fields if field) / len(fields) * 7.0
    @staticmethod
    def _generic_penalty(text: str, matched_terms: list[str]) -> float:
        generic_hits = sum(1 for term in GENERIC_BIOMEDICAL_TERMS if term in text)
        return max(0.0, generic_hits * 2.0 - len(matched_terms)) if matched_terms else generic_hits * 5.0
    @staticmethod
    def _classification(score: float) -> str:
        return "High" if score >= 70 else "Medium" if score >= 45 else "Watchlist"
    @staticmethod
    def _reasons(opportunity: Opportunity, matched_terms: list[str], semantic_score: float, urgency_score: float, generic_penalty: float) -> list[str]:
        reasons = []
        if matched_terms:
            reasons.append("Matched computational terms: " + ", ".join(matched_terms[:6]))
        if semantic_score >= 8:
            reasons.append("Description is close to curated ML/data-science grant examples")
        if MLRelevanceScorer._is_nih_hhs(opportunity):
            reasons.append("Source agency appears to be NIH/HHS")
        if opportunity.close_date and urgency_score > 0:
            reasons.append(f"Deadline is still active: {opportunity.close_date.isoformat()}")
        if generic_penalty > 0 and not matched_terms:
            reasons.append("Mostly generic biomedical wording; keep only as watchlist")
        return reasons or ["Weak computational signal; included for monitoring only"]
