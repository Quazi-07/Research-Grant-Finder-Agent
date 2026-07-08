from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from nih_grant_matcher.config import MatcherConfig
from nih_grant_matcher.excel import write_excel
from nih_grant_matcher.models import ScoredOpportunity
from nih_grant_matcher.workflow import load_saved, run_and_save


DEFAULT_DB = "data/grants.sqlite3"
DEFAULT_EXCEL = "outputs/nih_grant_opportunities_ui.xlsx"


st.set_page_config(page_title="NIH Grant Matcher", page_icon="NIH", layout="wide")
st.title("NIH Grant Opportunity Matcher")
st.caption("Run NIH Guide and Grants.gov searches, rank computational opportunities, and explore the results interactively.")


def get_scored_items_from_session() -> list[ScoredOpportunity]:
    # Older versions accidentally used st.session_state.items, which resolves
    # to a method. Clear that key and guard against any stale callable value.
    if "items" in st.session_state:
        del st.session_state["items"]
    value = st.session_state.get("scored_items", [])
    if callable(value) or value is None:
        st.session_state["scored_items"] = []
        return []
    return list(value)


def set_scored_items_in_session(value: list[ScoredOpportunity]) -> None:
    st.session_state["scored_items"] = list(value or [])


def scored_to_records(items: list[ScoredOpportunity]) -> list[dict]:
    records = []
    for rank, item in enumerate(items, start=1):
        opp = item.opportunity
        raw = opp.raw or {}
        grants_gov_url = raw.get("grants_gov_url") or ""
        if not grants_gov_url and isinstance(raw.get("guide_item"), dict) and raw["guide_item"].get("ggid"):
            grants_gov_url = f"https://www.grants.gov/search-results-detail/{raw['guide_item']['ggid']}"
        records.append(
            {
                "Rank": rank,
                "Classification": item.classification,
                "Score": item.score,
                "Opportunity Number": opp.opportunity_number,
                "Title": opp.title,
                "NIH Institute": opp.agency_code or opp.agency_name,
                "Agency": opp.agency_name,
                "Status": opp.status,
                "Open Date": opp.open_date,
                "Close Date": opp.close_date,
                "Activity": ", ".join(opp.funding_instruments),
                "Category": ", ".join(opp.funding_categories),
                "Matched Terms": ", ".join(item.matched_terms),
                "Why It Matched": "; ".join(item.reasons),
                "Summary": opp.description,
                "Source URL": opp.source_url,
                "Grants.gov URL": grants_gov_url,
                "Source ID": opp.source_id,
            }
        )
    return records


def make_dataframe(items: list[ScoredOpportunity]) -> pd.DataFrame:
    frame = pd.DataFrame(scored_to_records(items))
    if frame.empty:
        return frame
    frame["Open Date"] = pd.to_datetime(frame["Open Date"], errors="coerce")
    frame["Close Date"] = pd.to_datetime(frame["Close Date"], errors="coerce")
    frame["Close Month"] = frame["Close Date"].dt.to_period("M").astype(str).replace("NaT", "Not listed")
    return frame


def apply_filters(frame: pd.DataFrame, min_score: float, classifications: list[str], institutes: list[str], term_query: str) -> pd.DataFrame:
    if frame.empty:
        return frame
    filtered = frame[frame["Score"] >= min_score].copy()
    if classifications:
        filtered = filtered[filtered["Classification"].isin(classifications)]
    if institutes:
        filtered = filtered[filtered["NIH Institute"].isin(institutes)]
    if term_query.strip():
        query = term_query.strip().lower()
        haystack = (
            filtered["Title"].fillna("")
            + " "
            + filtered["Matched Terms"].fillna("")
            + " "
            + filtered["Summary"].fillna("")
        ).str.lower()
        filtered = filtered[haystack.str.contains(query, regex=False)]
    return filtered


with st.sidebar:
    st.header("Run Search")
    source = st.selectbox("Source", ["nih-guide", "both", "grants.gov"], index=0)
    keyword = st.text_input("Keyword", value="", placeholder="AI, machine learning, imaging...")
    limit = st.slider("Rows per source", min_value=25, max_value=500, value=250, step=25)
    db_path = st.text_input("Database", value=DEFAULT_DB)
    run_clicked = st.button("Run Search", type="primary", use_container_width=True)

    st.divider()
    st.header("Display")
    min_score = st.slider("Minimum score shown", 0.0, 100.0, 0.0, 5.0)
    max_saved = st.slider("Saved rows to load", 50, 1000, 500, 50)
    load_clicked = st.button("Load Saved Results", use_container_width=True)

    st.divider()
    st.header("Export")
    excel_path = st.text_input("Excel output", value=DEFAULT_EXCEL)
    export_clicked = st.button("Export Current View", use_container_width=True)


if "scored_items" not in st.session_state:
    st.session_state["scored_items"] = []
if "items" in st.session_state:
    del st.session_state["items"]
if "last_run" not in st.session_state:
    st.session_state["last_run"] = None

if run_clicked:
    config = MatcherConfig(rows=limit, db_path=db_path, min_digest_score=min_score)
    with st.spinner("Fetching and scoring opportunities..."):
        try:
            items, summary = run_and_save(config, source=source, keyword=keyword)
        except Exception as exc:
            st.error(f"Search failed: {exc}")
        else:
            set_scored_items_in_session(items)
            st.session_state["last_run"] = summary
            st.success(f"Fetched {summary.fetched} records from {summary.source}; saved {summary.saved} current NIH/HHS opportunities.")

