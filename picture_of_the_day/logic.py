import json
import os
import logging

logger = logging.getLogger("picture-of-the-day")
logger.setLevel(logging.DEBUG)

CONFIGDIR = os.environ.get("POD_CONFIG_DIR", os.path.join("config"))

config_admin = {}


def is_admin_initialized():
    if not os.path.exists(os.path.join(CONFIGDIR, "admin.json")):
        return False
    with open(os.path.join(CONFIGDIR, "admin.json"), "r") as f:
        config_admin = json.load(f)
        if not all(k in config_admin for k in ["nc_url", "nc_username", "nc_accesstoken", "admin_username", "admin_password"]):
            return False
        return True


def get_nc_albums():
    return None

def get_nc_album(album_id):
    return None

def get_album(album_id):
    return None

def set_photo_of_day(album_id, photo_id):
    return None
