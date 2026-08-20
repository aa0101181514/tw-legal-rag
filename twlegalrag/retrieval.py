"""Stage 1 — TLR retrieval client.

Talks to the public Taiwan Legal RAG API (default ``https://tlr.dr-lawbot.com``):

  POST /v1/search    — hybrid/keyword/phrase search over ~21M judgments.
                       Returns a structured Layer-1 *listing* per hit
                       (court / verdict / cited articles / type) plus a
                       short-lived ``result_token``. NOT reasoning text.
  POST /v1/fulltext  — given a doc_id + result_token, returns an excerpt of the
                       judgment's reasoning text (capped server-side). This is
                       what the citation check needs — the listing alone has no
                       holding text.

Design notes baked in from production experience:

* **strict=False JSON.** TLR responses embed raw control characters (full-width
  spaces, unescaped newlines from judgment text). A strict JSON parser rejects
  them — this is the same failure that breaks OpenAI's Action layer. We parse
  leniently so the CLI is robust where stricter clients are not.
* **result_token reuse.** One search returns a single token that encodes the
  whole result set; pass it back unchanged when fetching any hit's text excerpt.
* **Public, authless by default.** A Bearer key is optional — supply one only
  if the server operator issued you one (it just lets them attribute your
  traffic in their logs). Per-IP rate limiting applies regardless.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Optional

import httpx

DEFAULT_BASE_URL = "https://tlr.dr-lawbot.com"
_SEARCH_PATH = "/v1/search"
_FULLTEXT_PATH = "/v1/fulltext"
# v2.1 paging safety caps: at most this many windows / total chars per judgment.
_MAX_FULLTEXT_PAGES = 6
_MAX_FULLTEXT_CHARS = 90_000
_HEALTH_PATH = "/v1/health"


class RetrievalError(RuntimeError):
    """Raised when the TLR API cannot serve a request."""


@dataclass
class Judgment:
    """One search hit. ``fulltext``/``cited_articles`` populated after fetch_fulltext."""

    rank: int
    doc_id: str
    citation_text: str
    court_name: str
    jdate: str
    snippet: str          # Layer-1 listing line (NOT reasoning text)
    citation_url: str
    citation_markdown: str
    result_token: str
    case_category: Optional[str] = None
    # filled in by fetch_fulltext():
    fulltext: Optional[str] = None
    cited_articles: list[str] = field(default_factory=list)
    # Database-recorded appeal chain ({"upper": [...], "lower": [...], "note": str})
    # or None. An upper entry whose main_flag shows 主文含「廢棄」 means this
    # judgment was overturned on appeal — downstream models must not present it
    # as currently authoritative. Absence of an upper record means NOT COLLECTED,
    # never "final (確定)".
    case_history: Optional[dict] = None
    # v2.1 (2026-08-20 server): preview of the matched passage (why this hit
    # matched). Never a substitute for reading the full reasoning text.
    hit_excerpt: Optional[str] = None
    # v2.1: total reasoning-text length reported by the server, and whether the
    # paged fetch read it to the end. None/True on older servers.
    fulltext_total_chars: Optional[int] = None
    fulltext_complete: bool = True

    @property
    def has_fulltext(self) -> bool:
        return bool(self.fulltext)


def _loads_lenient(text: str):
    """Parse JSON tolerating embedded control characters (see module docstring)."""
    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise RetrievalError(f"TLR returned unparseable JSON: {exc}") from exc


class TLRClient:
    """Thin client over the TLR retrieval API. Carries no LLM, no DB, no keys."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = httpx.Client(timeout=timeout, follow_redirects=True)

    # -- context manager so callers can `with TLRClient() as c:` --------------
    def __enter__(self) -> "TLRClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _headers(self) -> dict:
        h = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _post(self, path: str, body: dict) -> dict:
        url = self.base_url + path
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = self._client.post(url, headers=self._headers(), json=body)
            except httpx.HTTPError as exc:
                last_exc = exc
                time.sleep(0.6 * (attempt + 1))
                continue
            if resp.status_code == 429:
                # Per-IP rate limit. Back off and retry within budget.
                if attempt < self.max_retries:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise RetrievalError(
                    "TLR rate limit hit (HTTP 429). Slow down or request an API key."
                )
            if resp.status_code == 503:
                raise RetrievalError(
                    "TLR service unavailable (HTTP 503) — the operator may have the "
                    "kill switch engaged."
                )
            data = _loads_lenient(resp.text)
            if resp.status_code >= 400:
                detail = data.get("detail", data) if isinstance(data, dict) else data
                raise RetrievalError(f"TLR error (HTTP {resp.status_code}): {detail}")
            return data
        raise RetrievalError(f"TLR request failed after retries: {last_exc}")

    # -- public API -----------------------------------------------------------
    def health(self) -> dict:
        try:
            resp = self._client.get(self.base_url + _HEALTH_PATH, headers=self._headers())
        except httpx.HTTPError as exc:
            # Same contract as _post(): callers (and the `health` command) see
            # RetrievalError, never a raw transport exception.
            raise RetrievalError(f"TLR health check failed: {exc}") from exc
        return _loads_lenient(resp.text)

    def search(
        self,
        query: str,
        *,
        search_type: str = "hybrid",
        max_results: int = 5,
    ) -> list[Judgment]:
        """Search judgments. Returns Layer-1 listings (no reasoning text yet)."""
        if search_type not in ("hybrid", "keyword", "phrase"):
            raise ValueError("search_type must be hybrid | keyword | phrase")
        max_results = max(1, min(int(max_results), 10))  # server caps at 10
        data = self._post(
            _SEARCH_PATH,
            {"query": query, "search_type": search_type, "max_results": max_results},
        )
        results = data.get("results", []) if isinstance(data, dict) else []
        # Server-side retrieval note (e.g. exact docket lookup engaged, or
        # "case number not found — do not describe the case from memory").
        # Exposed for the CLI to surface; None on older servers.
        self.last_search_note = data.get("note") if isinstance(data, dict) else None
        out: list[Judgment] = []
        for r in results:
            out.append(
                Judgment(
                    rank=r.get("rank", len(out) + 1),
                    doc_id=r.get("doc_id", ""),
                    citation_text=r.get("citation_text", ""),
                    court_name=r.get("court_name", ""),
                    jdate=r.get("jdate", ""),
                    snippet=r.get("snippet", ""),
                    citation_url=r.get("citation_url", ""),
                    citation_markdown=r.get("citation_markdown", ""),
                    result_token=r.get("result_token", ""),
                    case_category=r.get("case_category"),
                    hit_excerpt=r.get("hit_excerpt") or None,
                )
            )
        return out

    def fetch_fulltext(self, judgment: Judgment) -> Judgment:
        """Fetch the reasoning text excerpt for a hit and populate it in place.

        Required before the citation check: the search listing has no holding
        text, so the bundle-level checks have nothing to compare against.
        """
        if not judgment.result_token:
            raise RetrievalError(
                f"{judgment.doc_id}: no result_token (fetch via search() first)."
            )
        payload = {"doc_id": judgment.doc_id, "result_token": judgment.result_token}
        data = self._post(_FULLTEXT_PATH, payload)
        text = data.get("text_excerpt", "") if isinstance(data, dict) else ""

        # v2.1: page through long judgments. Servers from 2026-08-20 report
        # ``fulltext_truncated`` and accept ``excerpt_offset``; older servers
        # omit both, so this loop never runs and behavior is unchanged.
        # Each window's text_excerpt repeats the citation header (up to the
        # first blank line) — strip it from continuation windows before
        # concatenating, and advance the offset by the raw window length.
        if isinstance(data, dict) and data.get("fulltext_truncated") is True and text:
            parts = text.split("\n\n", 1)
            header, body = (parts[0] + "\n\n", parts[1]) if len(parts) == 2 else ("", text)
            offset = int(data.get("excerpt_offset") or 0) + len(body)
            pages = 1
            while (
                data.get("fulltext_truncated") is True
                and pages < _MAX_FULLTEXT_PAGES
                and len(body) < _MAX_FULLTEXT_CHARS
            ):
                try:
                    data = self._post(_FULLTEXT_PATH, {**payload, "excerpt_offset": offset})
                except RetrievalError:
                    break  # keep what we have; fulltext_complete stays False
                if not isinstance(data, dict):
                    break
                nxt = data.get("text_excerpt", "")
                nxt_body = nxt.split("\n\n", 1)[1] if "\n\n" in nxt else nxt
                if not nxt_body:
                    break
                body += nxt_body
                offset += len(nxt_body)
                pages += 1
            text = header + body

        judgment.fulltext = text
        judgment.cited_articles = (
            data.get("cited_articles") or [] if isinstance(data, dict) else []
        )
        judgment.case_history = (
            data.get("case_history") if isinstance(data, dict) else None
        )
        if isinstance(data, dict):
            judgment.fulltext_total_chars = data.get("fulltext_total_chars")
            judgment.fulltext_complete = data.get("fulltext_truncated") is not True
        return judgment

    def search_and_read(
        self,
        query: str,
        *,
        search_type: str = "hybrid",
        max_results: int = 5,
        read_top: Optional[int] = None,
    ) -> list[Judgment]:
        """Search then fetch full text for the top ``read_top`` hits (default all).

        This is the one-call retrieval the CLI uses: locate via search, then read
        reasoning text so the bundle and the citation check have real holding text.
        """
        hits = self.search(query, search_type=search_type, max_results=max_results)
        n = len(hits) if read_top is None else min(read_top, len(hits))
        for j in hits[:n]:
            try:
                self.fetch_fulltext(j)
            except RetrievalError:
                # Leave fulltext empty; the citation check degrades to
                # needs_review rather than failing on missing text.
                pass
        return hits
