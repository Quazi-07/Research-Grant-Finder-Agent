from datetime import date
import zipfile
from nih_grant_matcher.excel import write_excel
from nih_grant_matcher.models import Opportunity
from nih_grant_matcher.scoring import MLRelevanceScorer

def test_write_excel_creates_xlsx(tmp_path) -> None:
    opportunity = Opportunity(source_id="x1", opportunity_number="RFA-X1", title="Machine learning for clinical prediction", agency_code="HHS-NIH11", agency_name="National Institutes of Health", status="posted", close_date=date(2026, 12, 1), description="Machine learning and data analysis for EHR prediction.", source_url="https://www.grants.gov/search-results-detail/1")
    scored = MLRelevanceScorer().score(opportunity, today=date(2026, 7, 6))
    output = write_excel([scored], tmp_path / "results.xlsx", min_score=0)
    assert output.exists()
    assert zipfile.is_zipfile(output)
    with zipfile.ZipFile(output) as archive:
        assert "xl/worksheets/sheet1.xml" in archive.namelist()
        sheet = archive.read("xl/worksheets/sheet1.xml").decode("utf-8")
    assert "Machine learning for clinical prediction" in sheet

