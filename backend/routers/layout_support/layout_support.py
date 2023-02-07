import logging

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from db.cruds import wiki_access_log as supporter_crud

# logger
logger = logging.getLogger(__name__)

# router
router = APIRouter(
    tags=["application"],
    prefix="/layout_support"
)


@router.get("/supporter")
def supporter(
        request: Request,
        site_name: str,
        path: str,
        user_id: int,
        user_unix_name: str,
):
    supporter_crud.create(
        site_name=site_name,
        path=path,
        user_id=user_id,
        user_unix_name=user_unix_name,
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent")
    )
    return FileResponse("static/layout_support/supporter.png")
