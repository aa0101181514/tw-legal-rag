# Changelog

## Data coverage update (2026-09-02)

Documentation only; no package or API change (still v2.3.0).

- **Administrative interpretations: 84,737 → 88,382** across **90 issuing
  agencies** (was 78). The increase is mainly commercial-registration and
  company-law interpretations from the Ministry of Economic Affairs, whose
  count went from 3,131 to 6,670.
- **Interpretation validity ledger: 50,853 → 69,461.** Coverage now includes
  tax interpretations, whose serials were previously not registered, so exact
  serial lookup reaches them.
- **Exact serial lookup is more forgiving of format variants.** A query
  written as `台勞動2字第040204號` now resolves to a record stored as
  `（87）台勞動二字第040204號函` (year prefix, Chinese numerals, leading
  zeros). Such a hit is flagged in the response so the caller re-checks the
  returned serial and title before citing. Exact matches always take priority.
- **Court judgments: 22,558,169 → 22,563,805** (daily incremental sync).

## v2.3.0 (2026-09-01)

The CLI now reaches all six hosted tools. The server side for statutes and
interpretations shipped in 2026-08 and 2026-09-01; this release adds the
matching CLI commands (retrieval only, no LLM, same as the rest of the CLI):

- **New `law` command**: exact current-statute article lookup
  (`twlegalrag law 民法 184`). Current version only; when the article or the
  law name is not found the server returns explicit notes and law-name
  candidates instead of an empty result.
- **New `ref` command**: exact agency-interpretation lookup by serial with
  validity status passthrough (`--full` prints the stored fulltext).
- **New `ref-search` command**: semantic topic search over agency
  interpretations, listing only. Relevance judgment and citation stay with
  your AI: read the excerpts, then verify serials with `ref`.

## v2.2.0 (2026-08-23)

Hosted endpoint moved to the Dr.Legal domain:

- **Default TLR base URL is now `https://tlr.dr-legal.com.tw`** (CLI default,
  `TWLEGALRAG_TLR_BASE_URL` fallback, `server.json` remote, all docs).
- **The previous endpoint `https://tlr.dr-lawbot.com` keeps working** and is
  not scheduled for removal. Existing installs, config files, and MCP clients
  pointing at it need no change. Each hostname serves its own OAuth discovery
  metadata, so clients on either one complete the flow against the host they
  connected to.
- `server.json` version aligned with the package version.

## v2.1.0 (2026-08-20)

CLI support for the 2026-08-20 hosted-service capabilities:

- **`pack` reads long judgments to the end.** `fetch_fulltext` now pages
  through the server's excerpt windows (`excerpt_offset`), so late sections of
  long judgments are no longer cut off. Older servers: single window, behavior
  unchanged.
- **Per-judgment bundle budget doubled** (6,000 → 12,000 chars) to carry the
  extra text; bundles gain `fulltext_total_chars` so downstream models know
  how much of the judgment they received.
- **`hit_excerpt` in bundles** — the matched-passage preview returned by the
  server is included per judgment (never a substitute for the reasoning text).
- New `Judgment` fields: `hit_excerpt`, `fulltext_total_chars`,
  `fulltext_complete`.

## Hosted service 2026-08-20 (no CLI release)

Server-side update to the hosted TLR endpoint (all additive; existing clients
keep working unchanged):

- `search_bundle` responses carry a top-level `result_token`.
- Results carry `hit_excerpt` (matched-passage preview).
- `get_judgment_fulltext` accepts `excerpt_offset` (paging) and returns
  `fulltext_total_chars`.
- Lexical search modes (`keyword` / `phrase`) improved.

## v2.0.0 (2026-08-09)

### License change

- **v2.0.0 and later: Elastic License 2.0 (ELv2).** Free to use, copy,
  modify and redistribute — including commercial and internal-business use.
  Two limits: no offering the software itself as a hosted/managed service to
  third parties, and no removing license/notice protections.
- **Versions up to v1.2.2 remain MIT** (that grant is perpetual for those
  versions).
- The hosted API (`tlr.dr-lawbot.com`) and the judgment corpus were never
  covered by the code license; their terms are now written down in
  `TERMS.md`.
- Project names and logos are not licensed — see `TRADEMARK.md`.

### Contribution policy

- The project now maintains a **single-author codebase**: issues are
  welcome, external pull requests are not accepted (see `CONTRIBUTING.md`).
- Third-party code from PRs #9, #10 and #13 was removed and the underlying
  issues re-fixed first-party (thanks to @MrFrogIsMe, @jimwellh and
  @xianzuyang9-blip for the reports and original fixes; those remain part
  of the MIT-licensed v1.2.x line).

### Fixed (first-party reimplementations)

- `health()` wraps transport errors into `RetrievalError` (#1)
- `check` reads the answer file defensively instead of crashing (#2)
- `search` / `pack` validate `-n` at the CLI boundary (1-10) (#3)
- `config.toml` is honoured on Python 3.9/3.10 via the `tomli` backport (#5)
- `check` rejects JSON files that are not a `twlegalrag.bundle/` bundle (#6)
- pytest is confined to `tests/` via `testpaths` (#7)

### Added

- Rewritten Claude Code skill (`skills/tw-legal-rag/`)
- `tests/test_config.py` covering the config-loading contract

## v1.2.2 (2026-08-05)

- MCP Server Registry manifest (`server.json`) + PyPI ownership marker.
- Last MIT-licensed release line (v1.2.x).

## v1.2.0 (2026-07-18)

- Community round: error handling and input validation (#9), Claude Code
  skill (#10), tomli fallback (#13); Windows cp950 fix; version single
  source (#14).

## v1.1.0 and earlier

- See git history.
