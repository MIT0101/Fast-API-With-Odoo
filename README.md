## Steps

1. Create python venv `python -m venv .venv` (3.10) example
   `/c/Users/MSI/AppData/Local/Programs/Python/Python310/python -m venv .venv`
2. Activate venv : `source ./.venv/Scripts/activate`
3. Upgrade pip `python -m pip install --upgrade pip`
4. ~~Clone odoo16 `git clone https://github.com/odoo/odoo.git odoo_repo --depth=1 --branch=16.0`~~
   ~~5. link odoo to .venv site package (get odoo library dir and config from server) example
   `mklink /d ".venv/Lib/site-packages/odoo" "D:\Odoo-16-dev\odoo\odoo"`~~
5. install requirements `pip install -r requirements.txt`
6. run fast api with odoo `fastapi dev fast_api_test.py` or `python uvicorn fast_api_test:app --reload`
7. Configure Environment Variables
    1. `ODOO_REPO_PATH` : Full path to odoo repository
    2. `ODOO_CONFIG_PATH` : Full path to odoo config file
    3. `ODOO_DB_NAME` : Database name to be used

<a style="color: #ff0000;">Note: </a>