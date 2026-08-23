"""Config loading tests (first-party, v2.0.0).

Covers the contract of twlegalrag.config:
- values come from ~/.twlegalrag/config.toml (redirected via TWLEGALRAG_HOME)
- env vars always win over the file
- a broken or absent file degrades to defaults, never raises
"""

import importlib
import os

import pytest

import twlegalrag.config as config


@pytest.fixture()
def isolated_home(tmp_path, monkeypatch):
    """Point the config dir at a temp dir and reload the module so the
    CONFIG_DIR/CONFIG_FILE constants pick it up."""
    monkeypatch.setenv("TWLEGALRAG_HOME", str(tmp_path))
    monkeypatch.delenv("TWLEGALRAG_TLR_BASE_URL", raising=False)
    monkeypatch.delenv("TWLEGALRAG_TLR_API_KEY", raising=False)
    importlib.reload(config)
    yield tmp_path
    monkeypatch.delenv("TWLEGALRAG_HOME", raising=False)
    importlib.reload(config)


def test_defaults_without_config_file(isolated_home):
    assert config.get_tlr_base_url() == "https://tlr.dr-legal.com.tw"


def test_reads_base_url_from_toml(isolated_home):
    (isolated_home / "config.toml").write_text(
        '[tlr]\nbase_url = "https://example.invalid"\n', encoding="utf-8"
    )
    assert config.get_tlr_base_url() == "https://example.invalid"


def test_env_var_beats_file(isolated_home, monkeypatch):
    (isolated_home / "config.toml").write_text(
        '[tlr]\nbase_url = "https://from-file.invalid"\n', encoding="utf-8"
    )
    monkeypatch.setenv("TWLEGALRAG_TLR_BASE_URL", "https://from-env.invalid")
    assert config.get_tlr_base_url() == "https://from-env.invalid"


def test_malformed_toml_degrades_to_default(isolated_home):
    (isolated_home / "config.toml").write_text("this is [not toml", encoding="utf-8")
    assert config.get_tlr_base_url() == "https://tlr.dr-legal.com.tw"


def test_toml_parser_is_available():
    """requires-python allows 3.9; pyproject declares the tomli backport for
    interpreters without stdlib tomllib, so a parser must always be importable
    in a correctly installed environment."""
    assert config.tomllib is not None
