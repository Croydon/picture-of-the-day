import pytest
import os
import hashlib

from picture_of_the_day.api import api
import picture_of_the_day.logic as logic
import picture_of_the_day.nc_handler as nc_handler
import picture_of_the_day.config as config


###
### Basic tests with no NC instance required
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
    assert pod_id == "far_future_date.jpg"

    config._remove_photo_from_album_config("pod-test-album", "far_future_date.jpg")

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


def test_get_album_photos(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    photos = logic.get_album_photos("pod-test-album")

    assert "actual_existing_photo.jpg" in photos
    assert "1.jpg" in photos
    assert 13 == len(photos)


def test_get_unused_photos(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    unused_photos = logic.get_unused_photos("pod-test-album")

    assert "not_used_yet_1.jpg" in unused_photos
    assert "not_used_yet_2.jpg" in unused_photos
    assert 4 == len(unused_photos)

def test_get_photo_bytes(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    photo_bytes, mime_type = logic.get_photo_bytes("pod-test-album", "actual_existing_photo.jpg")
    checksum = hashlib.new("sha256", photo_bytes).hexdigest()
    
    assert "ca85488124e60afb8078dc44e9693b934f72c61c21be0714954da2c27409caad" == checksum

def test_get_pod_photo_bytes_existing(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    photo_bytes, mime_type = logic.get_pod_photo_bytes("pod-test-album", "2026-03-07")
    checksum = hashlib.new("sha256", photo_bytes).hexdigest()
    
    assert "ca85488124e60afb8078dc44e9693b934f72c61c21be0714954da2c27409caad" == checksum

def test_get_pod_photo_bytes_nonexisting(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    photo_bytes, mime_type = logic.get_pod_photo_bytes("pod-test-album", "0987-06-05")

    assert None == photo_bytes

def test_is_album_access_authenticated(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False 

    is_authenticated_true = logic.is_album_access_authenticated("pod-test-album", "super-duper-secret-token")
    is_authenticated_false_1 = logic.is_album_access_authenticated("album-not-existing", "super-duper-secret-token")
    is_authenticated_false_2 = logic.is_album_access_authenticated("pod-test-album", "")
    is_authenticated_false_3 = logic.is_album_access_authenticated("pod-test-album", "super-duper-secret-toke")
    is_authenticated_false_4 = logic.is_album_access_authenticated("pod-test-album", "superdupersecrettoken")

    assert True == is_authenticated_true
    assert False == is_authenticated_false_1
    assert False == is_authenticated_false_2
    assert False == is_authenticated_false_3
    assert False == is_authenticated_false_4
