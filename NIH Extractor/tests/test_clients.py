from nih_grant_matcher.clients import GrantsGovClient


class FakeGrantsGovClient(GrantsGovClient):
    def __init__(self) -> None:
        super().__init__()
        self.calls = []
    def search(self, agencies, statuses, rows=50, keyword="", start_record=0):
        self.calls.append((rows, start_record))
        if start_record == 0:
            return [{"id": i} for i in range(rows)]
        if start_record == rows:
            return [{"id": rows + i} for i in range(25)]
        return []


def test_grantsgov_search_all_paginates() -> None:
    client = FakeGrantsGovClient()
    hits = client.search_all(["HHS-NIH11"], ["posted"], limit=125)
    assert len(hits) == 125
    assert client.calls == [(100, 0), (100, 100)]

