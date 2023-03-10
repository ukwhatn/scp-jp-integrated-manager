import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import root
from routers.layout_support import layout_support
from routers.users import application as users_application

# for db import
# import sys
# sys.path.append("/user_modules")

# logger config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

# create app
app = FastAPI()

# mount static folder
app.mount("/static", StaticFiles(directory="/app/static"), name="static")

# add routers
app.include_router(
    root.router
)

app.include_router(
    users_application.router
)

app.include_router(
    layout_support.router
)
