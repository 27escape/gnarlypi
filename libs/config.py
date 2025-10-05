# simple class to read and write a YAML configuration file

# Example usage:
# config = Config('/path/to/config.yaml')
# or set the GNARLYPI_CONFIG environment variable
# config = Config()
# value = config.get('key')
# its possible to get nested values using dot notation
# value2 = config.get('key2.subkey')
# config.set('key', 'value')
# config.save()


import os
import re

# import yaml
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


class Config:
    def __init__(self, filepath=None):
        self.filepath = filepath or os.getenv("GNARLYPI_CONFIG")
        if not self.filepath:
            raise ValueError(
                "No configuration file path provided and GNARLYPI_CONFIG environment variable is not set."
            )
        self.data = {}
        self.updated = False
        self._load()

    def _substitute_references(self):
        """Substitute references to other fields (e.g., $(key)) and environment variables (e.g., ${VAR})
        in the loaded YAML data.
        """
        ref_pattern = re.compile(r"\$\(([^)]+)\)")
        # New pattern for environment variables: ${VAR}
        env_pattern = re.compile(r"\$\{([^}^{]+)\}")

        def replace_env_var(match):
            """Helper to replace ${VAR} with os.getenv('VAR')."""
            var = match.group(1)
            value = os.getenv(var)
            return value if value is not None else match.group(0)

        def replace_all(value):
            if isinstance(value, str):
                # First, substitute environment variables
                value = env_pattern.sub(replace_env_var, value)
                # Second, substitute internal references
                return ref_pattern.sub(
                    lambda match: self.get(match.group(1), match.group(0)), value
                )
            return value

        def walk_and_substitute(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        walk_and_substitute(value)
                    elif isinstance(value, list):
                        data[key] = [
                            replace_all(item) if isinstance(item, str) else item
                            for item in value
                        ]
                    else:
                        data[key] = replace_all(value)
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    if isinstance(item, dict):
                        walk_and_substitute(item)
                    elif isinstance(item, str):
                        data[index] = replace_all(item)

        walk_and_substitute(self.data)


    def _load(self):
        """Load the YAML file into the data dictionary.""" # Removed old reference to env var sub
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as file:
                content = file.read()
                # content = self._substitute_env_vars(content) # REMOVE THIS LINE
                self.data = yaml.load(content) or {}
                self._substitute_references() # This now handles both env vars and internal references
                if not self.data:
                    raise ValueError(
                        f"Invalid YAML content in configuration file {self.filepath}"
                    )
        else:
            raise ValueError(f"Invalid path to config file {self.filepath}")
        
    def _get_nested(self, keys, default=None):
        """Get a value from a nested dictionary using a list of keys."""
        data = self.data
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    def _set_nested(self, keys, value):
        """Set a value in a nested dictionary using a list of keys."""
        data = self.data
        for key in keys[:-1]:
            if key not in data or not isinstance(data[key], dict):
                data[key] = {}
            data = data[key]
        data[keys[-1]] = value

    def get(self, key, default=None):
        """Get a value from the configuration data."""
        keys = key.split(".")
        return self._get_nested(keys, default)

    def set(self, key, value):
        """Set a value in the configuration data."""
        keys = key.split(".")
        self._set_nested(keys, value)
        self.updated = True

    def save(self):
        """Save the configuration data back to the YAML file."""
        if self.updated:
            with open(self.filepath, "w") as file:
                yaml.dump(self.data, file)
