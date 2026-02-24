import io
import json
import logging
import os 
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

import picture_of_the_day.logic as logic


api = FastAPI()
logger = logging.getLogger("picture-of-the-day")

# @api.get("/")
# def read_root(request: Request):
#     user_agent = request.headers.get('user-agent')
#     return {"Hello": "World", "User-Agent": user_agent, "pwd": os.getcwd()}

@api.get("/api/admin/initialized")
def is_admin_initialized():
    return {"initialized": logic.is_admin_initialized(), "path": os.path.abspath(os.path.join(logic.CONFIGDIR, "admin.json"))}

@api.get("api/admin/albums")
def get_albums(request: Request):
    return {}

@api.get("api/admin/album/{album_id}")
def get_album(request: Request, album_id: int):
    return {}

@api.post("api/admin/album/{album_id}/photo_of_day")
def set_day(request: Request, album_id: int):
    return {}


api.mount("/", StaticFiles(directory="picture_of_the_day/ui", html=True), name="admin_frontend")

def run_server(args):
    uvicorn.run(api, host="0.0.0.0", port=args.port)
