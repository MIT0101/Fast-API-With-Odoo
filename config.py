from typing import Any
from dotenv import dotenv_values

REQUIRED_ENV_VARS = {"ODOO_DB_NAME", "ODOO_CONFIG_PATH", "ODOO_REPO_PATH"}
parsed_config = dotenv_values("./.env")


def validate_config(config_vals: dict[str, Any]):
    validated_config = {}
    for var in REQUIRED_ENV_VARS:
        value = config_vals.get(var)
        if not value:
            raise ValueError(f"The {var} ENV variable is required")
        validated_config[var] = value
    return validated_config


config = dict(parsed_config)
validated_config = validate_config(config)
ODOO_REPO_PATH = config.get("ODOO_REPO_PATH")
ODOO_CONFIG_PATH = config.get("ODOO_CONFIG_PATH")
ODOO_DB_NAME = config.get("ODOO_DB_NAME")
