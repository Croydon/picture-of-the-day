import json
import os
import logging

from datetime import datetime
from zoneinfo import ZoneInfo

import picture_of_the_day.nc_handler as nc_handler
import picture_of_the_day.config as config

logger = logging.getLogger("picture-of-the-day")
logger.setLevel(logging.DEBUG)

def update_album_photos(album_id):
    actual_photos = nc_handler.nc_get_album_photos(album_id)

    config.update_album_photos_config(album_id=album_id, actual_photos=actual_photos)

def get_album(album_id):
    return None

def set_photo_of_day(album_id, photo_id):
    return None
