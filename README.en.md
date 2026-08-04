[繁體中文](README.md) | **English** | [日本語](README.ja.md)

# Taiwan Legal RAG (`twlegalrag`)

> Open-source CLI for **semantic** Taiwan legal judgment retrieval, powered by
> Legal Detective's 22M-judgment retrieval infrastructure.

Taiwan Legal RAG CLI retrieves Taiwan court judgments from Legal Detective's
public TLR endpoint and packages them for use with **your own AI tools**. It
does **not** generate legal advice, does **not** call any LLM, and does **not**
guarantee semantic faithfulness of third-party model outputs. Its built-in
citation check only verifies whether cited judgments belong to the retrieved
bundle.

## Why it is different

This is not a generic keyword judgment search tool. It connects to the TLR
retrieval service that Legal Detective has been building for a long time:

- About **22 million** Taiwan court decisions, structurally processed and
  vectorized.
- Thousands of hours of retrieval pipeline optimization.
- **Semantic fuzzy search** — not limited to docket numbers, court names, or
  keywords; you can use natural language to find judgments that are
  "conceptually similar but worded differently."
- **Exact docket lookup** (v1.1) — when the query is a complete Taiwan docket
  number (e.g. 最高法院112年度台上字第9號), the tool automatically switches to
  exact lookup and returns that case's own documents (civil/criminal cases
  sharing the same number are listed side by side with labels). **When nothing
  is found it says so explicitly**: "not found does not mean the judgment does
  not exist; do not speculate about the case" — it never pads the result with
  semantically similar cases.
- **Appeal chain `case_history`** (v1.1) — when reading a judgment's full text,
  the database-recorded upper/lower instances are attached (including a flag
  for 主文含「廢棄」, i.e. the holding was vacated on appeal). **You can see
  whether a judgment has been vacated by a higher court before citing it.**
  Absence of an upper-court record only means the database has no record; it
  does not mean the judgment is final.
- **Exact administrative-interpretation lookup `get_legal_reference`**
  (2026-08, hosted MCP) — look up an administrative interpretation (函釋) by
  its issuing serial number (e.g. 台財稅第881945861號) and get its full text
  plus a **lifecycle status** (verified-active / unverified / repealed /
  no-longer-applied / superseded). Verify existence and validity before citing
  an interpretation; a miss explicitly states that **not found does not mean
  the interpretation does not exist**. Interpretations and judgments are
  strictly separated: never mixed in one ranking, and never to be cited as
  court reasoning. See [`docs/mcp-anchor.md`](docs/mcp-anchor.md).
- **Citation protection is a first-class citizen, not an afterthought** — each
  bundle carries an `allowed_citations` whitelist (only judgments whose
  reasoning text was actually read in), `unread_candidates` markers (judgments
  whose reasoning was not read must not be cited as authority), verification
  instructions written into every bundle (including opinion-layer self-check),
  plus a bundle-level citation check on the CLI side. The whole design targets
  the most painful hallucination pattern in legal AI: **real case number,
  fabricated holding**. Ordinary retrieval tools stop at handing data to the
  model; here, citation discipline is part of the data format itself.
- The open-source CLI **does not embed the judgment corpus** and does not
  expose backend model weights or vector indexes; it is a client for the
  public TLR retrieval endpoint.

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

(Wording note: what is open-sourced is the **CLI**, not the model or the vector
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
cited as court reasoning). See [`docs/mcp-anchor.md`](docs/mcp-anchor.md).

## Configuration (optional)

By default the CLI talks to the public endpoint `https://tlr.dr-lawbot.com`,
no key required. If the service operator issues you an API key, put it in an
environment variable or `~/.twlegalrag/config.toml` (git-ignored — **never**
commit it):

```bash
export TWLEGALRAG_TLR_BASE_URL=https://tlr.dr-lawbot.com   # default
export TWLEGALRAG_TLR_API_KEY=...                          # optional
```

```toml
[tlr]
# base_url = "https://tlr.dr-lawbot.com"
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
  (`https://tlr.dr-lawbot.com`) to fetch judgments.
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

## Other ways to connect (same TLR backend)

This CLI is one way to use the TLR retrieval service. The same backend
`tlr.dr-lawbot.com` also supports plugging judgment search directly into your
AI tools via **Remote MCP**. Both use the same MCP endpoint
`https://tlr.dr-lawbot.com/mcp`; OAuth completes automatically on connection
(dynamic registration, no API key application or setup needed):

- **Claude (Remote MCP)**: Settings → Connectors → Add custom connector, URL
  `https://tlr.dr-lawbot.com/mcp`.
- **ChatGPT (MCP connector)**: add a custom MCP server in Connectors, URL
  `https://tlr.dr-lawbot.com/mcp`.
- **Claude Code (Skill, via CLI not MCP)**: this repo ships a ready-made skill
  in [`skills/tw-legal-rag/`](skills/tw-legal-rag/) — drop the whole folder
  into your project's `.claude/skills/`. It wraps this CLI's `pack` subcommand
  so Claude automatically retrieves judgments when you ask about Taiwan
  case law and is required to cite only in-bundle `citation_id`s. The included
  `scripts/search_judgments.py` auto-locates the executable and handles two
  Windows pitfalls (see the skill's `SKILL.md`).

The Remote MCP surface currently has four tools: `search_bundle`,
`search_judgments`, `get_judgment_fulltext`, and `get_legal_reference` added
in 2026-08 (exact administrative-interpretation lookup, see
[`docs/mcp-anchor.md`](docs/mcp-anchor.md)); the last one is not wired into
this CLI yet.

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
**not in this repo**. This CLI is the open-source client and citation-check
tool.

## Disclaimer

This tool is an analysis aid, not legal advice, and not a lawyer. Always read
the full text of cited judgments yourself. Judgments obtained through the API
are Taiwan's publicly available court decisions; you are responsible for your
own use.

## License

MIT.
