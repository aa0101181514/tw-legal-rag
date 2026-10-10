# Changelog

## Data coverage update (2026-10-10)

Documentation-only change; no package release (CLI still v2.3.0).

- **Labour arbitration decisions: 400 to 465.** Ten decisions published since May 2026
  (114 年勞裁字第 36、38、45、47、53、56、57、58 號 and 115 年勞裁字第 4、6 號) and fifty-five
  decisions from 2011 and 2012 (100 and 101 年) are now included. The collection is
  refreshed weekly from the 勞動部不當勞動行為裁決委員會 public query page.
- **Constitutional Court judgments: 57 to 59** (115 年憲判字第 6 號 and 第 7 號); the
  constitutional row is now 872. Constitutional Court judgments are checked weekly.
- **Court judgments: 22,663,802 to 22,674,799.** Court-level rows: 地方法院 17,083,731,
  地方法院簡易庭 3,327,891, 高等法院及分院 1,355,772, 最高法院 405,325, 高等行政法院 202,960,
  最高行政法院 124,161, 地方行政訴訟庭 92,599, 高雄少年及家事法院 24,977, 智慧財產及商業法院
  24,092, 其他專業法庭・委員會 33,291. Case-type rows: 民事 14,550,390, 刑事 7,507,814,
  行政 591,068, 其他 25,527.
- **Administrative rules and interpretations: 102,950 to 103,029** (still 93 agencies).
  財政部 10,659, 經濟部智慧財產局 7,185, 經濟部 6,677, 主計總處 721 (now listed above
  公務人員保障暨培訓委員會).
- **Acts: 1,018 to 1,022 (44,503 articles). Regulations: 7,253 to 7,254 (128,781
  articles).** Repealed instruments unchanged at 3,525.
- **Interpretation validity ledger: 69,616 to 80,339.**
- **Appeal-chain relations: 4,550,703 to 4,366,833**, following a re-audit of the relation
  set against the Judicial Yuan appeal-history lists.

## Data coverage update (2026-10-08)

Documentation-only change; no package release (CLI still v2.3.0).

- **Administrative rules and interpretations: 88,459 to 102,950; agencies 90 to 93.**
  Eight more agency statute systems (主管法規查詢系統) are now collected weekly:
  金融監督管理委員會, 教育部, 文化部, 環境部, 考試院, 僑務委員會, 外交部, 大陸委員會
  (14,467 regulations and administrative rules added on 2026-10-08). Largest rows now:
  金管會 8,383 (law.fsc.gov.tw 法規命令與行政規則 5,525 新收), 考試院 3,373, 教育部 2,911, 文化部 1,516, 環境部 1,112, 僑務委員會 184, 外交部 134, 大陸委員會 52.
- Every administrative source now carries an explicit category (行政函釋 or 行政命令), so
  all 93,857 admin rows are reachable through `search_legal_references`; previously
  uncategorized rows (for example 法務部 and 經濟部智慧財產局 interpretations) were
  indexed but not returned by that tool.
- Full texts from the statute-system crawlers are now stripped of site navigation and
  footer text at crawl time; 22,041 existing rows were re-cleaned and re-embedded.
- **Court judgments: 22,649,339 to 22,663,802.** Court-level rows: 地方法院 17,075,529, 地方法院簡易庭 3,326,486, 高等法院及分院 1,355,046, 最高法院 405,247, 高等行政法院 202,904, 最高行政法院 124,117, 地方行政訴訟庭 92,229, 高雄少年及家事法院 24,870, 智慧財產及商業法院 24,085, 其他專業法庭・委員會 33,289. Case-type rows: 民事 14,543,715, 刑事 7,503,965, 行政 590,597, 其他 25,525.
- **Interpretation validity ledger: 69,593 to 69,616.**
- **Appeal-chain relations: 4,549,699 to 4,550,703.**
- Statute, constitutional-tier and labor-decision counts unchanged (statute dataset still
  the official release of 2026-09-24).

## Data coverage update (2026-10-04)

Documentation-only change; no package release (CLI still v2.3.0).

- **Court judgments: 22,617,802 to 22,649,339.** Court-level rows: 地方法院
  17,063,984, 地方法院簡易庭 3,325,054, 高等法院及分院 1,354,426, 最高法院
  405,029, 高等行政法院 202,855, 最高行政法院 124,056, 地方行政訴訟庭 91,776,
  高雄少年及家事法院 24,812, 智慧財產及商業法院 24,079, 其他專業法庭・委員會
  33,268. Case-type rows: 民事 14,534,450, 刑事 7,499,351, 行政 590,034,
  其他 25,504.
- **Statutes: act articles 44,396 to 44,399; regulation articles 128,744 to
  128,749.** Instrument counts unchanged (acts 1,018, regulations 7,253,
  repealed 3,525); the statute corpus corresponds to the official dataset
  release of 2026-09-24.
- **Administrative interpretations: 88,438 to 88,459** (財政部 10,647, 法務部
  7,089, 農業部 3,084, 法務部行政執行署 1,417, 國科會 570, 文化部 206,
  個人資料保護委員會籌備處 74); still 90 agencies.
- **Interpretation validity ledger: 69,543 to 69,593.**
- **Appeal-chain relations: 4,544,682 to 4,549,699.**
- Constitutional-tier and labor-decision counts unchanged.
- Wording: one 身份 corrected to 身分 in the Chinese README.

