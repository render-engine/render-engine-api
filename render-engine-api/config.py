import toml
from dataclasses import dataclass
from toml import TomlDecodeError

CONFIG_FILE_NAME = "pyproject.toml"

@dataclass
class CliConfig:
    """Handles loading and storing the config from disk"""

    @property
    def module_site(self):
        if not self._config_loaded:
            self.load_config()
            self._config_loaded = True
        return self._module_site

    @property
    def collection(self):
        if not self._config_loaded:
            self.load_config()
            self._config_loaded = True
        return self._collection

    @property
    def editor(self):
        if not self._config_loaded:
            self.load_config()
            self._config_loaded = True
        return self._editor

    # Initialize the arguments and default values
    _module_site: str = None
    _collection: str = None
    default_module_site: str = None
    default_collection: str = None
    _editor: str = None
    _config_loaded: bool = False

    def load_config(self, config_file: str = CONFIG_FILE_NAME):
        """Load the config from the file"""
        stored_config = {}
        try:
            with open(config_file) as stored_config_file:
                try:
                    stored_config = (
                        toml.load(stored_config_file).get("tool", {}).get("render-engine", {}).get("cli", {})
                    )
                except TomlDecodeError as exc:
                    click.echo(
                        f"{click.style(f'Encountered an error while parsing {config_file}', fg='red')}\n{exc}\n",
                        err=True,
                    )
                else:
                    click.echo(f"Config loaded from {config_file}")
        except FileNotFoundError:
            click.echo(f"No config file found at {config_file}")

        self._editor = stored_config.get("editor", getenv("EDITOR"))
        if stored_config:
            # Populate the argument variables and default values from the config
            if (module := stored_config.get("module")) and (site := stored_config.get("site")):
                self._module_site = f"{module}:{site}"
            if default_collection := stored_config.get("collection"):
                self._collection = default_collection

