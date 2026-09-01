"""Offline tests for the statute / interpretation client methods and CLI commands.

Same pattern as test_fulltext_paging.py: build a TLRClient without __init__ and
substitute a fake ``_post`` so no network is touched.
"""

from __future__ import annotations

from typer.testing import CliRunner

import twlegalrag.cli as cli_mod
from twlegalrag.cli import app
from twlegalrag.retrieval import TLRClient


def _fake_client(responses: dict):
    c = TLRClient.__new__(TLRClient)
    c.calls = []

    def _post(path, body):
        c.calls.append((path, body))
        return responses[path]

    c._post = _post
    c.close = lambda: None
    return c


# ---------------------------------------------------------------------------
# client methods: payload shape
# ---------------------------------------------------------------------------

def test_legal_reference_payload_minimal():
    c = _fake_client({"/v1/legal_reference": {"found": False, "matches": [], "notes": []}})
    out = c.legal_reference("台財稅第881945861號")
    assert out["found"] is False
    path, body = c.calls[0]
    assert path == "/v1/legal_reference"
    assert body == {"serial": "台財稅第881945861號"}  # authority omitted when None


def test_legal_reference_payload_with_authority():
    c = _fake_client({"/v1/legal_reference": {"found": False, "matches": [], "notes": []}})
    c.legal_reference("台財稅第881945861號", authority="財政部")
    _, body = c.calls[0]
    assert body["authority"] == "財政部"


def test_search_legal_references_clamps_max_results():
    c = _fake_client({"/v1/legal_references/search": {"results": []}})
    c.search_legal_references("q", max_results=99)
    c.search_legal_references("q", max_results=0)
    assert c.calls[0][1]["max_results"] == 10
    assert c.calls[1][1]["max_results"] == 1


def test_search_legal_references_optional_filters_omitted():
    c = _fake_client({"/v1/legal_references/search": {"results": []}})
    c.search_legal_references("q")
    _, body = c.calls[0]
    assert "authority" not in body and "source_kind" not in body
    c.search_legal_references("q", authority="財政部", source_kind="tax_interpretation")
    _, body2 = c.calls[1]
    assert body2["authority"] == "財政部"
    assert body2["source_kind"] == "tax_interpretation"


def test_law_article_payload():
    c = _fake_client({"/v1/law_article": {"found": True, "matches": [], "notes": []}})
    c.law_article("民法", "184")
    path, body = c.calls[0]
    assert path == "/v1/law_article"
    assert body == {"law_name": "民法", "article_no": "184"}


# ---------------------------------------------------------------------------
# CLI rendering: must not crash on found / not-found shapes
# ---------------------------------------------------------------------------

runner = CliRunner()

_LAW_FOUND = {
    "found": True,
    "matches": [{
        "law_name": "民法", "pcode": "B0000001", "law_level": "法律",
        "law_modified_date": "2021-01-20",
        "law_url": "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=B0000001",
        "abolished": False, "article_no": "第184條",
        "article_content": "因故意或過失,不法侵害他人之權利者,負損害賠償責任。",
        "article_content_truncated": False,
    }],
    "law_candidates": [], "notes": ["條文為現行版本"],
}

_LAW_NOT_FOUND = {
    "found": False, "matches": [],
    "law_candidates": [{"law_name": "中華民國刑法", "law_level": "法律"}],
    "notes": ["法規名稱查無"],
}

_REF_FOUND = {
    "found": True,
    "matches": [{
        "canonical_id": "財政部:台財稅第881945861號", "authority": "財政部",
        "serial_no": "台財稅第881945861號", "source_kind": "admin_ruling",
        "title": "測試標題", "issue_date": "88.09.22", "status": "active_verified",
        "status_effective_at": None, "superseded_by": None,
        "status_source_url": "https://example.gov.tw", "last_verified_at": "2026-08-04",
        "source_url": "https://example.gov.tw", "fulltext": "全文內容",
        "fulltext_truncated": False, "copies": 1,
    }],
    "notes": ["此為行政函釋資料"],
}

_REFSEARCH_HITS = {
    "results": [{
        "citation": "財政部 台財稅第881945861號", "canonical_id": "財政部:台財稅第881945861號",
        "authority": "財政部", "serial_no": "台財稅第881945861號", "title": "測試標題",
        "issue_date": "1999-09-22", "source_kind": "tax_interpretation",
        "status": "unknown", "score": 0.77, "related_laws": [],
        "excerpt": "命中段落文字", "fulltext_chars": 300,
    }],
    "notes": [],
}


def _patched_client(monkeypatch, responses):
    fake = _fake_client(responses)
    monkeypatch.setattr(cli_mod, "_client", lambda: fake)
    return fake


def test_cli_law_found(monkeypatch):
    _patched_client(monkeypatch, {"/v1/law_article": _LAW_FOUND})
    r = runner.invoke(app, ["law", "民法", "184"])
    assert r.exit_code == 0, r.output
    assert "第184條" in r.output
    assert "損害賠償" in r.output


def test_cli_law_not_found_shows_candidates(monkeypatch):
    _patched_client(monkeypatch, {"/v1/law_article": _LAW_NOT_FOUND})
    r = runner.invoke(app, ["law", "刑法", "185-4"])
    assert r.exit_code == 0, r.output
    assert "查無" in r.output
    assert "中華民國刑法" in r.output


def test_cli_ref_found_with_full(monkeypatch):
    _patched_client(monkeypatch, {"/v1/legal_reference": _REF_FOUND})
    r = runner.invoke(app, ["ref", "台財稅第881945861號", "--full"])
    assert r.exit_code == 0, r.output
    assert "active_verified" in r.output
    assert "全文內容" in r.output


def test_cli_ref_search_table_and_reminder(monkeypatch):
    _patched_client(monkeypatch, {"/v1/legal_references/search": _REFSEARCH_HITS})
    r = runner.invoke(app, ["ref-search", "扣繳義務人處罰", "-n", "3", "--excerpt"])
    assert r.exit_code == 0, r.output
    assert "台財稅第881945861號" in r.output
    assert "命中段落" in r.output
