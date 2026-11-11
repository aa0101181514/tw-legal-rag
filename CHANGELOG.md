# Changelog

## v2.3.3 (2026-11-11)

- **Judgment-date and court filters.** `search` and `pack` accept `--from` / `--to` (judgment date, YYYY-MM-DD), `--court` (full court name) and `--newest` (most recent first). `TLRClient.search()` / `search_and_read()` take the matching `date_from`, `date_to`, `court`, `sort` arguments; the hosted MCP tools `search_judgments` and `search_bundle` accept the same four optional inputs. Dates written inside the query text do not filter by date. See `docs/mcp-anchor.md`.
- Hosted service fixes on the same day: a query such as "court name + 115年10月 + keywords" is no longer treated as a case number; `get_law_article` accepts 台 for 臺 in statute names; summary-court judgments now carry the correct parent district court name.

## Data coverage update (2026-11-11)

Documentation-only change; no package release (CLI still v2.3.2).

- **Court judgments: 22,770,604 to 22,795,389** (+24,785). Court-level rows: 地方法院 17,176,339, 地方法院簡易庭 3,341,870, 高等法院及分院 1,363,241, 最高法院 406,823, 高等行政法院 203,478, 最高行政法院 124,470, 地方行政訴訟庭 95,634, 其他專業法庭・委員會 33,569, 高雄少年及家事法院 25,751, 智慧財產及商業法院 24,214. Case-type rows: 民事 14,623,447, 刑事 7,551,203, 行政 594,940, 其他 25,799.
- **Administrative rules and interpretations: 107,771 to 107,889**; issuing agencies unchanged at 107.
- **Regulations in force: 7,254 to 7,255 instruments, 128,745 to 128,753 articles.** Appeal-chain relations: 4,381,229 to 4,384,977. Interpretation validity ledger: 84,831 to 84,966. Labour arbitration decisions: 465 to 466.

## v2.3.2 (2026-11-06)

- **CLI: HTTP 401 now prints plain guidance.** Since 2026-10-30 the REST endpoint requires a credential.
  A command run without one used to print the raw error payload; it now says where to create a connection
  key (`https://dr-legal.com.tw/mcp/keys`, free after signing in) and how to set `TWLEGALRAG_TLR_API_KEY`.
  A rejected credential gets its own message. The credential itself is never echoed.
- **Docs:** each README opens with a quick-connect section (MCP endpoint, Claude directory link, one-line
  commands for Claude Code and Codex). The configuration sections describe self-serve connection keys.
  The Chinese README states that current statute articles are served by `get_law_article`.
- **Package metadata:** PyPI summary and keywords, and the MCP Registry description, now name the service
  as a Taiwan law MCP server.

## Data coverage update (2026-11-04)

Documentation-only change; no package release (CLI still v2.3.1).

- **Court judgments: 22,761,622 to 22,770,604** (+8,982). Court-level rows: 地方法院 17,157,654,
  地方法院簡易庭 3,338,826, 高等法院及分院 1,361,428, 最高法院 406,537,
  高等行政法院 203,379, 最高行政法院 124,414, 地方行政訴訟庭 95,050,
  高雄少年及家事法院 25,590, 智慧財產及商業法院 24,189,
  其他專業法庭・委員會 33,537. Case-type rows: 民事 14,608,812, 刑事 7,541,824,
  行政 594,201, 其他 25,767.
- **Appeal-chain relations: 4,380,929 to 4,381,229.** Statutes and regulations, administrative rules and interpretations (107,771, 107 agencies),
  constitutional decisions, labour arbitration decisions and the interpretation validity ledger unchanged.

## Data coverage update (2026-10-30)

Documentation-only change; no package release (CLI still v2.3.1).

- **Court judgments: 22,747,053 to 22,761,622** (+14,569). Court-level rows: 地方法院 17,150,511,
  地方法院簡易庭 3,337,915, 高等法院及分院 1,361,004, 最高法院 406,427,
  高等行政法院 203,338, 最高行政法院 124,401, 地方行政訴訟庭 94,843,
  高雄少年及家事法院 25,542, 智慧財產及商業法院 24,167,
  其他專業法庭・委員會 33,474. Case-type rows: 民事 14,602,694, 刑事 7,539,285,
  行政 593,939, 其他 25,704.
- **Regulations in force: 7,253 to 7,254 instruments, 128,738 to 128,745 articles.** Appeal-chain relations: 4,378,841 to 4,380,929.
  Administrative rules and interpretations (107,771, 107 agencies), acts, repealed instruments, constitutional decisions,
  labour arbitration decisions and the interpretation validity ledger unchanged.

## Access change (2026-10-30)

Service-side change; no package release (CLI still v2.3.1).

- **MCP authorization now requires signing in to a Dr.Legal account** (Google or email; free registration).
  Existing connections keep working until their current authorization expires (at most 30 days); the tool
  then shows the sign-in page once. Active connections stay signed in; 30 days of inactivity require
  signing in again.
- **The public REST endpoint no longer accepts anonymous requests.** Send a Bearer credential: an
  institutional API key (request by email at info@dr-legal.com.tw) or an OAuth access token obtained with
  the authorization-code + PKCE flow against `https://tlr.dr-legal.com.tw`. Anonymous requests receive
  HTTP 401 with instructions in the body. For the CLI set `TWLEGALRAG_TLR_API_KEY`. A standard-library
  OAuth example for your own scripts is in `docs/tlr_oauth_cli.py`.
