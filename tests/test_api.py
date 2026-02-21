from fastapi.testclient import TestClient

from picture_of_the_day.api import api

client = TestClient(api)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
