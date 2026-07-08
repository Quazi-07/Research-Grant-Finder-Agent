from __future__ import annotations

import html
import zipfile
from datetime import date, datetime
from pathlib import Path
from .models import ScoredOpportunity

HEADERS = ["Rank", "Classification", "Score", "Opportunity Number", "Title", "Agency", "Status", "Open Date", "Close Date", "Award Ceiling", "Matched Terms", "Why It Matched", "Summary", "Source URL"]

def write_excel(items: list[ScoredOpportunity], path: str | Path, min_score: float = 35.0) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = _rows(items, min_score=min_score)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _content_types())
        archive.writestr("_rels/.rels", _root_rels())
        archive.writestr("docProps/core.xml", _core_props())
        archive.writestr("docProps/app.xml", _app_props())
        archive.writestr("xl/workbook.xml", _workbook())
        archive.writestr("xl/_rels/workbook.xml.rels", _workbook_rels())
        archive.writestr("xl/styles.xml", _styles())
        archive.writestr("xl/worksheets/sheet1.xml", _worksheet(rows))
    return path

def _rows(items: list[ScoredOpportunity], min_score: float) -> list[list[object]]:
    included = [item for item in items if item.score >= min_score]
    rows: list[list[object]] = [["NIH Grant Opportunity Matcher", None, None, None, None, None, None, None, None, None, None, None, None, None], [f"Generated {datetime.now():%Y-%m-%d %H:%M}", None, None, None, None, None, None, None, None, None, None, None, None, None], [f"Minimum score: {min_score:g}", None, None, None, None, None, None, None, None, None, None, None, None, None], [], HEADERS]
    for rank, scored in enumerate(included, start=1):
        opp = scored.opportunity
        rows.append([rank, scored.classification, scored.score, opp.opportunity_number, opp.title, opp.agency_name or opp.agency_code, opp.status, opp.open_date, opp.close_date, opp.award_ceiling, ", ".join(scored.matched_terms), "; ".join(scored.reasons), _summary(opp.description), opp.source_url])
    return rows

def _worksheet(rows: list[list[object]]) -> str:
    sheet_data = []
    for row_idx, row in enumerate(rows, start=1):
        cells = []
        for col_idx, value in enumerate(row, start=1):
            ref = f"{_col(col_idx)}{row_idx}"
            cells.append(_cell(ref, value, _style_for(row_idx, col_idx)))
        sheet_data.append(f'<row r="{row_idx}">{"".join(cells)}</row>')
    last_row = max(len(rows), 5)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="A1:N{last_row}"/>
  <sheetViews><sheetView showGridLines="0" workbookViewId="0"><pane ySplit="5" topLeftCell="A6" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
  <sheetFormatPr defaultRowHeight="16"/>
  <cols><col min="1" max="1" width="8" customWidth="1"/><col min="2" max="3" width="14" customWidth="1"/><col min="4" max="4" width="22" customWidth="1"/><col min="5" max="5" width="42" customWidth="1"/><col min="6" max="7" width="24" customWidth="1"/><col min="8" max="9" width="14" customWidth="1"/><col min="10" max="10" width="16" customWidth="1"/><col min="11" max="12" width="38" customWidth="1"/><col min="13" max="13" width="60" customWidth="1"/><col min="14" max="14" width="48" customWidth="1"/></cols>
  <sheetData>{"".join(sheet_data)}</sheetData>
  <autoFilter ref="A5:N{last_row}"/>
  <mergeCells count="3"><mergeCell ref="A1:N1"/><mergeCell ref="A2:N2"/><mergeCell ref="A3:N3"/></mergeCells>
</worksheet>'''

def _cell(ref: str, value: object, style: int) -> str:
    if value is None:
        return f'<c r="{ref}" s="{style}"/>'
    if isinstance(value, (int, float)):
        return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'
    if isinstance(value, date):
        serial = (value - date(1899, 12, 30)).days
        return f'<c r="{ref}" s="{style}"><v>{serial}</v></c>'
    text = html.escape(str(value), quote=False)
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t>{text}</t></is></c>'

def _style_for(row_idx: int, col_idx: int) -> int:
    if row_idx == 1:
        return 1
    if row_idx in (2, 3):
        return 2
    if row_idx == 5:
        return 3
    if col_idx in (8, 9):
        return 4
    if col_idx == 10:
        return 5
    if col_idx in (5, 11, 12, 13, 14):
        return 6
    return 0

def _styles() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><numFmts count="2"><numFmt numFmtId="164" formatCode="yyyy-mm-dd"/><numFmt numFmtId="165" formatCode="$#,##0"/></numFmts><fonts count="4"><font><sz val="10"/><name val="Aptos"/></font><font><b/><sz val="16"/><color rgb="FFFFFFFF"/><name val="Aptos Display"/></font><font><sz val="10"/><color rgb="FF475569"/><name val="Aptos"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Aptos"/></font></fonts><fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF0F766E"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FF155E75"/></patternFill></fill></fills><borders count="2"><border/><border><bottom style="thin"><color rgb="FFD6DEE4"/></bottom></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="7"><xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFill="1" applyFont="1"><alignment vertical="center"/></xf><xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/><xf numFmtId="0" fontId="3" fillId="3" borderId="0" xfId="0" applyFill="1" applyFont="1"><alignment horizontal="center"/></xf><xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/><xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/><xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>'''

def _content_types() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''

def _root_rels() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''

def _workbook_rels() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''

def _workbook() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Ranked Opportunities" sheetId="1" r:id="rId1"/></sheets></workbook>'''

def _core_props() -> str:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>NIH Grant Opportunity Matcher Results</dc:title><dc:creator>NIH Grant Opportunity Matcher</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>'''

def _app_props() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>NIH Grant Opportunity Matcher</Application></Properties>'''

def _summary(description: str, max_chars: int = 600) -> str:
    clean = " ".join(description.split())
    return clean if len(clean) <= max_chars else clean[:max_chars].rsplit(" ", 1)[0] + "..."

def _col(index: int) -> str:
    label = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        label = chr(65 + remainder) + label
    return label

