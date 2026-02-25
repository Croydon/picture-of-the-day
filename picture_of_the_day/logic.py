import json
import os
import logging
import random 

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
    if not day in config.config["albums"][album_id]["pods"]:
        if not day == config.get_current_day():
            # We only implicitly auto-generate a random POD here if the call is for the current day
            # Random pre-generation of PODs should happen explicit elsewhere
            return None
        random_photoid = get_random_photoid(album_id)
        return random_photoid
        # TODO: Save it actually later on
        # set_pod(album_id, day, random_photoid, "random")
        
    return config.config["albums"][album_id]["pods"][day]["photo_id"]

def get_pod_photo_bytes(album_id, day=None) -> [bytes, str]:
    if day is None:
        day = config.get_current_day()
    photoid = get_pod_photoid(album_id, day)
    if photoid is not None:
        return get_photo_bytes(album_id, photoid)
    return None, None

def get_pod_set_by(album_id, day):
    if day in config.config["albums"][album_id]["pods"]:
        return config.config["albums"][album_id]["pods"][day]["set_by"]
    return None

def set_pod(album_id, day, photo_id, set_by):
    config.set_pod(album_id, day, photo_id, set_by)

def update_album_photos(album_id):
    actual_photos = nc_handler.nc_get_album_photos(album_id)
    # print(actual_photos)

    config.update_album_photos_config(album_id=album_id, actual_photos=actual_photos)

def get_album_photos(album_id):
    return config.get_album_photos(album_id)

def get_unused_photos(album_id):
    # This returnes photos that were POD in the past
    # AND photos that are planned to become POD
    return config.get_unused_photos(album_id)

def get_random_photoid(album_id) -> str:
    # Opinioned function to return a photo
    # that from the perspective of the end user looks random
    # also it isn't entirely random

    # First fetch the album's photos
    update_album_photos(album_id)

    # If there are photos that weren't POD so far,
    # nor are planned as a POD
    # prefer those
    unused_photos = get_unused_photos(album_id)
    if len(unused_photos) >= 1:
        return random.choice(unused_photos)
    else:
        # If all photos are/will be PODs already
        # choose a random picture out of all
        all_photos = get_album_photos()
        return random.choice(all_photos)

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
