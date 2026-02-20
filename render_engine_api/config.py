import sys

# TODO: Remove tomli fallback once Python 3.10 is no longer supported
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from dataclasses import dataclass
from os import getenv
from pathlib import Path

from rich import print as rprint

CONFIG_FILE_NAME = Path("pyproject.toml")


@dataclass
class ApiConfig:
    """Handles loading and storing the config from disk"""

    # Initialize the arguments and default values
    _module: str | None = None
    _site: str | None = None
    _collection: str | None = None
    _config_loaded: bool = False
    config_file: str | Path | None = CONFIG_FILE_NAME

    def __post_init__(self):
        self._editor = getenv("EDITOR")

    # Properties are only updated if needed.
    # Check via self.load_config if previously run.
    @property
    def module(self):
        self.load_config()
        return self._module

    @property
    def site(self):
        self.load_config()
        return self._site

    @property
    def collection(self):
        self.load_config()
        return self._collection

    @property
    def editor(self):
        self.load_config()
        return self._editor

    def load_config(self) -> None:
        """
        Load the config from the file.
        This should only be run once per ApiConfig call.
        """

        if self._config_loaded or not self.config_file:
            return

        # set self.config_loaded to prevent from running multiple times
        self._config_loaded = True

        stored_config = {}
        try:
            with open(self.config_file, "rb") as stored_config_file:
                try:
                    stored_config = (
                        tomllib.load(stored_config_file).get("tool", {}).get("render-engine", {}).get("cli", {})
                    )
                except tomllib.TOMLDecodeError as exc:
                    # TODO: Raise a custom except that can be caught in try/except in tooling
                    # raise ConfigFileError("Error parsing config_file") from exc
                    rprint(
                        f"[red]Encountered an error while parsing {self.config_file}[/red]\n{exc}\n",
                        file=sys.stderr,
                    )
                    return
                else:
                    rprint(f"Config loaded from {self.config_file}")
        except FileNotFoundError:
            # TODO: Raise a custom except that can be caught in try/except in tooling
            rprint(f"No config file found at {self.config_file}")
            return

        self._editor = stored_config.get("editor", self._editor)
        self._module = stored_config.get("module")
        self._site = stored_config.get("site")
        self._collection = stored_config.get("collection")
