
# pyconfig-loader

`pyconfig-loader` is a simple Python library for loading configurations from different sources such as environment variables and configuration files (JSON/YAML). It supports flexible configurations with features like default values, required keys, and filtering based on key prefixes.

## Installation

To install the package, you can use `pip`:

```bash
pip install pyconfig-loader
```

Alternatively, you can install it from the source using `poetry`:

```bash
poetry install
```

## Usage

### 1. Loading Configuration from Environment Variables

You can load configuration directly from environment variables, optionally filtering by key prefix, providing default values, or marking certain variables as required.

```python
from pyconfig_loader import ConfigLoader

# Example of loading configuration from environment variables
loader = ConfigLoader("env")

# Load with required keys and default values
config = loader.load_from_env(
    required_keys=["DB_USERNAME", "DB_PASSWORD"],
    default_values={"DB_PASSWORD": "default_pass"},
    key_prefix="DB_"
)

print(config)
```

This would output a dictionary like:

```python
{
    'DB_USERNAME': 'admin',   # from env
    'DB_PASSWORD': 'default_pass'  # default value as it's missing in the environment
}
```

### 2. Loading Configuration from a File (JSON or YAML)

You can also load configuration from a file, supporting both JSON and YAML formats.

#### JSON Example:

```json
{
    "DB_USERNAME": "admin",
    "DB_PASSWORD": "secret"
}
```

#### YAML Example:

```yaml
DB_USERNAME: admin
DB_PASSWORD: secret
```

```python
from pyconfig_loader import ConfigLoader

# Example of loading configuration from a JSON or YAML file
loader = ConfigLoader("path/to/config.json")  # Or "path/to/config.yaml"
config = loader.load()

print(config)
```

### 3. Error Handling

By default, if required environment variables are missing, a `ValueError` will be raised. You can modify this behavior with the `raise_on_missing` argument.

```python
config = loader.load_from_env(
    required_keys=["DB_USERNAME", "DB_PASSWORD"],
    raise_on_missing=False  # Will not raise an error if keys are missing
)
```

### 4. Advanced Configuration Features

- **Prefix Filtering:** You can filter environment variables based on a prefix (e.g., load only variables starting with `DB_`).
- **Default Values:** Specify default values for missing environment variables.
- **Required Keys:** Define which environment variables are required to exist in the configuration, and optionally set default values for them.

```python
config = loader.load_from_env(
    required_keys=["API_KEY", "DB_PASSWORD"],
    default_values={"DB_PASSWORD": "default_pass"},
    key_prefix="APP_"
)
```

## Development

To contribute to `pyconfig-loader`, you can clone the repository and use `poetry` to manage dependencies and run tests.

```bash
git clone https://github.com/yourusername/pyconfig-loader.git
cd pyconfig-loader
poetry install
poetry run pytest  # To run tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
