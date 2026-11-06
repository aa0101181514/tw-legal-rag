"""NO_PROXY entries httpx cannot parse must not crash client construction.

Reported 2026-10-14: a VM whose no_proxy carried an IPv6 entry made every CLI
command fail with httpx.InvalidURL until the user ran `env -u no_proxy`.
"""

import os

import pytest

from twlegalrag.retrieval import TLRClient, _no_proxy_entry_ok


@pytest.mark.parametrize("value", ["::1/128", "[::1]", "fe80::/10", "localhost,::1/128,10.0.0.0/8"])
def test_bad_ipv6_no_proxy_entries_do_not_crash(monkeypatch, capsys, value):
    monkeypatch.setenv("NO_PROXY", value)
    monkeypatch.setenv("no_proxy", value)
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example:3128")
    with TLRClient():
        pass
    assert "ignoring NO_PROXY entries" in capsys.readouterr().err
    assert os.environ["NO_PROXY"] == value  # environment left untouched


def test_valid_no_proxy_is_silent(monkeypatch, capsys):
    monkeypatch.setenv("NO_PROXY", "localhost,127.0.0.1,::1,.internal")
    monkeypatch.delenv("no_proxy", raising=False)
    with TLRClient():
        pass
    assert capsys.readouterr().err == ""


def test_bad_entry_is_actually_rejected_by_the_probe(monkeypatch):
    """`_no_proxy_entry_ok` must say False for an entry httpx cannot parse.

    Regression: on Windows `os.environ` is case-insensitive, so the probe's
    `{"NO_PROXY": entry, "no_proxy": None}` override removed the value it had
    just written. The probe then ran with no NO_PROXY at all, returned True for
    every entry, nothing was dropped, and the InvalidURL crash still happened.
    Passes on POSIX before and after the fix; only Windows showed the bug, so CI
    needs a windows-latest leg to catch a regression here.
    """
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example:3128")
    monkeypatch.setenv("NO_PROXY", "::1/128")
    monkeypatch.setenv("no_proxy", "::1/128")
    assert _no_proxy_entry_ok("::1/128") is False
    assert _no_proxy_entry_ok("localhost") is True
