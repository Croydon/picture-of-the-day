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
