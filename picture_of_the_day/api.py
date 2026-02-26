import io
import json
import logging
import os 
import uvicorn

from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

import picture_of_the_day.logic as logic
import picture_of_the_day.config as config
import picture_of_the_day.nc_handler as nc_handler


def init():
    logic.init()

api = FastAPI(dependencies=[Depends(init)])
logger = logging.getLogger("picture-of-the-day")

@api.get("/api/admin/initialized")
def is_admin_initialized():
    return {"initialized": config.is_admin_initialized(), "path": os.path.abspath(os.path.join(config.CONFIGDIR, "admin.json"))}

@api.get("/api/admin/albums")
def get_albums(request: Request):
    return nc_handler.nc_get_albums()


@api.get("/api/admin/album/{album_id}")
def get_album(request: Request, album_id: int):
    return {}

@api.post("/api/admin/album/{album_id}/photo_of_day")
def set_day(request: Request, album_id: int):
    return {}

@api.get("/api/album/{album_id}/{auth}/photo/today")
def get_pod(request: Request, album_id: str, auth: str):
    photo_bytes, mime_type = logic.get_pod_photo_bytes(album_id)
    return Response(photo_bytes, media_type=mime_type)

# api/album/pod-test-album/auth/photo/2026-03-07
@api.get("/api/album/{album_id}/{auth}/photo/{day}")
def get_pod(request: Request, album_id: str, auth: str, day: str):
    photo_bytes, mime_type = logic.get_pod_photo_bytes(album_id, day)

    if photo_bytes is None:
        return Response(status_code=404)

    return Response(content=photo_bytes, media_type=mime_type)

api.mount("/", StaticFiles(directory="picture_of_the_day/ui", html=True), name="admin_frontend")

def run_server(args):
    uvicorn.run(api, host="0.0.0.0", port=args.port)
