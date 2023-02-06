import logging
import sys

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

sys.path.append("/user_modules")

from db.cruds import user_application_password

# logger
logger = logging.getLogger(__name__)

# router
router = APIRouter(
    tags=["application"],
    prefix="/users/application"
)

# jinja2 template
templates = Jinja2Templates(directory="templates/users/application")


@router.get("/")
def root(
        request: Request,
        i: int = None
):
    if i is None:
        return "EMPTY"

    password = user_application_password.get(i)

    return templates.TemplateResponse(
        "view.html",
        {"request": request, "password": password}
    )
