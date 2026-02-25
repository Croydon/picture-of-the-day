import pytest
import os

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
    monkeypatch.setenv("POD_USERNAME", "nonexistent")
    monkeypatch.setenv("POD_ACCESSTOKEN", "nonexistent")
    assert nc_handler.nc_is_instance_reachable(caching=False) == False

###
### Tests that require an connection to a Nextcloud instance
###
@pytest.mark.skipif(not config.is_admin_initialized(), reason="core config is not set")
def test_nc_is_instance_reachable_true():
    # config loads are saved between tests run, we need to get back to an actual config
    config.load_core_config()

    assert nc_handler.nc_is_instance_reachable(caching=False) == True

@pytest.mark.skipif(not nc_handler.nc_is_instance_reachable(), reason="NC instance is unavailable")
def test_nc_get_albums():
    response = nc_handler.nc_get_albums()
    print(response)
    assert "pod-test-album/" in response


@pytest.mark.skipif(not nc_handler.nc_is_instance_reachable(), reason="NC instance is unavailable")
def test_nc_get_album_photos():
    response = nc_handler.nc_get_album_photos("pod-test-album/")
    print(response)
    search_for = ["cat_peeking", "cat_face_closeup", "young_cat", "moon"]
    for image_id in response:
        for search_term in search_for:
            if search_term in image_id:
                search_for.remove(search_term)
    assert [] == search_for
