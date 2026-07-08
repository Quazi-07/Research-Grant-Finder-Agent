# 🧠 NIH Grant Intelligence Agent

### An Agentic Research Software System for Autonomous Funding Discovery, Computational Relevance Analysis, and NIH Opportunity Prioritization

<p align="center">
  <b>Discover. Analyze. Rank. Review. Act.</b>
</p>

<p align="center">
  An agent-oriented research intelligence workflow that continuously transforms public NIH funding information into prioritized opportunities for AI, machine learning, data science, bioinformatics, imaging, and computational research teams.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Architecture-Agentic_AI-purple" alt="Agentic AI">
  <img src="https://img.shields.io/badge/Interface-Streamlit-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey" alt="SQLite">
  <img src="https://img.shields.io/badge/Data-NIH_Guide-green" alt="NIH Guide">
  <img src="https://img.shields.io/badge/Data-Grants.gov-blue" alt="Grants.gov">
  <img src="https://img.shields.io/badge/Context-NIH_RePORTER-darkgreen" alt="NIH RePORTER">
  <img src="https://img.shields.io/badge/Status-Research_Prototype-orange" alt="Status">
</p>

---

## 🚀 From Grant Search to Grant Intelligence

Researchers often spend hours manually searching funding databases, reviewing long opportunity announcements, and deciding whether a funding opportunity aligns with their expertise.

The **NIH Grant Intelligence Agent** explores a different approach.

Instead of treating funding discovery as a simple keyword search problem, the software organizes the process as an **agent-oriented research workflow**.

Specialized software agents collect funding records, normalize heterogeneous information, evaluate computational relevance, retrieve research context, prioritize opportunities, preserve results, and support researcher review.

The objective is simple:

> **Turn fragmented public funding information into actionable research intelligence.**

---

## 🤖 Agentic Research Workflow

The system separates major grant intelligence tasks into specialized software agents.

| Agent                             | Responsibility                                                         |
| --------------------------------- | ---------------------------------------------------------------------- |
| 🔎 **NIH Guide Ingestion Agent**  | Discovers and normalizes NIH Guide funding announcements               |
| 🌐 **Grants.gov Ingestion Agent** | Searches and enriches federal opportunity records                      |
| 🧩 **Grant Parser Agent**         | Converts heterogeneous funding records into a common opportunity model |
| 🧠 **ML Relevance Agent**         | Evaluates computational and data-science relevance                     |
| 🔬 **NIH Context Agent**          | Retrieves related funded-project context from NIH RePORTER             |
| 📊 **Digest Agent**               | Produces prioritized funding intelligence reports                      |
| 👤 **Review Feedback Agent**      | Captures researcher feedback for future relevance tuning               |

These agents support a coordinated workflow for funding discovery and prioritization.

```text
                    ┌──────────────────────────┐
                    │   PUBLIC FUNDING DATA    │
                    └─────────────┬────────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
      │ NIH GUIDE   │      │ GRANTS.GOV  │      │NIH RePORTER │
      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
             │                    │                    │
             ▼                    ▼                    ▼
      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
      │ NIH GUIDE   │      │ INGESTION   │      │ NIH CONTEXT │
      │    AGENT    │      │    AGENT    │      │    AGENT    │
      └──────┬──────┘      └──────┬──────┘      └─────────────┘
             │                    │
             └────────────┬───────┘
                          ▼
                  ┌───────────────┐
                  │ GRANT PARSER  │
                  │     AGENT     │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │ DEDUPLICATION │
                  │  & FILTERING  │
                  └───────┬───────┘
                          ▼
                  ┌───────────────┐
                  │ ML RELEVANCE  │
                  │     AGENT     │
                  └───────┬───────┘
                          ▼
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
         🔴 HIGH       🟠 MEDIUM    🟡 WATCHLIST
             │            │            │
             └────────────┼────────────┘
                          ▼
                  ┌───────────────┐
                  │    SQLITE     │
                  │ INTELLIGENCE  │
                  │     STORE     │
                  └───────┬───────┘
                          ▼
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
     📊 DASHBOARD     📗 EXCEL        📄 DIGEST
                          │
                          ▼
                  👤 RESEARCHER REVIEW
                          │
                          ▼
                  🔁 FEEDBACK AGENT
```

---

## 🧠 How the Intelligence Engine Thinks

The system does not rely on a single keyword.

Each funding opportunity is evaluated using multiple computational signals.

### 1. Computational Keyword Intelligence

The engine searches for signals associated with:

* Artificial intelligence
* Machine learning
* Deep learning
* Predictive modeling
* Data science
* Bioinformatics
* Omics
* Medical imaging
* Statistical modeling
* Multimodal data
* Data integration