- Health check and OAuth discovery endpoints remain public. Terms and privacy notice: dr-legal.com.tw/tlr-terms,
  dr-legal.com.tw/tlr-privacy.

## Data coverage update (2026-10-27)

Documentation-only change; no package release (CLI still v2.3.1).

- **Court judgments: 22,729,045 to 22,747,053** (+18,008). Court-level rows: 地方法院 17,139,047,
  地方法院簡易庭 3,336,358, 高等法院及分院 1,360,144, 最高法院 406,325,
  高等行政法院 203,269, 最高行政法院 124,391, 地方行政訴訟庭 94,460,
  高雄少年及家事法院 25,442, 智慧財產及商業法院 24,158,
  其他專業法庭・委員會 33,459. Case-type rows: 民事 14,593,554, 刑事 7,534,335,
  行政 593,475, 其他 25,689.
- **Administrative rules and interpretations: 107,767 to 107,771; issuing agencies unchanged at 107.**
  Rows that moved: 內政部 6,745, 經濟部 6,684, 農業部 3,089, 核能安全委員會 229.
  Agencies with fewer than 20 entries unchanged: 58 agencies, 120 entries.
- **Appeal-chain relations: 4,375,506 to 4,378,841. Interpretation validity ledger: 80,470 to 84,831.**
  Acts, regulations, repealed instruments, constitutional decisions and labour arbitration decisions unchanged.

## Data coverage update (2026-10-21)

Documentation-only change; no package release (CLI still v2.3.1).

- **Court judgments: 22,724,893 to 22,729,045** (+4,152). Court-level rows: 地方法院 17,125,227,
  地方法院簡易庭 3,334,066, 高等法院及分院 1,359,214, 最高法院 406,117,
  高等行政法院 203,198, 最高行政法院 124,354, 地方行政訴訟庭 93,970,
  高雄少年及家事法院 25,313, 智慧財產及商業法院 24,132,
  其他專業法庭・委員會 33,454. Case-type rows: 民事 14,582,169, 刑事 7,528,313,
  行政 592,875, 其他 25,688.
- **Administrative rules and interpretations: 103,091 to 107,767; issuing agencies 93 to 107.**
  Two interpretation collections were added: the Ministry of the Interior land-administration
  interpretation compilation (內政部 2,667 to 6,744; letters issued by other agencies and
  reproduced in that compilation are counted under their own issuing agency), and the Executive Yuan
  consumer-protection interpretations (行政院消費者保護處, new agency row, 269).
  Other rows that moved: 財政部 10,704, 法務部 7,105, 經濟部 6,683, 行政院環境保護署 4,467, 銓敘部 4,009,
  文化部 1,519, 環境部 1,121, 司法行政部 444, 行政院 227 (new row), 外交部 135, 司法院 56.
  Agencies with fewer than 20 entries: 46 agencies (104) to 58 agencies (120).
- **Appeal-chain relations: 4,371,339 to 4,375,506.** Interpretation validity ledger unchanged at
  80,470; acts, regulations, repealed instruments and labour arbitration decisions unchanged.

## Data coverage update (2026-10-20)

Documentation-only change; no package release (CLI still v2.3.1).

- **Court judgments: 22,674,799 to 22,724,893.** Court-level rows: 地方法院 17,122,239,
  地方法院簡易庭 3,333,452, 高等法院及分院 1,358,962, 最高法院 406,042, 高等行政法院 203,176,
  最高行政法院 124,350, 地方行政訴訟庭 93,870, 高雄少年及家事法院 25,279, 智慧財產及商業法院
  24,131, 其他專業法庭・委員會 33,392. Case-type rows: 民事 14,579,795, 刑事 7,526,721,
  行政 592,749, 其他 25,628. 21,029 judgments ingested from the August 2026 monthly bundle
  had been indexed without a court code; the code was backfilled on 2026-10-20 and the
  monthly-bundle importer now writes it, so every row above carries a court code.
- **Administrative rules and interpretations: 103,029 to 103,091** (still 93 agencies).
  財政部 10,661, 金管會 8,392, 勞動部 7,179, 法務部 7,096, 銓敘部 4,008, 考試院 3,382,
  農業部 3,088, 教育部 2,912, 文化部 1,517, 環境部 1,119, 公務人員保障暨培訓委員會 690,
  國科會 574, 海洋委員會 224, 法務部矯正署 170, 故宮博物院 59.
- **Regulations: 7,254 to 7,253 (128,738 articles); repealed instruments 3,525 to 3,526.**
  Acts unchanged at 1,022 (44,503 articles).
- **Interpretation validity ledger: 80,339 to 80,470. Appeal-chain relations: 4,366,833 to
  4,371,339.** Labour arbitration decisions unchanged at 465.

## v2.3.1 (2026-10-14)

- **Fix: CLI no longer crashes on NO_PROXY entries httpx cannot parse.** IPv6 CIDR or
  bracketed entries such as `::1/128`, `[::1]` or `fe80::/10` in `NO_PROXY`/`no_proxy`
  made every command fail with `httpx.InvalidURL`, so users had to run
  `env -u no_proxy -u NO_PROXY twlegalrag ...`. Unparseable entries are now skipped with a
  one-line warning on stderr; proxy settings otherwise apply as before.

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
