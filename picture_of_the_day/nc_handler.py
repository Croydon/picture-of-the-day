from webdav3.client import Client as webdavclient

import picture_of_the_day.logic as logic
import picture_of_the_day.config as config

_nc_instance_reachable = None
_client = None

# /remote.php/dav/photos/user/albums/
# /remote.php/dav/photos/user/albums/<album_id>
# apps/photos/api/v1/preview/id?etag=<>&x=512&y=512

def nc_is_instance_reachable(core_config=None, caching=True) -> bool:
    global _nc_instance_reachable;
    global _auth;
    global _client;

    if core_config is None:
        if not caching:
            config.load_core_config()
        core_config = config.config["core"]

    if caching and _nc_instance_reachable is not None:
        return _nc_instance_reachable

    try:
        client = webdavclient({"webdav_hostname": core_config["nc_url"], "webdav_login": core_config["nc_username"], "webdav_password": core_config["nc_accesstoken"]})

        if client.check(f"/remote.php/dav/photos/{core_config["nc_username"]}/albums/"):
            if client.list(f"/remote.php/dav/photos/{core_config["nc_username"]}/albums/"):
                _nc_instance_reachable = True
                _client = client
                return True
    except Exception as e:
        _nc_instance_reachable = False
        return False

def nc_get_albums():
    albums = _client.list(f"/remote.php/dav/photos/{config.config["core"]["nc_username"]}/albums/")
    return albums

def nc_get_album_photos(album_id):
    photos = _client.list(f"/remote.php/dav/photos/{config.config["core"]["nc_username"]}/albums/{album_id}")
    return photos

def nc_get_photo(photo_id):
    return None
