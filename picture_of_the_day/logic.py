import json
import os
import logging

import picture_of_the_day.nc_handler as nc_handler
import picture_of_the_day.config as config

logger = logging.getLogger("picture-of-the-day")
logger.setLevel(logging.DEBUG)

def init():
    config.load_core_config()
    nc_handler.nc_is_instance_reachable()

def get_pod_photoid(album_id, day=None):
    if day is None:
        day = config.get_current_day()
    if day in config.config["albums"][album_id]["pods"]:
        return config.config["albums"][album_id]["pods"][day]["photo_id"]
    return None

def get_pod_photo_bytes(album_id, day=None) -> [bytes, str]:
    if day is None:
        day = config.get_current_day()
    if day in config.config["albums"][album_id]["pods"]:
        return get_photo_bytes(album_id, get_pod_photoid(album_id, day))
    return None, None

def get_pod_set_by(album_id, day):
    if day in config.config["albums"][album_id]["pods"]:
        return config.config["albums"][album_id]["pods"][day]["set_by"]
    return None

def set_pod(album_id, day, photo_id, set_by):
    config.set_pod(album_id, day, photo_id, set_by)

def update_album_photos(album_id):
    actual_photos = nc_handler.nc_get_album_photos(album_id)

    config.update_album_photos_config(album_id=album_id, actual_photos=actual_photos)

def get_album_photos(album_id):
    return config.get_album_photos(album_id)

def get_unused_photos(album_id):
    return config.get_unused_photos(album_id)

def get_local_photo_path(album_id, photo_id):
    return f"cache/{album_id}/{photo_id}"

def get_photo_mimetype(album_id, photo_id):
    # keep album_id even when unused currently
    # maybe this should be smarter in the future
    file_ending = photo_id.rsplit(".", 1)[-1]
    if file_ending == "jpg":
        file_ending = "jpeg"
    
    return f"image/{file_ending}"

def get_photo_bytes(album_id, photo_id) -> [bytes, str]:
    # TODO: Improve cache logic
    photo_path = get_local_photo_path(album_id, photo_id)
    if not os.path.exists(photo_path):
        __photo_path = nc_handler.nc_get_photo(album_id, photo_id)

    mime_type = None
    photo_bytes = None
    with open(photo_path, "rb") as f:
        photo_bytes = f.read()
        mime_type = get_photo_mimetype(album_id, photo_id)
    return photo_bytes, mime_type
