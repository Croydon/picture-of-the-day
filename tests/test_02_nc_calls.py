import pytest
import os
import hashlib

from picture_of_the_day.api import api
import picture_of_the_day.logic as logic
import picture_of_the_day.nc_handler as nc_handler
import picture_of_the_day.config as config


def test_nc_is_instance_reachable_false(monkeypatch):
    monkeypatch.setenv("POD_NC_URL", "https://localhost:12345/nonexistent")
    monkeypatch.setenv("POD_NC_USERNAME", "nonexistent")
    monkeypatch.setenv("POD_NC_ACCESSTOKEN", "nonexistent")
    monkeypatch.setenv("POD_ADMIN_USERNAME", "nonexistent")
    monkeypatch.setenv("POD_ADMIN_PASSWORD", "nonexistent")
    assert nc_handler.nc_is_instance_reachable(caching=False) == False

###
### Tests that require an connection to a Nextcloud instance
###
@pytest.mark.skipif(not config.is_admin_initialized(), reason="core config is not set")
def test_nc_is_instance_reachable_true():
    assert nc_handler.nc_is_instance_reachable(caching=False) == True

@pytest.mark.skipif(not nc_handler.nc_is_instance_reachable(), reason="NC instance is unavailable")
def test_nc_get_albums():
    response = nc_handler.nc_get_albums()
    print(response)
    assert "pod-test-album" in response


@pytest.mark.skipif(not nc_handler.nc_is_instance_reachable(), reason="NC instance is unavailable")
def test_nc_get_album_photos():
    response = nc_handler.nc_get_album_photos("pod-test-album")
    print(response)
    search_for = ["cat_peeking", "cat_face_closeup", "young_cat", "moon"]
    download_photo_id = None
    for image_id in response:
        for search_term in search_for:
            if search_term in image_id:
                search_for.remove(search_term)
                if search_term == "cat_peeking":
                    download_photo_id = image_id
    assert [] == search_for

    downloaded_path = nc_handler.nc_get_photo("pod-test-album", download_photo_id)

    with open(downloaded_path, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")

    assert "744455716ad49d53c2f0037db39f667fc3a60b338df7e6a2569ec3ba47b69dab" == digest.hexdigest()
