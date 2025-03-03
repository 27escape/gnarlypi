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
yaml=YAML(typ="safe")



class Config:
    def __init__(self, filepath=None):
        self.filepath = filepath or os.getenv('GNARLYPI_CONFIG')
        if not self.filepath:
            raise ValueError("No configuration file path provided and GNARLYPI_CONFIG environment variable is not set.")
        self.data = {}
        self.updated = False
        self._load()

    def _substitute_env_vars(self, content):
        """Substitute environment variables and references to other fields in the YAML content."""
        # Environment variable pattern ${HOME}
        env_pattern = re.compile(r'\$\{([^}^{]+)\}')
        # Reference pattern $(key.subkey)
        ref_pattern = re.compile(r'\$\(([^)]+)\)')

        # Substitute environment variables
        content = env_pattern.sub(lambda match: os.getenv(match.group(1), match.group(0)), content)
        #  partial update to ensure we can reference other fields
        self.data = yaml.load(content) or {}

        # Substitute references to other fields
        def replace_ref(match):
            ref_key = match.group(1)
            ref_value = self.get(ref_key)
            return ref_value if ref_value is not None else match.group(0)

        content = ref_pattern.sub(replace_ref, content)
        # final update with references resolved
        self.data = yaml.load(content) or {}

    def _load(self):
        """Load the YAML file into the data dictionary and substitute environment variables."""
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                content = file.read()\
                # this will also update the data dictionary
                self._substitute_env_vars(content)
                if not self.data:
                    raise ValueError(f"Invalid YAML content in configuration file {self.filepath}")
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
        keys = key.split('.')
        return self._get_nested(keys, default)

    def set(self, key, value):
        """Set a value in the configuration data."""
        keys = key.split('.')
        self._set_nested(keys, value)
        self.updated = True

    def save(self):
        """Save the configuration data back to the YAML file."""
        if self.updated:
            with open(self.filepath, 'w') as file:
                yaml.dump(self.data, file)
