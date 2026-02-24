import pytest
import os

from fastapi.testclient import TestClient

from picture_of_the_day.api import api

client = TestClient(api)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_is_admin_initialized_false():
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
