from __future__ import annotations
import re
from datetime import date, datetime
from typing import Any
from .models import Opportunity

def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(value))).strip()

def _parse_date(value: Any) -> date | None:
    if not value:
        return None
    text = str(value).strip()
    if "T" in text:
        text = text.split("T", 1)[0]
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%b %d, %Y %I:%M:%S %p %Z", "%b %d, %Y %I:%M:%S %p", "%Y-%m-%d-%H-%M-%S"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    match = re.search(r"[A-Z][a-z]{2} \d{1,2}, \d{4}", text)
    if match:
        try:
            return datetime.strptime(match.group(0), "%b %d, %Y").date()
        except ValueError:
            return None
    return None

def _parse_money(value: Any) -> float | None:
    if value in (None, ""):
        return None
    text = re.sub(r"[^0-9.]", "", str(value))
    try:
        return float(text) if text else None
    except ValueError:
        return None

def _descriptions(items: Any) -> tuple[str, ...]:
    if not isinstance(items, list):
        return ()
    values = []
    for item in items:
        desc = _clean_text(item.get("description") or item.get("label") or item.get("programTitle")) if isinstance(item, dict) else _clean_text(item)
        if desc:
            values.append(desc)
    return tuple(values)

def _attachment_names(folders: Any, document_urls: Any) -> tuple[str, ...]:
    names = []
    if isinstance(folders, list):
        for folder in folders:
            if isinstance(folder, dict):
                for attachment in folder.get("synopsisAttachments", []):
                    name = _clean_text(attachment.get("fileName")) if isinstance(attachment, dict) else ""
                    if name:
                        names.append(name)
    if isinstance(document_urls, list):
        for item in document_urls:
            value = _clean_text(item.get("fileName") or item.get("url") or item.get("href")) if isinstance(item, dict) else _clean_text(item)
            if value:
                names.append(value)
    return tuple(dict.fromkeys(names))

def normalize_grantsgov(search_hit: dict[str, Any], detail: dict[str, Any] | None = None) -> Opportunity:
    detail = detail or {}
    synopsis = detail.get("synopsis") if isinstance(detail.get("synopsis"), dict) else {}
    agency_details = detail.get("agencyDetails") if isinstance(detail.get("agencyDetails"), dict) else {}
    source_id = str(detail.get("id") or search_hit.get("id") or "")
    close_value = search_hit.get("closeDate") or synopsis.get("responseDate") or synopsis.get("responseDateDesc") or detail.get("originalDueDateDesc")
    return Opportunity(source_id=source_id, opportunity_number=_clean_text(detail.get("opportunityNumber") or search_hit.get("number")), title=_clean_text(detail.get("opportunityTitle") or search_hit.get("title")), agency_code=_clean_text(detail.get("owningAgencyCode") or synopsis.get("agencyCode") or search_hit.get("agencyCode") or agency_details.get("agencyCode")), agency_name=_clean_text(synopsis.get("agencyName") or search_hit.get("agencyName") or agency_details.get("agencyName")), status=_clean_text(search_hit.get("oppStatus") or detail.get("oppStatus") or detail.get("docType")).lower(), open_date=_parse_date(search_hit.get("openDate") or synopsis.get("postingDate")), close_date=_parse_date(close_value), description=_clean_text(synopsis.get("synopsisDesc") or detail.get("description") or detail.get("synopsisDesc")), eligibility=_descriptions(synopsis.get("applicantTypes")), funding_instruments=_descriptions(synopsis.get("fundingInstruments")), funding_categories=_descriptions(synopsis.get("fundingActivityCategories")), award_ceiling=_parse_money(synopsis.get("awardCeiling") or synopsis.get("awardCeilingFormatted")), award_floor=_parse_money(synopsis.get("awardFloor") or synopsis.get("awardFloorFormatted")), source_url=f"https://www.grants.gov/search-results-detail/{source_id}" if source_id else "", attachments=_attachment_names(detail.get("synopsisAttachmentFolders"), detail.get("synopsisDocumentURLs")), raw={"search_hit": search_hit, "detail": detail})


def _nih_guide_url(docnum: str) -> str:
    if docnum.startswith("NOT-"):
        folder = "notice-files"
    elif docnum.startswith("RFA-"):
        folder = "rfa-files"
    else:
        folder = "pa-files"
    return f"https://grants.nih.gov/grants/guide/{folder}/{docnum}.html"

def normalize_nih_guide(item: dict[str, Any]) -> Opportunity:
    row_id = _clean_text(item.get("rowid") or item.get("_id") or item.get("docnum"))
    docnum = _clean_text(item.get("docnum"))
    organization = item.get("organization") if isinstance(item.get("organization"), dict) else {}
    primary_ic = _clean_text(item.get("primaryIC") or organization.get("primary"))
    parent_ic = _clean_text(item.get("parentIC") or organization.get("parent") or "NIH")
    ggid = _clean_text(item.get("ggid"))
    return Opportunity(
        source_id=f"nih-guide:{row_id or docnum}",
        opportunity_number=docnum,
        title=_clean_text(item.get("title")),
        agency_code=primary_ic or parent_ic,
        agency_name=f"NIH {primary_ic}".strip() if primary_ic else "National Institutes of Health",
        status=_clean_text(item.get("type") or "active").lower(),
        open_date=_parse_date(item.get("opendate") or item.get("reldate")),
        close_date=_parse_date(item.get("expdate")),
        description=_clean_text(item.get("purpose")),
        funding_instruments=tuple(_clean_text(code) for code in (item.get("ac") or []) if _clean_text(code)),
        funding_categories=(_clean_text(item.get("doctype")),) if _clean_text(item.get("doctype")) else (),
        source_url=_nih_guide_url(docnum) if docnum else "https://grants.nih.gov/funding/nih-guide-for-grants-and-contracts",
        raw={"source": "nih_guide", "guide_item": item, "grants_gov_url": f"https://www.grants.gov/search-results-detail/{ggid}" if ggid else ""},
    )
