import os
import json
import yaml
from typing import Any, Dict, Optional, List, Type

from pydantic import BaseModel, ValidationError


class ConfigLoader:
    def __init__(
        self, config_source: str, config_model: Optional[Type[BaseModel]] = None
    ):
        """Initialize the ConfigLoader with a given source for the config."""
        self.config_model = config_model
        self.config_source = config_source

    def load(self) -> Dict[str, Any]:
        """Load the configuration from the given source (file or environment)."""
        if self.config_source == "env":
            return self.load_from_env()
        elif os.path.isfile(self.config_source):
            return self.load_from_file(self.config_source)
        else:
            raise ValueError(f"Unsupported config source: {self.config_source}")

    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load the configuration from a file (JSON or YAML).
        Args:
            file_path: The path to the configuration file.
        Returns:
            A dictionary containing the configuration data.
        Raises:
            ValueError: If the file format is unsupported or if the configuration validation fails.
        """
        config_dict: dict = {}
        with open(file_path, "r") as file:
            if file_path.endswith(".json"):
                config_dict = json.load(file)
            elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
                config_dict = yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")

        # Validate the config data using the custom Pydantic model (if provided)
        if self.config_model:
            try:
                # Validate and return the config as a dict
                return self.config_model(**config_dict).model_dump()
            except ValidationError as e:
                raise ValueError(f"Configuration validation failed: {e}")

        return config_dict

    @staticmethod
    def load_from_env(
        required_keys: Optional[List[str]] = None,
        default_values: Optional[Dict[str, Any]] = None,
        key_prefix: Optional[str] = "",
        raise_on_missing: bool = True,
    ) -> Dict[str, Any]:
        """
        Load the configuration from environment variables with customizable options.
        Args:
            required_keys: A list of environment variable keys that are required.
            default_values: A dictionary of default values for missing keys.
            key_prefix: An optional prefix that all keys should match.
            raise_on_missing: If True, raises an error when a required key is missing.
        Returns:
            A dictionary with environment variables.
        """
        env_vars: dict = {}

        # Get all environment variables, filter by the key prefix if provided
        env_vars.update(
            {
                key: value
                for key, value in os.environ.items()
                if key_prefix and key.startswith(key_prefix)
            }
        )

        if required_keys:
            missing_keys = [key for key in required_keys if key not in env_vars]
            if raise_on_missing and missing_keys:
                raise ValueError(
                    f"Required environment variables {missing_keys} are missing."
                )
            env_vars.update(
                {
                    key: (
                        default_values.get(key, os.environ.get(key))
                        if default_values
                        else os.environ.get(key)
                    )
                    for key in missing_keys
                }
            )

        if default_values:
            env_vars.update(
                {
                    key: default_value
                    for key, default_value in default_values.items()
                    if key not in env_vars
                }
            )

        return env_vars
