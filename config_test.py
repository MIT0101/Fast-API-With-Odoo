import pytest
from config import validate_config


def test_validate_config_success():
    config_vals = {
        "ODOO_DB_NAME": "test_db",
        "ODOO_CONFIG_PATH": "/path/to/config",
        "ODOO_REPO_PATH": "/path/to/repo",
    }
    validated = validate_config(config_vals)
    assert validated["ODOO_DB_NAME"] == "test_db"
    assert validated["ODOO_CONFIG_PATH"] == "/path/to/config"
    assert validated["ODOO_REPO_PATH"] == "/path/to/repo"


@pytest.mark.parametrize(
    "missing_key", ["ODOO_DB_NAME", "ODOO_CONFIG_PATH", "ODOO_REPO_PATH"]
)
def test_validate_config_missing_var(missing_key):
    config_vals = {
        "ODOO_DB_NAME": "test_db",
        "ODOO_CONFIG_PATH": "/path/to/config",
        "ODOO_REPO_PATH": "/path/to/repo",
    }
    config_vals.pop(missing_key)
    with pytest.raises(ValueError) as excinfo:
        validate_config(config_vals)
    assert missing_key in str(excinfo.value)
