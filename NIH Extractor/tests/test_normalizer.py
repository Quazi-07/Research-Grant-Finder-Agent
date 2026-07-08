from nih_grant_matcher.normalizer import normalize_grantsgov

def test_normalize_grantsgov_combines_search_and_detail() -> None:
    hit = {"id": "123", "number": "RFA-CA-26-001", "title": "AI for cancer imaging", "agencyCode": "HHS-NIH11", "agencyName": "National Institutes of Health", "openDate": "07/01/2026", "closeDate": "12/01/2026", "oppStatus": "posted"}
    detail = {"id": 123, "opportunityNumber": "RFA-CA-26-001", "opportunityTitle": "AI for cancer imaging", "owningAgencyCode": "HHS-NIH11", "synopsis": {"agencyName": "National Institutes of Health", "synopsisDesc": "<p>Deep learning methods for imaging analytics.</p>", "awardCeiling": "$500000", "applicantTypes": [{"description": "Public and State controlled institutions of higher education"}], "fundingInstruments": [{"description": "Grant"}], "fundingActivityCategories": [{"description": "Health"}]}}
    opportunity = normalize_grantsgov(hit, detail)
    assert opportunity.source_id == "123"
    assert opportunity.opportunity_number == "RFA-CA-26-001"
    assert opportunity.close_date is not None
    assert opportunity.award_ceiling == 500000
    assert "Deep learning" in opportunity.description
