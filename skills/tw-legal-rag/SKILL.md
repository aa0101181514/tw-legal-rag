---
name: tw-legal-rag
description: Retrieve real Taiwan court judgments with verifiable citations before answering any question about Taiwan law or case law. Use when the user asks about 台灣/臺灣 judgments, 判決, 法院見解, legal precedents, or wants case support for a legal argument. Wraps the twlegalrag CLI (pack subcommand); answers must cite only citation_ids present in the returned bundle.
---

# TW Legal RAG — Taiwan judgment retrieval for Claude Code

## When to use

Any time the question involves Taiwan law and the answer would benefit from
actual court judgments: legal questions in plain language, case-law research,
checking whether a cited 字號 exists, or building an argument that needs
precedent support. Retrieve FIRST, answer second.

## How to retrieve

Run the bundled script with the user's question:

```bash
python3 scripts/search_judgments.py "雇主未足額提撥勞工退休準備金的法律責任" -n 5
```

It prints a bundle JSON containing judgments (court, case number, date,
reasoning excerpts), stable citation ids (J1, J2, ...), an
`allowed_citations` whitelist and verification instructions.

The script locates the `twlegalrag` executable automatically and falls back
to `python -m twlegalrag` when the console script is not on PATH (common on
Windows user-site installs). If both fail, install the CLI first:
`pip install twlegalrag`.

## Citation rules (non-negotiable)

1. Cite ONLY ids listed in the bundle's `allowed_citations`. Judgments in
   `unread_candidates` were not read in full — never present them as
   authority.
2. Quote only text that appears verbatim in a judgment's
   `fulltext_excerpt`. Do not reconstruct holdings from memory.
3. If the bundle is empty or retrieval fails, say so explicitly. Never
   substitute invented case numbers.
4. A case number appearing in the bundle proves the judgment exists — it
   does not prove it supports the user's position. Read the excerpt before
   characterising a holding.
5. Follow the bundle's own `verification_instructions` field; it is part of
   the data contract.

## Notes

- Retrieval hits the public TLR endpoint (`tlr.dr-lawbot.com`); no API key
  is required and no LLM is called server-side.
- Windows: if output shows garbled Chinese, the terminal is not in UTF-8;
  the CLI reconfigures its own streams, but pipe output to a file when in
  doubt.
