"""HTTP 401 must surface as plain guidance, not a raw error payload.

Since 2026-10-30 the REST endpoint requires a credential. A fresh install with
no key should tell the user where to get one.
"""

import pytest

from twlegalrag.retrieval import KEYS_PAGE, RetrievalError, TLRClient


class _Resp:
    status_code = 401
    text = '{"detail": {"error": "authentication_required"}}'


class _Http:
    def post(self, url, headers=None, json=None):
        return _Resp()


def _client(api_key):
    c = TLRClient.__new__(TLRClient)
    c.base_url = "https://example.invalid"
    c.api_key = api_key
    c.timeout = 1.0
    c.max_retries = 0
    c._client = _Http()
    return c


def test_401_without_key_points_to_keys_page():
    with pytest.raises(RetrievalError) as e:
        _client(None)._post("/v1/search", {"query": "x"})
    msg = str(e.value)
    assert KEYS_PAGE in msg
    assert "TWLEGALRAG_TLR_API_KEY" in msg
    assert "尚未設定" in msg
    assert "authentication_required" not in msg  # no raw payload dump


def test_401_with_key_says_credential_rejected():
    with pytest.raises(RetrievalError) as e:
        _client("tlr_bad")._post("/v1/search", {"query": "x"})
    msg = str(e.value)
    assert "拒絕了目前的憑證" in msg
    assert KEYS_PAGE in msg
    assert "tlr_bad" not in msg  # never echo the credential