if load_clicked or (not get_scored_items_from_session() and Path(db_path).exists()):
    try:
        set_scored_items_in_session(load_saved(db_path, min_score=0.0, limit=max_saved))
    except Exception as exc:
        st.warning(f"Could not load saved results: {exc}")

items = get_scored_items_from_session()
frame = make_dataframe(items)

if frame.empty:
    st.info("Run a search or load saved results to populate the dashboard.")
    st.stop()

all_classes = sorted(frame["Classification"].dropna().unique().tolist())
all_institutes = sorted(frame["NIH Institute"].dropna().unique().tolist())

filter_col1, filter_col2, filter_col3 = st.columns([1.1, 1.3, 1.6])
with filter_col1:
    selected_classes = st.multiselect("Classification", all_classes, default=all_classes)
with filter_col2:
    selected_institutes = st.multiselect("NIH institute", all_institutes)
with filter_col3:
    term_filter = st.text_input("Filter within results", placeholder="PRIMED-AI, EHR, NINDS...")

filtered = apply_filters(frame, min_score=min_score, classifications=selected_classes, institutes=selected_institutes, term_query=term_filter)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
metric_col1.metric("Visible Opportunities", f"{len(filtered):,}")
metric_col2.metric("High Matches", f"{(filtered['Classification'] == 'High').sum():,}")
metric_col3.metric("Median Score", f"{filtered['Score'].median():.1f}" if not filtered.empty else "0")
next_deadline = filtered["Close Date"].dropna().min() if not filtered.empty else None
metric_col4.metric("Next Deadline", next_deadline.strftime("%Y-%m-%d") if pd.notna(next_deadline) else "Not listed")

tab_results, tab_visuals, tab_detail = st.tabs(["Results", "Visuals", "Details"])

with tab_results:
    st.dataframe(
        filtered.drop(columns=["Source ID"], errors="ignore"),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.1f"),
            "Source URL": st.column_config.LinkColumn("NIH Guide URL"),
            "Grants.gov URL": st.column_config.LinkColumn("Grants.gov URL"),
            "Open Date": st.column_config.DateColumn("Open Date", format="YYYY-MM-DD"),
            "Close Date": st.column_config.DateColumn("Close Date", format="YYYY-MM-DD"),
        },
    )

with tab_visuals:
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("Matches by Classification")
        st.bar_chart(filtered["Classification"].value_counts().reindex(["High", "Medium", "Watchlist"]).dropna())
    with chart_col2:
        st.subheader("Top NIH Institutes")
        st.bar_chart(filtered["NIH Institute"].value_counts().head(12))

    chart_col3, chart_col4 = st.columns(2)
    with chart_col3:
        st.subheader("Score Distribution")
        score_labels = ["0-25", "25-45", "45-70", "70-100"]
        score_bins = pd.cut(
            filtered["Score"],
            bins=[0, 25, 45, 70, 100],
            labels=score_labels,
            include_lowest=True,
        )
        score_counts = score_bins.value_counts().reindex(score_labels, fill_value=0)
        st.bar_chart(score_counts)
    with chart_col4:
        st.subheader("Deadlines by Month")
        month_counts = filtered[filtered["Close Month"] != "Not listed"]["Close Month"].value_counts().sort_index()
        if month_counts.empty:
            st.info("No deadline dates in the current view.")
        else:
            st.bar_chart(month_counts)

with tab_detail:
    options = filtered["Opportunity Number"].fillna("") + " | " + filtered["Title"].fillna("")
    selected = st.selectbox("Opportunity", options.tolist()) if not filtered.empty else None
    if selected:
        row = filtered.iloc[options.tolist().index(selected)]
        st.subheader(row["Title"])
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Score", f"{row['Score']:.1f}")
        d2.metric("Class", row["Classification"])
        d3.metric("Institute", row["NIH Institute"])
        d4.metric("Deadline", row["Close Date"].strftime("%Y-%m-%d") if pd.notna(row["Close Date"]) else "Not listed")
        st.markdown(f"**Opportunity number:** {row['Opportunity Number']}")
        st.markdown(f"**Matched terms:** {row['Matched Terms'] or 'None'}")
        st.markdown(f"**Why it matched:** {row['Why It Matched']}")
        st.write(row["Summary"] or "No summary available.")
        link_cols = st.columns(2)
        if row["Source URL"]:
            link_cols[0].link_button("Open NIH Guide", row["Source URL"], use_container_width=True)
        if row["Grants.gov URL"]:
            link_cols[1].link_button("Open Grants.gov", row["Grants.gov URL"], use_container_width=True)

if export_clicked:
    visible_ids = set(filtered["Source ID"].tolist())
    visible_items = [item for item in items if item.opportunity.source_id in visible_ids]
    try:
        output_path = write_excel(visible_items, excel_path, min_score=min_score)
        st.success(f"Wrote Excel file to {output_path}")
        with open(output_path, "rb") as handle:
            st.download_button("Download Excel", handle.read(), file_name=Path(output_path).name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as exc:
        st.error(f"Excel export failed: {exc}")

