#!/usr/bin/env python3
"""Retrieve Taiwan court judgments via the twlegalrag CLI and print a clean,
UTF-8-safe summary plus write the raw bundle JSON.

Why this wrapper exists: the `twlegalrag` CLI renders results with `rich`,
which crashes on the Windows console (cp950/cp1252 cannot encode CJK box
chars). We bypass that by always driving the JSON-producing `pack` subcommand
and reading the file back ourselves with an explicit UTF-8 decode. It also
locates the executable so callers do not depend on it being on PATH.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile


def find_cli() -> str:
    """Locate the twlegalrag executable: PATH first, then the Python Scripts dir."""
    found = shutil.which("twlegalrag")
    if found:
        return found
    exe = "twlegalrag.exe" if os.name == "nt" else "twlegalrag"
    candidate = os.path.join(sysconfig.get_path("scripts"), exe)
    if os.path.exists(candidate):
        return candidate
    sys.exit(
        "twlegalrag not found. Install it with: python -m pip install twlegalrag"
    )


def run_pack(cli: str, question: str, n: int, out_path: str, read_top: int | None) -> None:
    cmd = [cli, "pack", question, "-n", str(n), "-o", out_path]
    if read_top is not None:
        cmd += ["--read-top", str(read_top)]
    # Force UTF-8 / dumb terminal so the CLI's own rich output does not crash.
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "COLUMNS": "120", "TERM": "dumb"}
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout + "\n" + proc.stderr + "\n")
        sys.exit(f"pack failed (exit {proc.returncode})")


def summarize(bundle_path: str, excerpt_chars: int) -> None:
    with open(bundle_path, encoding="utf-8") as f:
        data = json.load(f)
    judgments = data.get("judgments", [])
    out = sys.stdout
    # Guarantee UTF-8 output regardless of the host console code page.
    try:
        out.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass
    print(f"Query: {data.get('query', '')}")
    print(f"Retrieved {len(judgments)} judgments. Bundle: {bundle_path}\n")
    for j in judgments:
        print(f"[{j.get('citation_id')}] {j.get('citation_text', '')}")
        print(f"    court: {j.get('court_name', '')}  date: {j.get('jdate', '')}  "
              f"category: {j.get('case_category', '')}")
        arts = j.get("cited_articles") or []
        if arts:
            print(f"    cited_articles: {', '.join(map(str, arts))}")
        url = j.get("citation_url")
        if url:
            print(f"    url: {url}")
        excerpt = (j.get("fulltext_excerpt") or "").strip()
        if excerpt and excerpt_chars != 0:
            shown = excerpt if excerpt_chars < 0 else excerpt[:excerpt_chars]
            print(f"    excerpt: {shown}")
        print()
    print("AI USE NOTICE: cite only the citation_id values above; mark any "
          "proposition not supported by these judgments as unverified.")


def main() -> None:
    p = argparse.ArgumentParser(description="Search Taiwan judgments via twlegalrag.")
    p.add_argument("question", help="Legal question in plain language (Chinese OK).")
    p.add_argument("-n", type=int, default=5, help="Number of judgments (1-10).")
    p.add_argument("-o", "--out", help="Bundle JSON output path (default: temp file).")
    p.add_argument("--read-top", type=int, default=None,
                   help="Fetch full text for only the top N results.")
    p.add_argument("--excerpt-chars", type=int, default=600,
                   help="Excerpt chars to print per judgment (0=none, -1=full).")
    args = p.parse_args()

    out_path = args.out or os.path.join(tempfile.gettempdir(), "twlegalrag_bundle.json")
    cli = find_cli()
    run_pack(cli, args.question, args.n, out_path, args.read_top)
    summarize(out_path, args.excerpt_chars)


if __name__ == "__main__":
    main()
