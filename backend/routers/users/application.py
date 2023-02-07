import logging
import os

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from db.cruds import user_application_password, user_application_key

# logger
logger = logging.getLogger(__name__)

# router
router = APIRouter(
    tags=["application"],
    prefix="/users/application"
)

# jinja2 template
templates = Jinja2Templates(directory="templates/users/application")


@router.get("/password")
def show_password(
        request: Request,
        user_id: int = None,
        key: str = None
):
    # 引数未定義 or keyが有効でなければ、偽のパスワードを取得する
    if user_id is None or key is None or key not in user_application_key.get_active_keys():
        password = os.getenv("APPLICATION_PASSWORDS_FAKE")
    # それ以外はDB問い合わせ
    else:
        password = user_application_password.get(user_id)

    return templates.TemplateResponse(
        "view.html",
        {"request": request, "password": password}
    )


@router.get("/decode")
def decode_password(pw: str):
    return user_application_password.decode(pw)
