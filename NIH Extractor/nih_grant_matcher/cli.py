from __future__ import annotations
import argparse, json
from pathlib import Path
from .agents import DigestAgent, GrantParserAgent, IngestionAgent, MLRelevanceAgent, NihContextAgent, NihGuideIngestionAgent
from .clients import GrantsGovClient, GrantsGovXmlClient, NihGuideClient, NihReporterClient
from .config import MatcherConfig
from .excel import write_excel
from .filters import is_current_nih_hhs_opportunity
from .scoring import MLRelevanceScorer
from .store import OpportunityStore

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Find NIH grant opportunities relevant to ML/data analysis.")
    parser.add_argument("--db", default="data/grants.sqlite3", help="SQLite database path.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Fetch, score, save, and write a digest.")
    run.add_argument("--source", choices=("nih-guide", "grants.gov", "both"), default="nih-guide", help="Opportunity source. Defaults to NIH Guide.")
    run.add_argument("--agency", action="append", help="Grants.gov agency code. Used only with --source grants.gov or both.")
    run.add_argument("--status", action="append", help="Grants.gov opportunity status. Defaults to posted and forecasted.")
    run.add_argument("--keyword", default="", help="Optional keyword search.")
    run.add_argument("--limit", type=int, default=250, help="Maximum rows to request per source.")
    run.add_argument("--out", default="digests/latest.md", help="Markdown digest path.")
    run.add_argument("--min-score", type=float, default=0.0, help="Minimum score included in digest.")
    digest = sub.add_parser("digest", help="Write a digest from saved opportunities.")
    digest.add_argument("--out", default="digests/latest.md")
    digest.add_argument("--min-score", type=float, default=0.0)
    digest.add_argument("--limit", type=int, default=100)
    excel = sub.add_parser("excel", help="Write saved ranked opportunities to an Excel .xlsx file.")
    excel.add_argument("--out", default="outputs/nih_grant_opportunities.xlsx")
    excel.add_argument("--min-score", type=float, default=0.0)
    excel.add_argument("--limit", type=int, default=500)
    context = sub.add_parser("reporter-context", help="Search NIH RePORTER for funded project context.")
    context.add_argument("--term", required=True)
    context.add_argument("--limit", type=int, default=10)
    xml = sub.add_parser("backfill-xml", help="Download the latest Grants.gov XML extract zip.")
    xml.add_argument("--out", default="data/latest_grants_extract.zip")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "run":
        return _run(args)
    if args.command == "digest":
        return _digest(args)
    if args.command == "excel":
        return _excel(args)
    if args.command == "reporter-context":
        return _reporter_context(args)
    if args.command == "backfill-xml":
        return _backfill_xml(args)
    raise ValueError(args.command)

def _run(args: argparse.Namespace) -> int:
    config = MatcherConfig(agencies=tuple(args.agency or ("HHS-NIH11",)), statuses=tuple(args.status or ("posted", "forecasted")), rows=args.limit, min_digest_score=args.min_score, db_path=args.db)
    parser = GrantParserAgent()
    relevance = MLRelevanceAgent(MLRelevanceScorer(config))
    opportunities = []
    fetched = 0
    if args.source in ("nih-guide", "both"):
        guide_opportunities = NihGuideIngestionAgent(NihGuideClient(), config).ingest(keyword=args.keyword)
        opportunities.extend(guide_opportunities)
        fetched += len(guide_opportunities)
    if args.source in ("grants.gov", "both"):
        enriched = IngestionAgent(GrantsGovClient(), config).ingest(keyword=args.keyword)
        opportunities.extend(parser.parse(hit, detail) for hit, detail in enriched)
        fetched += len(enriched)
    opportunities = _dedupe_opportunities(opportunities)
    scored = [relevance.score(opp) for opp in opportunities]
    scored = [item for item in scored if is_current_nih_hhs_opportunity(item.opportunity)]
    store = OpportunityStore(config.db_path)
    try:
        store.upsert_many(scored)
        digest_path = DigestAgent(store, min_score=args.min_score).write(args.out, limit=max(100, args.limit))
    finally:
        store.close()
    print(f"Fetched {fetched} opportunities from {args.source}.")
    print(f"Saved {len(scored)} current NIH/HHS opportunities to {config.db_path}.")
    print(f"Wrote digest to {digest_path}.")
    return 0

def _dedupe_opportunities(opportunities):
    deduped = {}
    for opportunity in opportunities:
        key = opportunity.opportunity_number or opportunity.source_id
        existing = deduped.get(key)
        if existing is None or opportunity.source_id.startswith("nih-guide:"):
            deduped[key] = opportunity
    return list(deduped.values())

def _digest(args: argparse.Namespace) -> int:
    store = OpportunityStore(args.db)
    try:
        digest_path = DigestAgent(store, min_score=args.min_score).write(args.out, limit=args.limit)
    finally:
        store.close()
    print(f"Wrote digest to {digest_path}.")
    return 0

def _excel(args: argparse.Namespace) -> int:
    store = OpportunityStore(args.db)
    try:
        items = store.top_scored(min_score=args.min_score, limit=args.limit)
        output_path = write_excel(items, args.out, min_score=args.min_score)
    finally:
        store.close()
    print(f"Wrote Excel file to {output_path}.")
    return 0

def _reporter_context(args: argparse.Namespace) -> int:
    print(json.dumps(NihContextAgent(NihReporterClient()).similar_funded_projects(args.term, limit=args.limit), indent=2))
    return 0

def _backfill_xml(args: argparse.Namespace) -> int:
    print(f"Downloaded latest Grants.gov XML extract to {GrantsGovXmlClient().download_latest(Path(args.out))}.")
    return 0
