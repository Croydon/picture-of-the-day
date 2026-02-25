import json
import os
import logging

import picture_of_the_day.nc_handler as nc_handler
import picture_of_the_day.config as config

logger = logging.getLogger("picture-of-the-day")
logger.setLevel(logging.DEBUG)

def update_album_photos(album_id):
    actual_photos = nc_handler.nc_get_album_photos(album_id)

    config.update_album_photos_config(album_id=album_id, actual_photos=actual_photos)

def get_album(album_id):
    return None


def get_pod_photoid(album_id, day):
    if day in config.config["albums"][album_id]["pods"]:
        return config.config["albums"][album_id]["pods"][day]["photo_id"]
    return None

def get_pod_set_by(album_id, day):
    if day in config.config["albums"][album_id]["pods"]:
        return config.config["albums"][album_id]["pods"][day]["set_by"]
    return None

def set_pod(album_id, day, photo_id, set_by):
    config.set_pod(album_id, day, photo_id, set_by)
