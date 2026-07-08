from __future__ import annotations
from dataclasses import dataclass, field

GRANTSGOV_SEARCH_URL = "https://api.grants.gov/v1/api/search2"
GRANTSGOV_FETCH_URL = "https://api.grants.gov/v1/api/fetchOpportunity"
GRANTSGOV_XML_EXTRACT_URL = "https://www.grants.gov/xml-extract"
NIH_REPORTER_SEARCH_URL = "https://api.reporter.nih.gov/v2/projects/search"
NIH_GUIDE_API_URL = "https://vtbgfslh0k.execute-api.us-east-1.amazonaws.com/prod"

DEFAULT_KEYWORDS = {
    "machine learning": 18, "artificial intelligence": 18, "deep learning": 18,
    "predictive model": 16, "predictive modeling": 16, "prediction model": 16,
    "clinical prediction": 16, "risk model": 14, "natural language processing": 16,
    "computer vision": 16, "clinical decision support": 12, "multimodal data": 12, "data science": 14, "statistical modeling": 12,
    "bioinformatics": 12, "computational": 10, "omics": 10, "ehr": 10,
    "electronic health record": 10, "imaging analytics": 12, "data analysis": 8,
    "analytics": 7, "algorithm": 7, "modeling": 6,
}
CURATED_COMPUTATIONAL_EXAMPLES = (
    "Develop machine learning models to predict clinical risk from electronic health records.",
    "Use deep learning and computer vision to analyze biomedical imaging data.",
    "Apply bioinformatics and multi-omics data integration to identify disease mechanisms.",
    "Create predictive models and statistical learning tools for patient outcomes.",
    "Use natural language processing to extract phenotypes from clinical text.",
    "Build artificial intelligence methods for biomedical data analysis.",
)
GENERIC_BIOMEDICAL_TERMS = {"clinical trial", "health disparities", "community health", "training program", "capacity building", "implementation", "prevention", "therapeutic"}

@dataclass(frozen=True)
class MatcherConfig:
    agencies: tuple[str, ...] = ("HHS-NIH11",)
    statuses: tuple[str, ...] = ("posted", "forecasted")
    rows: int = 250
    min_digest_score: float = 0.0
    db_path: str = "data/grants.sqlite3"
    keywords: dict[str, int] = field(default_factory=lambda: dict(DEFAULT_KEYWORDS))
    semantic_examples: tuple[str, ...] = CURATED_COMPUTATIONAL_EXAMPLES