## Statute lookup: dataset version + data coverage update (2026-09-23)

Hosted-server and documentation change; no package release (CLI still v2.3.0,
which already prints the new note through `law`).

- **`get_law_article` / `POST /v1/law_article` now returns `dataset_version`**
  on every match: the release date of the official 全國法規資料庫 dataset the
  statute corpus corresponds to (`2026-09-11` at the time of writing). `notes`
  also states the version in prose. Amendments promulgated after that date are
  not yet in the corpus, so compare the official last-amendment date before
  citing. The statute corpus is now checked against the official dataset daily
  and re-imported whenever a new release appears (the official cadence is
  roughly weekly); previously it was refreshed on a fixed twice-monthly schedule.
- **Court judgments: 22,613,130 to 22,617,802.** Every record now carries a
  court code, so the "no court-code field" bucket (450,063 in the previous
  snapshot) is gone and all court-level rows are updated: 地方法院 17,039,112,
  地方法院簡易庭 3,321,646, 高等法院及分院 1,352,908, 最高法院 404,588,
  高等行政法院 202,701, 最高行政法院 124,006, 地方行政訴訟庭 91,061,
  高雄少年及家事法院 24,632, 智慧財產及商業法院 24,050, 其他專業法庭・委員會
  33,098. Case-type rows updated accordingly (民事 14,515,015, 刑事 7,488,340,
  行政 588,944, 其他 25,503).
- **Statutes: acts 1,017 to 1,018 (44,372 to 44,396 articles); regulations
  7,254 to 7,253 (128,749 to 128,744 articles); repealed instruments 3,523 to
  3,525.** Constitutional-tier counts unchanged.
- **Administrative interpretations: 88,437 to 88,438** (勞動部 7,164 to 7,165).
- **Interpretation validity ledger: 69,542 to 69,543.**
- **Appeal-chain relations: 4,544,095 to 4,544,682.**
- Labor-decision count unchanged.

## Data coverage update (2026-09-22)

Documentation only; no package or API change (still v2.3.0).

- **Court judgments: 22,578,975 to 22,613,130** (daily incremental sync
  resumed). As in the 2026-09-08 update, the entire increase lands in the
  "no court-code field" bucket (415,908 to 450,063, an exact match with the
  34,155 new records), so the court-level and case-type tables are unchanged.
- **Administrative interpretations: 88,421 to 88,437** across the same 90
  agencies (財政部 10,639 to 10,642, 金管會 2,844 to 2,850, 銓敘部 3,991 to
  3,994, and one each for 法務部, 農業部, 法務部矯正署 and 環境部).
- **Regulations (命令): 7,249 to 7,254 instruments, 128,675 to 128,749
  articles.** Acts, constitutional-tier instruments and repealed counts are
  unchanged.
- **Interpretation validity ledger: 69,509 to 69,542.**
- **Appeal-chain relations: 4,540,466 to 4,544,095.**
- Labor-decision count unchanged.

## Data coverage update (2026-09-13)

Documentation only; no package or API change (still v2.3.0).

- **Court judgments: unchanged at 22,578,975.** No new upstream batches were
  ingested in this window, so the court-level and case-type tables are
  identical to the 2026-09-08 snapshot.
- **Administrative interpretations: 88,392 to 88,421** across the same 90
  agencies. Eight agencies gained between one and eleven records
  (經濟部智慧財產局 7,162 to 7,173, 勞動部 7,155 to 7,164, 經濟部 6,671 to
  6,674, 內政部 2,665 to 2,667, and one each for 財政部, 農業部,
  原住民族委員會 and 文化部).
- **Interpretation validity ledger: 69,483 to 69,509.**
- Statute, repealed-instrument, labor-decision and appeal-chain counts are
  unchanged.

## Data coverage update (2026-09-08)

Documentation only; no package or API change (still v2.3.0).

- **Court judgments: 22,563,805 to 22,578,975** (daily incremental sync).
  As in the previous two updates, the entire increase lands in the
  "no court-code field" bucket (400,738 to 415,908, an exact match with the
  delta). The ten court-level rows and four case-type rows are unchanged;
  the daily sync does not populate the `court` field, and the cleanup is
  still outstanding.
- **Statute counts now come from the `laws` table, split by tier and repeal
  status.** Previous figures did not reconcile with the production tables:
  acts 1,083 to 1,017 (45,620 to 44,372 articles), regulations 7,474 to
  7,249 (132,760 to 128,675 articles). Constitutional-tier instruments are
  now listed as the 7 that exist in the database (228 articles: the
  Constitution, its additional articles, the implementation procedure and
  the martial-law orders) rather than the Constitution alone.
- **Repealed instruments: 3,230 to 3,523** (320 acts, 3,201 regulations,
  2 constitutional-tier), consistent with the same table and tier split.
- **Administrative interpretations: 88,382 to 88,392** across the same 90
  agencies; seven agencies gained between one and three records.
- **Interpretation validity ledger: 69,461 to 69,483.**
- **Appeal-chain relations: 4,537,220 to 4,540,466.** This row now uses an
  exact `count(*)`; the earlier figure came from `pg_class.reltuples`, a
  planner estimate that drifts with vacuum and had understated the table.

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
