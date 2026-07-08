from __future__ import annotations
from dataclasses import dataclass
from .clients import GrantsGovClient, NihGuideClient, NihReporterClient
from .config import MatcherConfig
from .digest import write_digest
from .models import Opportunity, ScoredOpportunity
from .normalizer import normalize_grantsgov, normalize_nih_guide
from .scoring import MLRelevanceScorer
from .store import OpportunityStore

@dataclass
class IngestionAgent:
    client: GrantsGovClient
    config: MatcherConfig
    def ingest(self, keyword: str = "") -> list[tuple[dict, dict]]:
        hits = self.client.search_all(list(self.config.agencies), list(self.config.statuses), limit=self.config.rows, keyword=keyword)
        return [(hit, self.client.fetch_opportunity(hit["id"])) for hit in hits]

@dataclass
class NihGuideIngestionAgent:
    client: NihGuideClient
    config: MatcherConfig
    def ingest(self, keyword: str = "") -> list[Opportunity]:
        return [normalize_nih_guide(item) for item in self.client.search(rows=self.config.rows, keyword=keyword)]

class GrantParserAgent:
    def parse(self, hit: dict, detail: dict | None = None) -> Opportunity:
        return normalize_grantsgov(hit, detail)

@dataclass
class MLRelevanceAgent:
    scorer: MLRelevanceScorer
    def score(self, opportunity: Opportunity) -> ScoredOpportunity:
        return self.scorer.score(opportunity)

@dataclass
class NihContextAgent:
    client: NihReporterClient
    def similar_funded_projects(self, term: str, limit: int = 25) -> list[dict]:
        return self.client.search_projects(term, limit=limit)

@dataclass
class DigestAgent:
    store: OpportunityStore
    min_score: float
    def write(self, output_path: str, limit: int = 50) -> str:
        return str(write_digest(self.store.top_scored(min_score=self.min_score, limit=limit), output_path, min_score=self.min_score))

@dataclass
class ReviewFeedbackAgent:
    store: OpportunityStore
    def record_feedback(self, source_id: str, useful: bool, note: str = "") -> None:
        self.store.conn.execute("CREATE TABLE IF NOT EXISTS feedback (source_id TEXT PRIMARY KEY, useful INTEGER NOT NULL, note TEXT, reviewed_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        with self.store.conn:
            self.store.conn.execute("INSERT INTO feedback (source_id, useful, note) VALUES (?, ?, ?) ON CONFLICT(source_id) DO UPDATE SET useful=excluded.useful, note=excluded.note, reviewed_at=CURRENT_TIMESTAMP", (source_id, 1 if useful else 0, note))
