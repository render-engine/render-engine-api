import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from render_engine_api.config import ApiConfig


def _write_config(tmp_path, content):
    """Helper to write a pyproject.toml in tmp_path."""
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(content)
    return config_file


# Strategy for valid TOML-safe identifier strings (no quotes, newlines, etc.)
toml_safe_text = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
    min_size=1,
    max_size=50,
)

# Strategy that produces an optional config key (present or absent)
optional_toml_value = st.one_of(st.none(), toml_safe_text)


class TestAPIConfigLoadConfig:
    """Tests for APIConfig.load_config parsing pyproject.toml."""

    @given(
        module=optional_toml_value,
        site=optional_toml_value,
        collection=optional_toml_value,
    )
    @settings(max_examples=50, deadline=None)
    def test_loads_module_site_from_valid_config(self, module, site, collection):
        """Config correctly populates module, site, and collection from any combination of keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            lines = ["[tool.render-engine.cli]"]
            if module is not None:
                lines.append(f'module = "{module}"')
            if site is not None:
                lines.append(f'site = "{site}"')
            if collection is not None:
                lines.append(f'collection = "{collection}"')

            temp_config_file = _write_config(tmp_path, "\n".join(lines) + "\n")
            config = ApiConfig(config_file=temp_config_file)
            config.load_config()

            assert config._module == module
            assert config._site == site
            assert config._collection == collection

    def test_config_file_not_passed(self):
        """Returns None for all properties when no config_file is passed."""
        config = ApiConfig(config_file=None)  # intentional path that doesn't exist
        assert config.module is None
        assert config.site is None
        assert config.collection is None
        # Editor pulls from editor by default

    def test_config_file_not_found(self, tmp_path):
        """Returns None for all properties when the supplied config file does not exist."""
        config = ApiConfig(config_file=tmp_path / "no-pyproject.toml")  # intentional path that doesn't exist
        assert config.module is None
        assert config.site is None
        assert config.collection is None
        # Editor pulls from editor by default

    def test_invalid_toml_prints_error_and_returns_none(self, tmp_path):
        """Returns None for all properties when the config file contains invalid TOML."""
        config_file = _write_config(tmp_path, "not valid toml [[[")
        config = ApiConfig(config_file=config_file)
        assert config.module is None
        assert config.site is None
        assert config.collection is None

    def test_config_file_not_ran_if_self_config_loaded_equals_true(self, tmp_path):
        config_file = _write_config(
            tmp_path,
            content="""
module="app"
site="app"
editor="nvim"
""",
        )
        config = ApiConfig(config_file=config_file, _config_loaded=True)
        assert config.module is None
        assert config.site is None
        assert config.collection is None

    def test_editor_from_config(self, tmp_path, monkeypatch):
        """Reads the editor value from the config file."""
        config_file = _write_config(tmp_path, content='[tool.render-engine.cli]\neditor="nvim"\n')
        config = ApiConfig(config_file=config_file)
        assert config.editor == "nvim"

    def test_editor_falls_back_to_env(self, tmp_path, monkeypatch):
        """Falls back to the EDITOR environment variable when not in config."""
        monkeypatch.setenv("EDITOR", "fake-editor")
        config = ApiConfig()
        assert config.editor == "fake-editor"

    def test_editor_none_when_not_set(self, monkeypatch):
        """Returns None when editor is not in config or environment."""
        monkeypatch.delenv("EDITOR")
        config = ApiConfig()
        assert config.editor is None


class TestApiConfigLazyLoading:
    """Tests that ApiConfig lazily loads the config on first property access."""

    def test_config_not_loaded_until_property_accessed(self, tmp_path):
        """Config file is not read until a property is first accessed."""
        config_file = _write_config(
            tmp_path,
            """
[tool.render-engine.cli]
module = "myapp"
site = "MySite"
""",
        )
        config = ApiConfig(config_file=config_file)
        assert config._config_loaded is False
        _ = config.module
        assert config._config_loaded is True
