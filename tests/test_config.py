"""Offline tests for config file loading."""

import builtins
import importlib
from types import SimpleNamespace


def test_config_file_loads_with_available_toml_parser(monkeypatch, tmp_path):
    monkeypatch.setenv("TWLEGALRAG_HOME", str(tmp_path))
    monkeypatch.delenv("TWLEGALRAG_TLR_BASE_URL", raising=False)
    monkeypatch.delenv("TWLEGALRAG_TLR_API_KEY", raising=False)

    (tmp_path / "config.toml").write_text(
        '[tlr]\nbase_url = "https://example.test"\napi_key = "secret"\n',
        encoding="utf-8",
    )

    import twlegalrag.config as config

    config = importlib.reload(config)

    assert config.get_tlr_base_url() == "https://example.test"
    assert config.get_tlr_api_key() == "secret"


def test_config_uses_tomli_when_tomllib_is_unavailable(monkeypatch, tmp_path):
    monkeypatch.setenv("TWLEGALRAG_HOME", str(tmp_path))
    monkeypatch.delenv("TWLEGALRAG_TLR_BASE_URL", raising=False)
    monkeypatch.delenv("TWLEGALRAG_TLR_API_KEY", raising=False)
    (tmp_path / "config.toml").write_text("[tlr]\n", encoding="utf-8")

    fake_tomli = SimpleNamespace(
        load=lambda _: {
            "tlr": {
                "base_url": "https://tomli.example",
                "api_key": "tomli-secret",
            },
        },
    )
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "tomllib":
            raise ModuleNotFoundError("No module named 'tomllib'")
        if name == "tomli":
            return fake_tomli
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    import twlegalrag.config as config

    config = importlib.reload(config)

    assert config.tomllib is fake_tomli
    assert config.get_tlr_base_url() == "https://tomli.example"
    assert config.get_tlr_api_key() == "tomli-secret"


def test_env_vars_override_config_file(monkeypatch, tmp_path):
    monkeypatch.setenv("TWLEGALRAG_HOME", str(tmp_path))
    monkeypatch.setenv("TWLEGALRAG_TLR_BASE_URL", "https://env.example")
    monkeypatch.setenv("TWLEGALRAG_TLR_API_KEY", "env-secret")
    (tmp_path / "config.toml").write_text(
        '[tlr]\nbase_url = "https://file.example"\napi_key = "file-secret"\n',
        encoding="utf-8",
    )

    import twlegalrag.config as config

    config = importlib.reload(config)

    assert config.get_tlr_base_url() == "https://env.example"
    assert config.get_tlr_api_key() == "env-secret"
