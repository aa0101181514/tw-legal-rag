"""Offline tests for CLI-level diagnostics (no network, no LLM).

Covers three regressions:

1. ``python -m twlegalrag`` must work — ``search_judgments.py`` falls back to it
   when the console script is not on PATH.
2. A bad ``--type`` value must produce a message, not a traceback.
3. Missing / truncated reasoning text must be reported to the user, not left
   sitting silently in a JSON field.
"""

import subprocess
import sys

from typer.testing import CliRunner

from twlegalrag import cli
from twlegalrag.retrieval import Judgment

runner = CliRunner()


def _j(citation="某案", fulltext="理由...", complete=True, total=None):
    return Judgment(
        rank=1, doc_id="XXDM,100,X,1,20110101", citation_text=citation,
        court_name="某法院", jdate="2011-01-01", snippet="", citation_url="",
        citation_markdown="", result_token="tok",
        fulltext=fulltext, fulltext_complete=complete, fulltext_total_chars=total,
    )


# -- 1. module entry point ---------------------------------------------------

def test_python_dash_m_entry_point_runs():
    """`python -m twlegalrag --version` must not raise "No module named ...__main__"."""
    proc = subprocess.run(
        [sys.executable, "-m", "twlegalrag", "--version"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "twlegalrag" in proc.stdout


# -- 2. bad option value -----------------------------------------------------

def test_bad_search_type_is_a_message_not_a_traceback():
    result = runner.invoke(cli.app, ["search", "測試", "--type", "bogus"])
    assert result.exit_code == 1
    assert result.exception is None or isinstance(result.exception, SystemExit)


# -- 3. incomplete full text is surfaced -------------------------------------

def test_warn_missing_fulltext_names_the_judgment(capsys):
    cli._warn_missing_fulltext([_j("甲案", fulltext="")], read_n=1)
    out = capsys.readouterr().err
    assert "甲案" in out
    assert "未取得判決理由全文" in out


def test_warn_missing_fulltext_ignores_deliberately_unread_hits(capsys):
    hits = [_j("甲案", fulltext="有全文"), _j("乙案", fulltext="")]
    cli._warn_missing_fulltext(hits, read_n=1)  # --read-top 1
    assert "乙案" not in capsys.readouterr().err


def test_warn_truncated_bundle_reports_captured_vs_total(capsys):
    data = {
        "judgments": [
            {
                "citation_id": "J1",
                "citation_text": "甲案",
                "fulltext_excerpt": "x" * 300,
                "fulltext_truncated": True,
                "fulltext_total_chars": 1145,
            },
            {
                "citation_id": "J2",
                "citation_text": "乙案",
                "fulltext_excerpt": "y" * 50,
                "fulltext_truncated": False,
                "fulltext_total_chars": 50,
            },
        ]
    }
    cli._warn_truncated_bundle(data)
    out = capsys.readouterr().err
    assert "J1" in out and "300" in out and "1145" in out
    assert "J2" not in out  # complete judgments must stay quiet
