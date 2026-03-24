import schedule

from picture_of_the_day import config


def cache_pods():
    albums = config.get_albums()
    for album in albums:
        __photo_bytes, __mime_type = logic.get_pod_photo_bytes(album_id)

def init_jobs():
    schedule.every().day.at("00:01", config.get_timezone_config()).do(cache_pods)
