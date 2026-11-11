#!/usr/bin/env python3
"""Run `twlegalrag pack` for a question and print the bundle JSON to stdout.

Thin wrapper used by the tw-legal-rag Claude Code skill. It only locates the
CLI and forwards arguments — all retrieval logic lives in the twlegalrag
package. Works on macOS / Linux / Windows, including user-site installs where
the console script is not on PATH.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys


def _cli_command() -> list[str]:
    """Return the command vector for the twlegalrag CLI.

    Preference order:
    1. `twlegalrag` console script on PATH (shutil.which also finds .exe on
       Windows).
    2. `<current python> -m twlegalrag` — covers pip --user installs whose
       Scripts/bin dir is not on PATH.
    """
    exe = shutil.which("twlegalrag")
    if exe:
        return [exe]
    return [sys.executable, "-m", "twlegalrag"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Retrieve Taiwan judgments as a citation bundle (JSON on stdout)."
    )
    parser.add_argument("question", help="legal question in plain language")
    parser.add_argument(
        "-n", type=int, default=5, help="number of judgments to retrieve (1-10)"
    )
    parser.add_argument("--from", dest="date_from", help="earliest judgment date, YYYY-MM-DD")
    parser.add_argument("--to", dest="date_to", help="latest judgment date, YYYY-MM-DD")
    parser.add_argument("--court", help="full court name, e.g. 最高法院")
    parser.add_argument("--newest", action="store_true", help="most recent judgment date first")
    args = parser.parse_args()

    cmd = _cli_command() + ["pack", args.question, "-n", str(args.n)]
    if args.date_from:
        cmd += ["--from", args.date_from]
    if args.date_to:
        cmd += ["--to", args.date_to]
    if args.court:
        cmd += ["--court", args.court]
    if args.newest:
        cmd += ["--newest"]
    try:
        # The CLI prints the bundle JSON to stdout and progress to stderr;
        # inherit both so the caller sees exactly what the CLI produced.
        proc = subprocess.run(cmd)
    except FileNotFoundError:
        print(
            "twlegalrag CLI not found. Install it with: pip install twlegalrag",
            file=sys.stderr,
        )
        return 127
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
