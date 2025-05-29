import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

## Odoo Server config
ODOO_REPO_PATH = str(os.getenv("ODOO_REPO_PATH", "")).strip()
ODOO_CONFIG_PATH = str(os.getenv("ODOO_CONFIG_PATH", "")).strip()
ODOO_DB_NAME = str(os.getenv("ODOO_DB_NAME", "")).strip()

assert ODOO_CONFIG_PATH, "ODOO_CONFIG_PATH is required"
assert ODOO_DB_NAME, "ODOO_DB_NAME is required"
