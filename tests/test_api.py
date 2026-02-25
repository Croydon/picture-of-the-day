import pytest
import os
import hashlib

from webdav3.client import Client as webdavclient
from fastapi.testclient import TestClient

from picture_of_the_day.api import api
import picture_of_the_day.logic as logic
import picture_of_the_day.nc_handler as nc_handler
import picture_of_the_day.config as config

client = TestClient(api)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_is_admin_initialized_false(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "empty"))
    monkeypatch.delenv("POD_NC_URL", raising=False)
    monkeypatch.delenv("POD_NC_USERNAME", raising=False)
    monkeypatch.delenv("POD_NC_ACCESSTOKEN", raising=False)

    response = client.get("/api/admin/initialized")
    assert response.status_code == 200
    data = response.json()
    assert "initialized" in response.json()
    assert data["initialized"] == False

def test_is_admin_initialized_true(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))

    response = client.get("/api/admin/initialized")
    assert response.status_code == 200
    data = response.json()
    assert "initialized" in response.json()
    assert data["initialized"] == True

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
    cat_peeking_id = None
    for image_id in response:
        for search_term in search_for:
            if search_term in image_id:
                search_for.remove(search_term)
                if search_term == "cat_peeking":
                    cat_peeking_id = image_id
    assert [] == search_for

    cat_seeking_path = nc_handler.nc_get_photo("pod-test-album", cat_peeking_id)

    with open(cat_seeking_path, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")

    assert "744455716ad49d53c2f0037db39f667fc3a60b338df7e6a2569ec3ba47b69dab" == digest.hexdigest()


###
### Further tests without an instance required
###
def test_get_pod(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    pod_id = logic.get_pod_photoid("pod-test-album", "2026-02-26")
    assert pod_id == "2.jpg"
    pod_set_by = logic.get_pod_set_by("pod-test-album", "2026-02-26")
    assert pod_set_by == "admin"

def test_set_pod(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    logic.set_pod("pod-test-album", "2026-02-26", "newphoto.jpg", "admin")

    pod_id = logic.get_pod_photoid("pod-test-album", "2026-02-26")
    assert pod_id == "newphoto.jpg"
    pod_set_by = logic.get_pod_set_by("pod-test-album", "2026-02-26")
    assert pod_set_by == "admin"

    logic.set_pod("pod-test-album", "3033-03-33", "newdate.jpg", "random")

    pod_id = logic.get_pod_photoid("pod-test-album", "3033-03-33")
    assert pod_id == "newdate.jpg"
    pod_set_by = logic.get_pod_set_by("pod-test-album", "3033-03-33")
    assert pod_set_by == "random"

def test_remove_photo_from_album_success(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    pod_id = logic.get_pod_photoid("pod-test-album", "4444-04-04")
    assert pod_id == "7.jpg"

    config._remove_photo_from_album_config("pod-test-album", "7.jpg")

    pod_id = logic.get_pod_photoid("pod-test-album", "4444-04-04")
    assert pod_id == None


def test_remove_photo_from_album_prevent_keep_history(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    pod_id = logic.get_pod_photoid("pod-test-album", "0888-01-01")
    assert pod_id == "0.jpg"

    config._remove_photo_from_album_config("pod-test-album", "0.jpg")

    pod_id = logic.get_pod_photoid("pod-test-album", "0888-01-01")
    assert pod_id == "0.jpg"


def test_get_unused_photos(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    unused_photos = logic.get_unused_photos("pod-test-album")

    assert "not_used_yet_1.jpg" in unused_photos
    assert "not_used_yet_2.jpg" in unused_photos
    assert 4 == len(unused_photos)
