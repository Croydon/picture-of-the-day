import json
import os
import logging
import random 
import io

import exifread

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

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

def write_on_photo_bytes(photo_bytes, text: str, mime_type: str):
    fh = io.BytesIO(photo_bytes)
    fh.seek(0)

    img = Image.open(fh).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_path = os.path.join("picture_of_the_day", "ui", "assets", "fonts", "noto_sans", "NotoSans-Variable.ttf")

    # Try to scale font size reasonable
    percentage_of_photo_scale = 0.07
    min_px = 30
    font_size = max(min_px, int(min(img.size) * percentage_of_photo_scale))

    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        font = ImageFont.load_default(font_size)

    # Measure text
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_w = right - left
    text_h = bottom - top

    # Bottom-left position
    x = 120
    y = img.height - text_h - 140

    # Outline around text
    draw.text((x - 5, y), text, font=font, fill="black")
    draw.text((x + 5, y), text, font=font, fill="black")
    draw.text((x, y - 5), text, font=font, fill="black")
    draw.text((x, y + 5), text, font=font, fill="black")

    # Text itself
    draw.text((x, y), text, font=font, fill="white")

    out = io.BytesIO()
    save_options = {"format": "JPEG"}
    if "jpeg" in mime_type:
        save_options["quality"] = 100

    img.save(out, **save_options)
    return out.getvalue()

def get_pod_photo_bytes(album_id, day=None, overlay=True) -> [bytes, str]:
    if day is None:
        day = config.get_current_day()
    photoid = get_pod_photoid(album_id, day)
    if photoid is not None:
        photo_bytes, mime_type = get_photo_bytes(album_id, photoid)
        if overlay:
            photo_creationtime = get_photo_exif_creationtime(photo_bytes)
            print(photo_creationtime)
            if photo_creationtime is not None:
                photo_bytes = write_on_photo_bytes(photo_bytes, photo_creationtime.strftime("%d.%m.%Y"), mime_type)
        return photo_bytes, mime_type
    return None, None

def get_pod_set_by(album_id, day):
    if day in config.config["albums"][album_id]["pods"]:
        return config.config["albums"][album_id]["pods"][day]["set_by"]
    return None

def set_pod(album_id, day, photo_id, set_by):
    config.set_pod(album_id, day, photo_id, set_by)

def update_albums():
    nc_handler.nc_get_albums()
    # TODO: Implement logic for adding new album to config, removing deleted albums from config (i.e. renaming them with a deleted prefix for now or something), and actually saving the config file again

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

def _parse_exif_times(exif_time: str):
    exif_time = exif_time.strip()
    try:
        return datetime.strptime(exif_time, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        pass

    try:
        return datetime.strptime(exif_time[:19], "%Y:%m:%d %H:%M:%S")
    except ValueError:
        return None

def get_photo_exif_creationtime(photo_bytes):
    # TODO: Handle EXIF OffsetTime if existing
    fh = io.BytesIO(photo_bytes)
    fh.seek(0)
    tags = exifread.process_file(fh, details=False)
    # print(tags)
    for tag in ["EXIF DateTimeOriginal", "DateTimeOriginal", "EXIF SubSecTimeOriginal", "EXIF DateTimeDigitized", "DateTimeDigitized", "EXIF SubSecTimeDigitized"]:
        # consider "DateTime" , but this is probably just file creation time
        if tag in tags:
            print(str(tags[tag]))
            return _parse_exif_times(str(tags[tag]))

    return None
    

def get_photo_mimetype(album_id, photo_id):
    # keep album_id even when unused currently
    # maybe this should be smarter in the future
    file_ending = photo_id.rsplit(".", 1)[-1]
    if file_ending.lower() == "jpg" or file_ending.lower() == "JPEG":
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

def is_album_access_authenticated(album_id: str, provided_access_token: str) -> bool:
    if album_id not in config.config["albums"]:
        return False
    
    if "access_token" not in config.config["albums"][album_id]:
        return False

    if config.config["albums"][album_id]["access_token"] == provided_access_token:
        return True

    return False