### 2. Title Centrality Analysis

Computational concepts appearing directly in the opportunity title receive stronger relevance weighting.

The assumption is that a computational concept appearing in the title is more likely to represent a central scientific theme.

### 3. Grant Similarity Analysis

Opportunity descriptions are compared with curated AI and data-science grant examples.

Text similarity provides an additional relevance signal when explicit computational terminology is limited.

### 4. NIH/HHS Source Intelligence

The scoring system considers whether the opportunity originates from an NIH or HHS source.

### 5. Deadline Awareness

Active deadlines contribute to prioritization so researchers can focus on actionable opportunities.

### 6. Record Completeness

Opportunities with richer metadata receive additional consideration.

### 7. Biomedical Noise Reduction

Generic biomedical terminology can create false-positive computational matches.

The intelligence engine applies penalties when biomedical language is broad but computational evidence is weak.

---

## 🎯 Opportunity Intelligence Classification

Each opportunity receives a relevance score from **0–100**.

| Intelligence Level | Interpretation                                                                                        |
| ------------------ | ----------------------------------------------------------------------------------------------------- |
| 🔴 **HIGH**        | Strong evidence that AI, ML, statistics, or computational expertise may be central to the opportunity |
| 🟠 **MEDIUM**      | Potential opportunity for interdisciplinary data-science collaboration                                |
| 🟡 **WATCHLIST**   | Weak or emerging computational signals; retained for monitoring                                       |

The score is designed to **prioritize expert review—not replace scientific judgment**.

---

## 📊 Research Intelligence Dashboard

The Streamlit interface provides an interactive environment for grant opportunity analysis.

Researchers can:

* 🔍 Search NIH Guide and Grants.gov
* 🎯 Filter by relevance classification
* 🏛️ Filter by NIH institute
* 🧠 Search within computational signals
* 📈 Review relevance score distributions
* 📅 Monitor upcoming deadlines
* 🔬 Inspect why an opportunity matched
* 🔗 Open official NIH Guide and Grants.gov records
* 📗 Export selected opportunities to Excel

### Dashboard Intelligence Metrics

The dashboard automatically displays:

* **Visible Opportunities**
* **High-Priority Matches**
* **Median Relevance Score**
* **Next Funding Deadline**

---

## 🔍 Explainable Opportunity Matching

A major design principle of the system is **transparent prioritization**.

For each opportunity, the software preserves:

* Relevance score
* Priority classification
* Matched computational terms
* Reasons for the match
* NIH institute
* Opportunity status
* Open and close dates
* Funding category
* Opportunity description
* Official source links

Researchers can inspect **why an opportunity was prioritized** before deciding whether to pursue it.

---

## 🧬 NIH RePORTER Research Context

The architecture includes an **NIH Context Agent** designed to retrieve related funded projects from NIH RePORTER.

This capability creates a foundation for future research intelligence tasks such as:

* Identifying previously funded work
* Exploring related scientific topics
* Understanding funding patterns
* Comparing new opportunities with funded projects
* Identifying potential research gaps

---

## 🔁 Human-in-the-Loop Research Intelligence

The system includes a **Review Feedback Agent** that records researcher assessments of opportunities.

Researchers can identify whether an opportunity was useful and preserve review notes.

This creates the foundation for a future adaptive recommendation system in which researcher feedback can improve opportunity prioritization.

```text
Agent Recommendation
        │
        ▼
Researcher Review
        │
        ▼
Useful / Not Useful
        │
        ▼
Feedback Store
        │
        ▼
Future Relevance Tuning
```

The long-term objective is a **human-AI collaborative grant discovery environment**.

---

## 🛠️ Technology Stack

| Technology            | Role                                        |
| --------------------- | ------------------------------------------- |
| 🐍 Python             | Agent and workflow development              |
| 🐼 Pandas             | Data processing and analytics               |
| 📊 Streamlit          | Interactive research intelligence interface |
| 🗄️ SQLite            | Persistent opportunity intelligence store   |
| 🔌 REST APIs          | Funding and research data integration       |
| 📗 Excel              | Research collaboration and export           |
| 🧠 Similarity Scoring | Computational relevance analysis            |

---

## 📂 Current Software Capabilities

The research prototype currently supports:

