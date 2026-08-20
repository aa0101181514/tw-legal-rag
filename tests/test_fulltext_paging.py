"""Offline tests for v2.1 full-text paging (no network)."""

from twlegalrag.retrieval import TLRClient, Judgment


def _j():
    return Judgment(
        rank=1, doc_id="XXDM,100,X,1,20110101", citation_text="某案",
        court_name="某法院", jdate="2011-01-01", snippet="", citation_url="",
        citation_markdown="", result_token="tok",
    )


HEADER = "引用連結: [某案](https://example.invalid)\n引用字號: 某案\n\n"


def _client_with_pages(pages):
    """TLRClient whose _post replays canned fulltext responses, recording calls."""
    c = TLRClient.__new__(TLRClient)
    calls = []

    def fake_post(path, payload):
        calls.append(payload)
        return pages[min(len(calls) - 1, len(pages) - 1)]

    c._post = fake_post  # type: ignore[attr-defined]
    return c, calls


def test_old_server_single_window_unchanged():
    pages = [{"text_excerpt": HEADER + "甲" * 100, "cited_articles": []}]
    c, calls = _client_with_pages(pages)
    j = c.fetch_fulltext(_j())
    assert j.fulltext == HEADER + "甲" * 100
    assert j.fulltext_complete is True
    assert len(calls) == 1
    assert "excerpt_offset" not in calls[0]


def test_paged_fetch_concatenates_and_strips_headers():
    body1, body2 = "甲" * 50, "乙、後段理由"
    pages = [
        {"text_excerpt": HEADER + body1, "fulltext_truncated": True,
         "excerpt_offset": 0, "fulltext_total_chars": 50 + len(body2)},
        {"text_excerpt": HEADER + body2, "fulltext_truncated": False,
         "excerpt_offset": 50, "fulltext_total_chars": 50 + len(body2),
         "cited_articles": ["刑法第359條"]},
    ]
    c, calls = _client_with_pages(pages)
    j = c.fetch_fulltext(_j())
    assert j.fulltext == HEADER + body1 + body2          # header once, bodies joined
    assert calls[1]["excerpt_offset"] == 50              # offset = raw window length
    assert j.fulltext_complete is True
    assert j.fulltext_total_chars == 50 + len(body2)
    assert j.cited_articles == ["刑法第359條"]           # metadata from last window


def test_paging_stops_at_cap_and_marks_incomplete():
    big = "丙" * 30000
    page = {"text_excerpt": HEADER + big, "fulltext_truncated": True,
            "excerpt_offset": 0, "fulltext_total_chars": 999999}
    c, calls = _client_with_pages([page])
    j = c.fetch_fulltext(_j())
    assert j.fulltext_complete is False                  # still truncated at stop
    assert len(calls) <= 6                               # page cap respected
    assert len(j.fulltext) <= len(HEADER) + 30000 * 6
