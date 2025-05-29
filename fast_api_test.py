import sys
from typing import List, Tuple, Union

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from fastapi import Depends

from config import ODOO_REPO_PATH, ODOO_CONFIG_PATH, ODOO_DB_NAME

sys.path.insert(0, ODOO_REPO_PATH)

try:
    import odoo
except ImportError:
    raise ImportError("Odoo is not installed, please configure the path to the odoo repository")

from pydantic import BaseModel
from pydantic import field_validator, Field
from odoo.api import Environment

# odoo.tools.config.parse_config(
#     ["--config", "D:\Odoo-16-dev\conf\odoo-me.conf", "-d", "odoo-16-pms-db-test-1"])

odoo.tools.config.parse_config(
    ["--config", ODOO_CONFIG_PATH, "-d", ODOO_DB_NAME])

from odoo.addons.management.helpers import model_helper as m_helper


class OdooService:
    # was_initialized = False

    @staticmethod
    def odoo_env() -> Environment:
        # passe the odoo config # -c D:\Odoo-16-dev\conf\odoo-me.conf -d odoo-16-pms-db-test-1
        # if not OdooService.was_initialized:
        #     odoo.tools.config.parse_config(
        #         ["--config", "D:\Odoo-16-dev\conf\odoo-me.conf", "-d", "odoo-16-pms-db-test-1"])
        #     OdooService.was_initialized = True
        odoo_registry = odoo.registry(odoo.tools.config['db_name']).check_signaling()

        with odoo_registry.manage_changes():
            with odoo_registry.cursor() as cr:
                yield Environment(cr, odoo.SUPERUSER_ID, {})


class PartnerResponse(BaseModel):
    id: int
    name: str
    email: None | str = None
    states: Union[List[Tuple[str, str]], None] = None
    # states: List[Tuple[str, str]]


app = FastAPI(title="FastAPI with Odoo")

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/api/v1/res_partners/{partner_id}", response_model=PartnerResponse)
def get_partner(partner_id: int, odoo_env: Environment = Depends(OdooService.odoo_env)):
    # my_env = OdooService.odoo_env()
    # get first partner in the database
    partner = odoo_env['res.partner'].sudo().search([('id', '=', partner_id)], limit=1)
    # return the partner name
    states = m_helper.IRAQ_STATES

    return PartnerResponse(id=partner.id, name=partner.name, email=partner.email, states=states)


class AddMessageRequest(BaseModel):
    message: str = Field(..., title="The message to add", description="The message to add", min_length=3, max_length=10)

    # @field_validator("message")
    # def validate_message(cls, v):
    #     if len(v) < 3:
    #         raise ValueError("message is too short")
    #     return v


class AddMessageResponse(AddMessageRequest):
    partner_id: int


# add comment on partner (receive message and partner id) (message in request body)
@app.post("/api/v1/res_partner/{partner_id}/comment", response_model=AddMessageResponse)
def add_comment(partner_id: int, message_request: AddMessageRequest,
                odoo_env: Environment = Depends(OdooService.odoo_env)):
    # get partner
    partner = odoo_env['res.partner'].sudo().search([('id', '=', partner_id)], limit=1)
    # create comment
    partner.message_post(body=message_request.message)
    return AddMessageResponse(partner_id=partner_id, message=message_request.message)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

# # run fastapii using uvicorn
# def main():
#     # import uvicorn
#     # uvicorn.run(app, host="localhost", port=8000)
#     ## Run the app using fastapi command like fastapi dev fast_api_test ......
#     # import sys
#     # import os
#     # os.system(f"fastapi run {sys.argv[0]}:{app}")
#
#
# main()
