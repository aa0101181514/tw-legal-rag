# Changelog

## Hosted service 2026-08-20 (no CLI release)

Server-side update to the hosted TLR endpoint; documented here because it
changes the wire responses this CLI and the Remote MCP tools consume:

- `search_bundle` responses carry a top-level `result_token`.
- Every search/bundle result carries `hit_excerpt` (matched passage).
- `get_judgment_fulltext` accepts `excerpt_offset` (paging) and returns
  `fulltext_total_chars`.
- `keyword` / `phrase` search modes now rank by BM25 relevance
  (all-terms-AND, empty on zero hits).

All additive; existing clients keep working unchanged.

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
