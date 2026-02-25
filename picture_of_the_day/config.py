import json
import os

CONFIGDIR = os.environ.get("POD_CONFIG_DIR", os.path.join("config"))

_config_init = {"core": {}, "albums": {}}
config = _config_init.copy()

# pods: ["YYYY-MM-DD": {photo_id: "photo_id", set_by: "admin|algo"}, ..]

def load_core_config():
    global config;
    if all(k in os.environ for k in ["POD_NC_URL", "POD_NC_USERNAME", "POD_NC_ACCESSTOKEN", "POD_ADMIN_USERNAME", "POD_ADMIN_PASSWORD"]):
        config["core"] = {
            "nc_url": os.environ["POD_NC_URL"],
            "nc_username": os.environ["POD_NC_USERNAME"],
            "nc_accesstoken": os.environ["POD_NC_ACCESSTOKEN"],
            "admin_username": os.environ["POD_ADMIN_USERNAME"],
            "admin_password": os.environ["POD_ADMIN_PASSWORD"]
        }
    elif os.path.exists(os.path.join(CONFIGDIR, "admin.json")):
        with open(os.path.join(CONFIGDIR, "admin.json"), "r") as f:
            config_file = json.load(f)
            if all(k in config_file["core"] for k in ["nc_url", "nc_username", "nc_accesstoken", "admin_username", "admin_password"]):
                config = config_file
    else:
        config = _config_init.copy()


def is_admin_initialized():
    load_core_config()
    if not all(k in config["core"] for k in ["nc_url", "nc_username", "nc_accesstoken", "admin_username", "admin_password"]):
        return False
    return True


def save_config():
    if not os.path.exists(CONFIGDIR):
        os.makedirs(CONFIGDIR)
    with open(os.path.join(CONFIGDIR, "admin.json"), "w") as f:
        json.dump(config, f, indent=4)


def _get_timezone_config():
    if "timezone" in config["core"]:
        return config["core"]["timezone"]
    else:
        return "Europa/Berlin"


def get_current_day():
    now = datetime.now(ZoneInfo(_get_timezone_config))
    return now.strftime("%Y-%m-%d")


def _remove_photo_from_album_config(album_id, photo_id):
    # remove only from future days and the current day, don't delete history data
    for pod_day, pod_obj in config["albums"][album_id]["pods"].items():
        if pod_day >= pod_photo["day"] >= get_current_day() and pod_obj["photo_id"] == photo_id:
            del config["albums"][album_id]["pods"][day]


def update_album_photos_config(album_id, actual_photos):
    # we haven't saved infos about the album yet
    if album_id not in config["albums"]:
        config["albums"][album_id] = {"photos": actual_photos, "pods": {}}
        save_config()
    else:
        # update already saved album
        if set(config["albums"][album_id]["photos"]) != set(actual_photos):
            for saved_photo in config["albums"][album_id]["photos"]:
                if saved_photo not in actual_photos:
                    _remove_photo_from_album_config(album_id, saved_photo)
            config["albums"][album_id]["photos"] = actual_photos
            save_config()


# def set_pod(album_id, day, photo_id, set_by="admin")
# def unset_pod(album_id, day)
# def get_random_photo_for_day(album_id)
# def set_random_photos_for_next_x_days(album_id, days=31, reset_existing=False)