* Multi-source funding ingestion
* NIH Guide opportunity collection
* Grants.gov search and enrichment
* Heterogeneous grant record normalization
* Opportunity deduplication
* NIH/HHS opportunity filtering
* Computational relevance scoring
* Explainable match reasoning
* Deadline-aware prioritization
* SQLite persistence
* Saved opportunity retrieval
* Markdown digest generation
* Excel export
* Interactive Streamlit analytics
* NIH RePORTER research-context retrieval
* Researcher feedback storage

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Quazi-07/nih-grant-opportunity-matcher.git
cd nih-grant-opportunity-matcher/"NIH Extractor"
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch the Research Intelligence Dashboard

```bash
streamlit run streamlit_app.py
```

The dashboard will open in your browser.

---

## 🧪 Research Software Status

> **Current Stage: Functional Research Prototype**

The system currently implements an agent-oriented funding discovery and prioritization workflow.

It is intended as a research software platform for exploring how data science, AI, and agent-based architectures can support research development and funding intelligence.

The current intelligence engine uses explainable computational scoring and text similarity.

It does **not currently rely on a Large Language Model for autonomous scientific reasoning**.

This distinction is intentional and provides a transparent baseline for evaluating future LLM-based agents.

---

## 🗺️ Roadmap: Toward Autonomous Research Funding Intelligence

### Phase I — Funding Intelligence Foundation ✅

* [x] NIH Guide ingestion
* [x] Grants.gov ingestion
* [x] Opportunity normalization
* [x] Relevance scoring
* [x] Opportunity prioritization
* [x] SQLite persistence
* [x] Interactive dashboard

### Phase II — Research Context Intelligence 🚧

* [x] NIH RePORTER client architecture
* [ ] Funded-project similarity analysis
* [ ] Institute-level funding trend analysis
* [ ] Research topic clustering
* [ ] Funding-gap identification

### Phase III — Generative AI Agents 🔮

* [ ] LLM Grant Summary Agent
* [ ] Researcher Expertise Extraction Agent
* [ ] CV-to-NOFO Matching Agent
* [ ] Scientific Fit Explanation Agent
* [ ] Eligibility Review Agent
* [ ] Collaboration Recommendation Agent

### Phase IV — Agentic Funding Surveillance 🔮

* [ ] Autonomous scheduled opportunity monitoring
* [ ] New-NOFO detection
* [ ] Opportunity change tracking
* [ ] Deadline monitoring
* [ ] Personalized email intelligence digests
* [ ] Agent memory for researcher preferences
* [ ] Human-feedback-driven ranking adaptation

### Phase V — Research Collaboration Intelligence 🔮

* [ ] Researcher network discovery
* [ ] Expertise-gap analysis
* [ ] Potential Co-I recommendation
* [ ] Multi-investigator team formation support
* [ ] Institution-level research intelligence

---

## 🔮 Long-Term Vision

The long-term vision is to evolve the NIH Grant Intelligence Agent into an **Agentic Research Funding Intelligence Platform**.

A future research team could provide:

* Research interests
* CVs or biosketches
* Publication histories
* Technical expertise
* Prior grant experience

Autonomous research agents could then:

1. Continuously monitor funding sources.
2. Detect newly published opportunities.
3. Analyze scientific and computational requirements.
4. Compare opportunities with researcher expertise.
5. Review related NIH-funded projects.
6. Explain why an opportunity may be relevant.
7. Identify expertise gaps.
8. Recommend potential collaborators.
9. Monitor deadlines and announcement changes.
10. Deliver personalized research funding intelligence.

> **The goal is not to replace researchers or research development professionals. The goal is to give them an intelligent research agent that continuously searches, analyzes, and prioritizes opportunities on their behalf.**

---

## ⚠️ Responsible Use and Disclaimer

This project is not affiliated with or endorsed by the National Institutes of Health, Grants.gov, or the U.S. Department of Health and Human Services.

The software uses publicly available official information to support funding opportunity discovery and prioritization.

Relevance scores and classifications are research-support signals only.

Always verify:

* Eligibility
* Deadlines
* Funding mechanism
* Application requirements
* Clinical or scientific scope
* Submission instructions

using the official funding opportunity announcement.

---

## 👨‍💻 Researcher & Developer

**Md. Saifur Rahman, Ph.D.**

**Research Areas:**
Artificial Intelligence • Machine Learning • Data Science • Health Analytics • Generative AI • Agentic AI

This project explores the intersection of **AI, data science, research informatics, and agentic software engineering** for improving research funding intelligence.

---

## 🤝 Collaboration

Research collaborations are welcome in:

* Agentic AI for research
* Generative AI and LLM applications
* Biomedical and public health informatics
* Research funding intelligence
* AI-assisted grant development
* Human-AI collaborative research systems

⭐ **If this research software is useful to you, consider starring the repository.**

💡 **Ideas, issues, and research collaborations are welcome.**
