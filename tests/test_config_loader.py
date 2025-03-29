import os
import pytest
from pydantic import BaseModel

from pyconf_ezload.config_loader import ConfigLoader

# Sample config file content for testing
sample_json_config = '{"key1": "value1", "key2": "value2"}'
sample_yaml_config = """
key1: value1
key2: value2
"""


# Define a custom Pydantic model for testing
class TestConfigModel(BaseModel):
    key1: str
    key3: str


# Test loading from JSON file
@pytest.fixture
def json_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(sample_json_config)
    return config_file


# Test loading from YAML file
@pytest.fixture
def yaml_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(sample_yaml_config)
    return config_file


# Test loading from JSON file
def test_load_json_config(json_config):
    loader = ConfigLoader(config_source=str(json_config))
    config = loader.load()
    assert config == {"key1": "value1", "key2": "value2"}


def test_load_json_config_with_model(json_config):
    loader = ConfigLoader(config_source=str(json_config), config_model=TestConfigModel)
    config = loader.load()

    assert config == {"key1": "value1", "key2": "value2"}
    assert isinstance(config, dict)  # Ensure the result is a dictionary
    assert config["key1"] == "value1"  # Check specific key-value pairs
    assert config["key2"] == "value2"


# Test loading from YAML file
def test_load_yaml_config(yaml_config):
    loader = ConfigLoader(str(yaml_config))
    config = loader.load()
    assert config == {"key1": "value1", "key2": "value2"}


# Test loading from environment variables
def test_load_from_env_with_key_prefix(monkeypatch):
    # Setting environment variables
    monkeypatch.setenv("MYAPP_DB_USERNAME", "admin")
    monkeypatch.setenv("MYAPP_DB_PASSWORD", "1234")

    loader = ConfigLoader("env")
    config = loader.load_from_env(key_prefix="MYAPP")
    assert config == {"MYAPP_DB_USERNAME": "admin", "MYAPP_DB_PASSWORD": "1234"}


def test_load_from_env_required_and_default(monkeypatch):
    # Setting environment variables before loading the config
    monkeypatch.setenv("DB_USERNAME", "admin")

    loader = ConfigLoader("env")
    config = loader.load_from_env(
        required_keys=["DB_USERNAME", "DB_PASSWORD"],  # DB_PASSWORD is missing
        default_values={"DB_PASSWORD": "default_pass"},
        raise_on_missing=False,
    )

    # The test now expects DB_USERNAME to be "admin" and DB_PASSWORD to be set to the default
    assert config == {"DB_USERNAME": "admin", "DB_PASSWORD": "default_pass"}
