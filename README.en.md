# Taiwan Legal RAG: Taiwan Legal MCP Server & CLI (`twlegalrag`)

Author: Aaron Huang (黃思齊), attorney-at-law, founder of [Dr.Legal / 法律偵探](https://dr-legal.com.tw) ([profile](https://dr-legal.com.tw/aaron)).

<div align="center">

### 🌐 Language / 語言 / 言語

[**繁體中文**](README.md) ・ **English** ・ [**日本語**](README.ja.md)

</div>

---

> **Free, no signup, no API key.** A Taiwan legal **MCP server**: add one URL
> (`https://tlr.dr-legal.com.tw/mcp`) to Claude, ChatGPT, Codex or Cursor and your AI
> assistant can semantically search 22M+ Taiwan court judgments, administrative
> interpretations and Constitutional Court decisions, each with a citation check.
> A source-available CLI (`twlegalrag`) talks to the same backend.

Taiwan Legal RAG CLI retrieves Taiwan court judgments from Legal Detective's
public TLR endpoint and packages them for use with **your own AI tools**. It
does **not** generate legal advice, does **not** call any LLM, and does **not**
guarantee semantic faithfulness of third-party model outputs. Its built-in
citation check only verifies whether cited judgments belong to the retrieved
bundle.

## Data coverage (as of 2026-09-01, counted directly from the production database)

| Corpus | Size | Access |
|---|---:|---|
| **Court judgments** (all Taiwan court levels) | **22,558,169** | semantic + lexical search + exact docket lookup; daily incremental sync from Judicial Yuan open data, including post-publication corrections and takedowns |
| Appeal-chain relations | 4,537,220 | attached as `case_history` per judgment, with 主文 "廢棄/駁回" flags |
| Administrative rules / interpretations (行政規則・函釋) | 84,737 | exact serial lookup + semantic search (hosted MCP); 78 issuing agencies, per-agency detail below |
| Judicial Yuan Grand Justices interpretations (大法官解釋) | 813 | same as above |
| Constitutional Court judgments (憲判字) | 57 | same as above |
| Tax interpretations (財政部) | 9,093 | same as above |
| Interpretation validity ledger | 50,853 | repealed / ceased / superseded status, checked before citing |
| Labour arbitration decisions (勞動部裁決委員會) | 400 | surfaced alongside labour queries, explicitly labelled as non-court decisions |
| Constitution (憲法) | 1 | 197 articles incl. 12 additional articles. Searchable on [dr-legal.com.tw](https://dr-legal.com.tw) |
| Acts (法律) | 1,083 / 45,620 articles | Named 法/律/條例/通則 per Central Regulation Standard Act §2. Same as above |
| Regulations (命令) | 7,474 / 132,760 articles | Named 規程/規則/細則/辦法/綱要/標準/準則 per §3. Same as above |
| Repealed instruments | 3,230 | 254 acts, 2,974 regulations, plus constitutional-tier norms such as the Temporary Provisions; flagged as repealed for historical research |

Judgments sync daily (Judicial Yuan open data lags publication by a few days;
for very recent decisions consult the official site). Numbers above are taken
directly from the production database on the stated date, not estimates.

### Judgment detail (by court level / case category)

| 法院層級 | 筆數 |
|---|---:|
| 地方法院 | 16,686,132 |
| 地方法院簡易庭 | 3,268,493 |
| 高等法院及分院 | 1,328,658 |
| 最高法院 | 399,288 |
| 高等行政法院 | 200,600 |
| 最高行政法院 | 122,964 |
| 地方行政訴訟庭 | 78,891 |
| 智慧財產及商業法院 | 23,678 |
| 高雄少年及家事法院 | 22,113 |
| 其他專業法庭・委員會 | 32,250 |
| 未帶法院代碼欄位（計入總數，不列層級） | 395,102 |
| **合計** | **22,558,169** |

| 案件類別 | 筆數 |
|---|---:|
| 民事 | 14,232,700 |
| 刑事 | 7,332,300 |
| 行政 | 573,417 |
| 其他 | 24,650 |

### Administrative rules by issuing agency (75,644 by serial number)

Agency names are kept in their official Chinese form as recorded on each
interpretation, including historical names of reorganized agencies.

| Agency | Count |
|---|---:|
| 財政部 | 10,623 |
| 內政部國土管理署 | 8,769 |
| 經濟部智慧財產局 | 7,161 |
| 勞動部 | 7,147 |
| 法務部 | 7,068 |
| 行政院環境保護署 | 4,463 |
| 行政院公共工程委員會 | 4,104 |
| 銓敘部 | 3,990 |
| 經濟部 | 3,131 |
| 農業部 | 3,078 |
| 金管會 | 2,824 |
| 內政部 | 2,654 |
| 前司法行政部 | 1,432 |
| 法務部行政執行署 | 1,410 |
| 內政部戶政司 | 1,391 |
| 公務人員保障暨培訓委員會 | 687 |
| 主計總處 | 669 |
| 國科會 | 568 |
| 文化部文化資產局 | 561 |
| 農業部水保署 | 543 |
| 司法行政部 | 433 |
| 考選部 | 429 |
| 人事行政總處 | 323 |
| 核能安全委員會 | 228 |
| 原住民族委員會 | 225 |
| 海洋委員會 | 223 |
| 公平交易委員會 | 204 |
| 文化部 | 203 |
| 法務部矯正署 | 168 |
| 中央選舉委員會 | 112 |
| 農業部林業及自然保育署 | 103 |
| 客家委員會 | 97 |
| 國家發展委員會 | 86 |
| 考試院 | 86 |
| 個人資料保護委員會籌備處 | 73 |
| 故宮博物院 | 58 |
| 環境部 | 46 |
| 臺灣高等法院檢察署 | 41 |
| 法務部政風司 | 37 |
| 法務部廉政署 | 32 |
| 司法院 | 28 |
| 經濟部能源署 | 28 |
| 法務部調查局 | 20 |
| 其他 35 個機關（各未滿 20 筆） | 88 |
| **合計** | **75,644** |


## Why it is different

This is not a generic keyword judgment search tool. It connects to the TLR
retrieval service that Legal Detective has been building for a long time:

- **22,558,169** Taiwan court decisions (as of 2026-09-01), structurally
  processed and vectorized.
- **Semantic fuzzy search** — natural-language queries find judgments that are
  "conceptually similar but worded differently"; lexical exact-match modes are
  available for technical vocabulary.
- **Exact docket lookup** — a complete docket number switches to exact lookup
  automatically; a miss is reported honestly ("not found does not mean the
  judgment does not exist"), never padded with similar cases.
- **Appeal chain `case_history`** — each judgment carries its recorded
  upper/lower instances with 主文 "廢棄/駁回" flags, so you can see **before
  citing** whether a judgment has been overturned.
- **Paired interpretation tools** — exact serial lookup (with validity status)
  and semantic search over administrative interpretations; interpretations and
  judgments are strictly separated. See
  [`docs/mcp-anchor.md`](docs/mcp-anchor.md).
- **Exact statute lookup** — retrieve the current text of a Taiwan statute
  article by law name plus article number, with the law's last-amendment date
  and any abolition note, so an article citation can be verified before it
  goes into legal writing instead of being recalled from model memory. Common
  abbreviations resolve to official law names. Current consolidated version
  only; for pre-amendment text consult the official amendment history.
- **Citation safeguards are first-class** — `allowed_citations` read-whitelist,
  `unread_candidates` markers, per-bundle verification instructions, plus the
  CLI-side citation check — all aimed at legal AI's worst hallucination mode:
  **real docket number, fabricated holding**.
- This CLI ships **no judgment database** and exposes no model weights, vector
  indexes, or retrieval-pipeline internals; it is a client for the public TLR
  retrieval endpoint.

### Compared with "official-website wrapper" tools

Another common approach is to proxy the Judicial Yuan / law database websites'
built-in search in real time. The two serve different purposes and can
complement each other:

| | Official-site wrapper | Taiwan Legal RAG |
|---|---|---|
| Search | official site keyword search | semantic retrieval over a self-built 22M-judgment corpus; finds conceptually similar cases even with different wording |
| Citation protection | usually none | read-whitelist + verification instructions + citation check |
| Docket lookup | as provided by the site | exact lookup; on a miss it explicitly says not to speculate |
| Appeal chain | trace case by case yourself | `case_history` attached, with vacated flags |
| Availability | subject to site WAF / redesigns; often needs a local browser to pass challenges | hosted endpoint, zero local setup |
| Freshness | official site is real-time | for very recently published decisions, check the official site |

The wrapper's strength is real-time official-source access; this tool's
strength is semantic retrieval quality and citation discipline.

> Unlike keyword-only legal search tools, Taiwan Legal RAG CLI connects to a
> production semantic retrieval backend built on 22M+ Taiwan court judgments,
> enabling fuzzy concept-level search while keeping model weights, infrastructure,
> and private indexes server-side.

(Wording note: what is published here is the **CLI**, not the model or the vector
store; the backend retrieval service, model weights, and private indexes stay
server-side and are not published with this tool.)

## What it does / does not do

**Does**: retrieve judgments with natural language → get a structured listing,
judgment reasoning excerpts, and citation links → package them into a bundle
for your own AI; and run a bundle-level citation check on any AI-generated
answer.

**Does not**: this tool **calls no LLM, generates no legal opinion, and
endorses no** model output. Answers are produced by the AI you choose
(ChatGPT / Claude / Gemini / a local model).

### What the built-in citation check can verify

`check` is a **bundle-level, best-effort** string check. It only verifies:

- whether the case numbers cited in the answer **are inside the bundle**
  (catching "cited a number not in the bundle" = suspected fabrication);
- citations of judgments outside the bundle, or nonexistent ones;
- **quote existence (bundle level)**: whether a verbatim sentence the answer
  attributes to "the court said…" appears **anywhere** in the bundle text.

### What it **cannot** verify (important)

- whether a quote comes from **the specific judgment** the answer attributes it
  to (existence check only looks at "does this sentence appear anywhere in the
  bundle", not bound to a particular judgment);
- whether the court's holding was **read correctly**;
- whether a **party's argument** (plaintiff/defendant/appellant) was mistaken
  for the **court's holding**;
- whether **obiter dicta** was treated as the judgment's **core authority**;
- paraphrase-style holding hallucinations.

All of these require reading the full judgment text — which is why bundles
include judgment excerpts and verification instructions that require the
downstream model to verify on its own. **`pass` only means "the cited numbers
match the bundle's identity list"; it does not mean "the legal reasoning is
correct" or "the quote really comes from that judgment."** Also, `check` only
compares against **bundle content**, not the entire Legal Detective database —
if you later open full judgment texts yourself and rewrite the answer, `check`
still only sees the excerpts originally packed.

## Install

```bash
pip install twlegalrag
```

Depends only on `httpx` / `typer` / `rich`. No LLM packages or keys needed —
this tool does not call LLMs.

## Usage

```bash
# 1) Pure retrieval — list matching judgments
twlegalrag search "勞資 加班費" -n 5 --read

# 2) Pack — produce a bundle you can hand to any AI  ★ main flow
twlegalrag pack "車禍對方全責,我可以求償什麼?" -o bundle.json
#   → paste bundle.json to ChatGPT / Claude / Gemini and require it to cite
#     only judgments inside the bundle

# 3) Citation check — bundle-level check on any AI-generated answer
twlegalrag check bundle.json answer.txt

# Service health
twlegalrag health
```

A `pack` bundle contains `query`, each judgment's `citation_id` (J1, J2, ...),
`citation_text`, `citation_url`, `doc_id`, the Layer-1 listing,
`fulltext_excerpt` (an excerpt of the judgment's reasoning, length-capped),
`case_history` (database-recorded appeal chain, v1.1), `allowed_citations`,
and a `verification_instructions` block that explicitly requires the
downstream model to cite only in-bundle judgments and to mark unsupported
propositions as unverified. An AI USE NOTICE is also printed to stderr.

Since v1.1, `verification_instructions` additionally includes an
**OPINION-LAYER SELF-CHECK**: after answering, the downstream model must go
back and verify that (a) every holding attributed to a judgment actually
appears in that judgment's excerpt (not another judgment's, not inferred);
(b) outcome directions (win/lose/vacated/dismissed/remanded) are not reversed;
(c) judgments shown as vacated in `case_history` are not cited as currently
valid holdings. This complements `check`'s bundle-level number check — a real
case number does not make the attributed holding real, and opinion-layer
verification can only be done by **the model that read the text**; these rules
write that obligation into every bundle.

`allowed_citations` is the whitelist of citable judgments and **only contains
judgments whose reasoning text was actually read in**. The CLI's `pack` reads
every judgment it returns, so the two always match. For the hosted Remote MCP
`search_bundle` (`/v1/pack`), when `read_top < max_results`, only the top
`read_top` judgments are read in full; the rest remain listed in `judgments`
for browsing but are moved to `unread_candidates` (not authority; must not be
cited as court reasoning). See [`docs/mcp-anchor.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/docs/mcp-anchor.md).

## Configuration (optional)

By default the CLI talks to the public endpoint `https://tlr.dr-legal.com.tw`,
no key required. If the service operator issues you an API key, put it in an
environment variable or `~/.twlegalrag/config.toml` (git-ignored — **never**
commit it):

```bash
export TWLEGALRAG_TLR_BASE_URL=https://tlr.dr-legal.com.tw   # default
export TWLEGALRAG_TLR_API_KEY=...   # optional; NOT needed for the public endpoint (enterprise keys only)
```

```toml
[tlr]
# base_url = "https://tlr.dr-legal.com.tw"
# api_key  = "..."
```

## Privacy and data flow

First, what **never** passes through the TLR server:

- Your **full conversation with your AI** (Claude / ChatGPT / local model),
  your uploaded documents, and the AI-generated answers all happen between you
  and your AI provider and **never** pass through TLR. TLR is a retrieval-only
  server; the only things it receives are the **retrieval query strings** your
  AI client decides to send and the subsequent judgment-document requests.
- **No account registration**: the public REST endpoint works without a key,
  the service has no user account system, and queries are not tied to any
  account identity.
- The judgment data itself consists of Taiwan's **publicly available** court
  decisions; responses contain no non-public personal data.

What does travel over the network, and you should understand:

- Your **search terms / questions** are sent to the TLR retrieval endpoint
  (`https://tlr.dr-legal.com.tw`) to fetch judgments.
- **TLR may log your query text, timestamp, IP-derived metadata, and result
  counts for retrieval-quality analysis. Do not submit personal secrets or
  confidential facts. Queries are not used to train generative models.**
- This tool **calls no LLM and uses no server-side tokens**; if you feed a
  bundle to some AI yourself, that transmission and its cost happen **between
  you and your chosen AI provider** and have nothing to do with this tool.
- If you have an endpoint API key, keep it in environment variables; do not
  commit config files.

## How the citation check works

`twlegalrag/faithful/` is a set of **zero-dependency pure functions** (standard
library `re` + `unicodedata` only). Given the answer text and the bundle's
judgment excerpts, it returns `pass` / `needs_review` / `fail`. It is
deliberately conservative: when unsure it returns `needs_review` rather than
`fail` to keep false alarms low. It **calls no LLM and touches no database**;
it is deterministic string analysis.

⚠️ This directory is a **snapshot** of internal code; some functions in it
(e.g. `check_party_as_court` / `run_all_checks`) are **not used** by the CLI.
Their presence does **not** mean the CLI can do opinion-layer / semantic
verification — the CLI uses only two bundle-level checks. Do not read the file
list as a feature list. See `twlegalrag/faithful/VENDORED.md`.

## 2026-08-20 hosted-service update (MCP / REST)

- Bundle responses carry a `result_token`, so any judgment in the bundle can be
  read in full directly.
- Every result carries `hit_excerpt` (a preview of the matched passage); quote
  from the full reasoning text, not from this field.
- `get_judgment_fulltext` supports `excerpt_offset` paging — long judgments can
  be read to the end.
- Lexical search modes (`search_type: keyword` / `phrase`) improved for precise
  technical vocabulary; conceptual questions should still use the default
  `hybrid`.

Live now on REST and Remote MCP. CLI **v2.1.0** follows suit: `pack` pages
through long judgments to the end (per-judgment bundle budget doubled) and
carries `hit_excerpt` into bundles.

## Other ways to connect (same TLR backend)

This CLI is one way to use the TLR retrieval service. The same backend
`tlr.dr-legal.com.tw` also supports plugging judgment search directly into your
AI tools via **Remote MCP**. Both use the same MCP endpoint
`https://tlr.dr-legal.com.tw/mcp`; OAuth completes automatically on connection
(dynamic registration, no API key application or setup needed):

- **Claude (Remote MCP)**: Settings → Connectors → Add custom connector, URL
  `https://tlr.dr-legal.com.tw/mcp`.
- **ChatGPT (MCP connector)**: add a custom MCP server in Connectors, URL
  `https://tlr.dr-legal.com.tw/mcp`.
- **Claude Code (skill, wraps this CLI rather than MCP)**: a ready-made skill
  lives in [`skills/tw-legal-rag/`](https://github.com/aa0101181514/tw-legal-rag/blob/main/skills/tw-legal-rag/).
  Copy that folder into your project's `.claude/skills/` and Claude will run
  this CLI's `pack` subcommand whenever a question involves Taiwan case law,
  citing only `citation_id`s that exist in the returned bundle. Setup notes
  and Windows caveats are in the skill's `SKILL.md`.
The Remote MCP surface currently has six tools:

| Tool | What it does | Added | In this CLI |
|------|--------------|:-----:|:-----------:|
| `search_bundle` | Search plus reasoning-text reads in one call, returning a bundle with a citation whitelist (recommended entry point) | 2026-06 | ✅ |
| `search_judgments` | Judgment search (structured listing; a full docket number switches to exact lookup) | 2026-05 | ✅ |
| `get_judgment_fulltext` | Full reasoning text of a judgment (with the `case_history` appeal chain) | 2026-05 | ✅ |
| `get_legal_reference` | Exact administrative-interpretation lookup by serial, with validity status | 2026-08 | not yet |
| `search_legal_references` | Semantic search over administrative interpretations | 2026-08 | not yet |
| `get_law_article` | Exact current-statute lookup and article-number verification | 2026-09 | not yet |

Per-tool input/output contracts are in
[`docs/mcp-anchor.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/docs/mcp-anchor.md).

This server is listed in the official [MCP Server Registry](https://registry.modelcontextprotocol.io/)
as `io.github.aa0101181514/tw-legal-rag`.

Whether you go through the CLI, MCP, or the Claude Code skill, answers are
generated by **your own AI**; this service only provides judgment content and
verifiable citation links.

## Architecture

```
your question
   │
[retrieve]  TLR /v1/search   ──►  Layer-1 listings + result_token
   │        TLR /v1/fulltext ──►  reasoning excerpt per judgment (capped)
   │
[pack]      pack ──► bundle.json (citation_id / allowed_citations / verification rules)
   │                 └─► hand to your own AI tool
   │
[check]     check ──► bundle-level citation check (in/out of bundle + in-bundle quote existence)
```

The judgment corpus, embeddings, and retrieval logic live server-side and are
**not in this repo**. This CLI is the published client and citation-check
tool.

## Disclaimer

This tool is an analysis aid, not legal advice, and not a lawyer. Always read
the full text of cited judgments yourself. Judgments obtained through the API
are Taiwan's publicly available court decisions; you are responsible for your
own use.

## License

**Elastic License 2.0 (ELv2)** from v2.0.0. Free to use, copy, modify and
redistribute — including commercial and internal-business use — with two
limits: you may not offer the software itself to third parties as a hosted
or managed service, and you may not remove license/notice protections.
Versions up to v1.2.2 remain MIT.

The hosted API and the judgment corpus were never covered by the code
license — see [`TERMS.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/TERMS.md). Project names and logos are not licensed —
see [`TRADEMARK.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/TRADEMARK.md). This project does not accept external pull
requests (single-author licensing policy) — see [`CONTRIBUTING.md`](https://github.com/aa0101181514/tw-legal-rag/blob/main/CONTRIBUTING.md).

---

<!-- MCP Server Registry ownership marker — verifies this PyPI package owns the
     io.github.aa0101181514/* namespace. Do not remove. -->
mcp-name: io.github.aa0101181514/tw-legal-rag
