from __future__ import annotations
from datetime import datetime
from pathlib import Path
from .models import ScoredOpportunity

def render_digest(items: list[ScoredOpportunity], min_score: float = 35.0) -> str:
    included = [item for item in items if item.score >= min_score]
    lines = ["# NIH Grant Opportunity Matcher Digest", "", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", f"Minimum score: {min_score:g}", f"Included opportunities: {len(included)}", ""]
    if not included:
        return "\n".join(lines + ["No opportunities met the current threshold.", "", "Try lowering --min-score or running a broader agency/status search."]).rstrip() + "\n"
    for index, scored in enumerate(included, start=1):
        opp = scored.opportunity
        lines += [f"## {index}. {opp.title}", "", f"- Score: {scored.score:g} ({scored.classification})", f"- Opportunity number: {opp.opportunity_number or 'Not listed'}", f"- Agency: {opp.agency_name or opp.agency_code or 'Not listed'}", f"- Status: {opp.status or 'Not listed'}", f"- Deadline: {opp.close_date.isoformat() if opp.close_date else 'Not listed'}", f"- Link: {opp.source_url or 'Not listed'}"]
        if opp.award_ceiling is not None:
            lines.append(f"- Award ceiling: USD {opp.award_ceiling:,.0f}")
        if scored.matched_terms:
            lines.append("- Matched terms: " + ", ".join(scored.matched_terms))
        lines.append("- Why it matched:")
        lines += [f"  - {reason}" for reason in scored.reasons]
        summary = _summary(opp.description)
        if summary:
            lines += ["", summary]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"

def write_digest(items: list[ScoredOpportunity], path: str | Path, min_score: float = 35.0) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_digest(items, min_score=min_score), encoding="utf-8")
    return path

def _summary(description: str, max_chars: int = 650) -> str:
    clean = " ".join(description.split())
    return clean if len(clean) <= max_chars else clean[:max_chars].rsplit(" ", 1)[0] + "..."
