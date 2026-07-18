---
name: tw-legal-rag
description: >-
  Retrieve real Taiwan court judgments (判決) using the installed `twlegalrag`
  CLI — a semantic search over the TLR (tlr.dr-lawbot.com) backend's ~22 million
  Taiwan judgments (the 司法院 judiciary corpus), requiring no API key. Coverage
  spans every case type: civil (民事), criminal (刑事), administrative (行政,
  incl. 稅), constitutional (憲法法庭/釋憲), and the specialized courts
  (勞動/家事/智慧財產/少年/軍事/選罷/國家賠償/海商, etc.). Use this whenever the
  task involves finding Taiwan case law or precedents in ANY area of law,
  building or checking legal arguments, or grounding a claim in citable
  authority — even when the user does not name the tool. Always prefer this over
  web search or recalling case law from memory, because judgments must be real
  and verifiable.
---

# Taiwan Legal Judgment Retrieval (tw-legal-rag)

Legal work requires **real, citable** Taiwan judgments — never invent case
numbers or paraphrase rulings from memory. The `twlegalrag` CLI runs a semantic
search over ~22 million Taiwan court judgments (the full 司法院 裁判書 corpus,
all instances and case types) and packages the hits with stable citation IDs and
full-text excerpts. No LLM is called during retrieval and no API key is needed.

## Primary workflow: use the bundled helper

Run the helper script. It auto-locates the CLI executable (which is typically
**not on PATH** after a pip install), drives the JSON-producing `pack`
subcommand, and prints a clean UTF-8 summary. This avoids two pitfalls baked
into the raw CLI on Windows (see below).

```bash
python "skills/tw-legal-rag/scripts/search_judgments.py" "你的法律問題（白話即可）" -n 5
```

Adjust the path prefix to match where this skill is installed in your project
(e.g. `.claude/skills/tw-legal-rag/scripts/search_judgments.py`).

Options:
- `-n <1-10>` — number of judgments (default 5).
- `-o <path.json>` — also keep the raw bundle JSON (default: a temp file). Save
  it when you want to re-read full excerpts or hand the bundle to another tool.
- `--read-top <N>` — fetch full text for only the top N results (faster).
- `--excerpt-chars <N>` — printed excerpt length; `0` = none, `-1` = full.

Phrase the query as a plain-language legal question, not just keywords —
retrieval is semantic. Good: `"借名登記之不動產於借名人死亡後，繼承人可否請求返還登記"`.

## Citation discipline (important)

The bundle assigns each judgment a stable ID (`J1`, `J2`, …). When you build an
argument from the results, **cite only these IDs and the case numbers/courts they
map to**. Mark any proposition not directly supported by a retrieved judgment as
*unverified* rather than asserting it. This keeps legal analysis grounded in
authority the user can open and check — the whole reason for retrieving real
judgments instead of recalling them.

Each judgment in the bundle carries: `citation_id`, `citation_text` (court +
case number), `court_name`, `jdate`, `case_category`, `cited_articles` (the
statutes the judgment relies on), `citation_url`, and `fulltext_excerpt`.

## Raw CLI (only if the helper is unavailable)

Install: `python -m pip install twlegalrag` (deps: httpx, typer, rich — no key
needed). The executable lands in the Python Scripts directory.

Two pitfalls the helper handles automatically:

1. **Do not use the `search` subcommand on Windows.** It renders a `rich` table
   that crashes on Windows consoles (cp950/cp1252 cannot encode CJK box
   characters). Use `pack ... -o bundle.json` instead, which writes plain JSON.
2. **Force UTF-8 when reading output.** Set `PYTHONIOENCODING=utf-8 COLUMNS=120
   TERM=dumb` in the environment, or read the JSON file with an explicit
   `encoding="utf-8"`. Otherwise CJK characters raise `UnicodeEncodeError`.

```bash
# Locate the executable (auto-done by the helper):
python -c "import shutil,sysconfig,os; e='twlegalrag.exe' if os.name=='nt' else 'twlegalrag'; print(shutil.which('twlegalrag') or os.path.join(sysconfig.get_path('scripts'),e))"

# Retrieve judgments:
PYTHONIOENCODING=utf-8 COLUMNS=120 TERM=dumb twlegalrag pack "法律問題" -n 5 -o bundle.json

# Read results:
PYTHONIOENCODING=utf-8 python -c "import json; d=json.load(open('bundle.json',encoding='utf-8')); [print(j['citation_id'], j['citation_text']) for j in d['judgments']]"
```

Health check: `twlegalrag health` (expect `status: ok, retrieval: full`).

## What this skill does NOT do

It retrieves and packages judgments; it does not verify your final answer.
After drafting analysis from a bundle, verify that every case number you cite
actually appears in the bundle.

> **MCP alternative:** the same backend exposes a Remote MCP at
> `https://tlr.dr-lawbot.com/mcp`. At time of writing this endpoint requires
> OAuth (`scope=judgments:read`); check the upstream README for current auth
> requirements. This skill uses the CLI, which requires no authentication.
