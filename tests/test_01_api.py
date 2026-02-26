import pytest
import os
import hashlib

from fastapi.testclient import TestClient

from picture_of_the_day.api import api
import picture_of_the_day.logic as logic
import picture_of_the_day.nc_handler as nc_handler
import picture_of_the_day.config as config

client = TestClient(api)

def test_api_running():
    response = client.get("/")
    assert response.status_code == 200

def test_api_is_admin_initialized_false(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "empty"))
    monkeypatch.delenv("POD_NC_URL", raising=False)
    monkeypatch.delenv("POD_NC_USERNAME", raising=False)
    monkeypatch.delenv("POD_NC_ACCESSTOKEN", raising=False)

    response = client.get("/api/admin/initialized")
    assert response.status_code == 200
    data = response.json()
    assert "initialized" in response.json()
    assert data["initialized"] == False

def test_api_is_admin_initialized_true(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))

    response = client.get("/api/admin/initialized")
    assert response.status_code == 200
    data = response.json()
    assert "initialized" in response.json()
    assert data["initialized"] == True

def test_api_get_pod_photo_bytes(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    response = client.get("/api/album/pod-test-album/super-duper-secret-token/photo/2026-03-07")
    assert response.status_code == 200

    checksum = hashlib.new("sha256", response.content).hexdigest()
    
    # without overlay: ca85488124e60afb8078dc44e9693b934f72c61c21be0714954da2c27409caad
    
    assert "017074049ec4b32c5257fe959b4b3c9bea585b8530ecd701188ecee48cbf938d" == checksum

def test_api_endpoint_calls_unauthenticated(monkeypatch):
    monkeypatch.chdir(os.path.join("tests", "configs", "is_admin_initialized_true"))
    config.load_core_config(ignore_env=True)
    config.autosave_configs = False

    response = client.get("/api/album/pod-test-album/totally-wrong-secrect/photo/2026-03-07")
    assert response.status_code == 401
