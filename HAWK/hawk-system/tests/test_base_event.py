import pytest
from unittest.mock import patch
from volan.main import app as app_v
from repair.main import app as app_r
from security.main import app as app_s
from grif.main import app as app_g
from kollektiv.main import app as app_k

VOLAN_URL = "http://localhost:8000/motion"
GRIF_URL = "http://localhost:8001/process"
KOLLEKTIV_URL = "http://localhost:8002/log"
REPAIR_URL = "http://localhost:8003/fix"
SECURITY_URL = "http://localhost:8004/check"

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@pytest.fixture
def volan_client():
    return app_v.test_client()

@pytest.fixture
def grif_client():
    return app_g.test_client()

@pytest.fixture
def kollektiv_client():
    return app_k.test_client()

@pytest.fixture
def repair_client():
    return app_r.test_client()

@pytest.fixture
def security_client():
    return app_s.test_client()

@pytest.fixture
def mock_access():
    with patch("requests.post") as mock_post:
        def side_effect(url, json):
            if url == VOLAN_URL:
                return MockResponse({"message": "access"}, 200)
            elif url == GRIF_URL:
                return MockResponse({"source": "Волан", "message": "access"}, 200)
            elif url == KOLLEKTIV_URL:
                return MockResponse({"status": "access"}, 200)
            return MockResponse({}, 404)
        mock_post.side_effect = side_effect
        yield mock_post

@pytest.fixture
def mock_denied():
    with patch("requests.post") as mock_post:
        def side_effect(url, json):
            if url == VOLAN_URL:
                return MockResponse({"message": "Охрана решила проблему"}, 200)
            elif url == SECURITY_URL:
                return MockResponse({"status": "Охрана решила проблему"}, 200)
            elif url == GRIF_URL:
                return MockResponse({"source": "Волан", "message": "Охрана решила проблему"}, 200)
            elif url == KOLLEKTIV_URL:
                return MockResponse({"status": "Охрана решила проблему"}, 200)
            return MockResponse({}, 404)
        mock_post.side_effect = side_effect
        yield mock_post

@pytest.fixture
def mock_repair():
    with patch("requests.post") as mock_post:
        def side_effect(url, json):
            if url == VOLAN_URL:
                return MockResponse({"message": "repair"}, 200)
            elif url == REPAIR_URL:
                return MockResponse({"status": "Ремонт готов"}, 200)
            elif url == GRIF_URL:
                return MockResponse({"source": "Волан", "message": "Ремонт готов"}, 200)
            elif url == KOLLEKTIV_URL:
                return MockResponse({"status": "Ремонт готов"}, 200)
            return MockResponse({}, 404)
        mock_post.side_effect = side_effect
        yield mock_post

def test_access(mock_access, volan_client, grif_client, kollektiv_client):
    to_volan = volan_client.post(VOLAN_URL, json={"motion_detected": True, "status": "access"})
    to_grif = grif_client.post(GRIF_URL, json={"source": "Волан", "message": "access"})
    to_kollektiv = kollektiv_client.post(KOLLEKTIV_URL, json=to_grif.json)

    assert to_volan.status_code == 200
    assert to_grif.status_code == 200
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json == {"status": "access"}

def test_denied(mock_denied, volan_client, security_client, grif_client, kollektiv_client):
    to_volan = volan_client.post(VOLAN_URL, json={"motion_detected": True, "status": "denied"})
    to_sec = security_client.post(SECURITY_URL, json="denied")
    to_grif = grif_client.post(GRIF_URL, json={"source": "Волан", "message": "Охрана решила проблему"})
    to_kollektiv = kollektiv_client.post(KOLLEKTIV_URL, json=to_grif.json)

    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json == {"status": "Охрана решила проблему"}

def test_repair(mock_repair, volan_client, repair_client, grif_client, kollektiv_client):
    to_volan = volan_client.post(VOLAN_URL, json={"motion_detected": True, "status": "repair"})
    to_rep = repair_client.post(REPAIR_URL, json={"message": "repair"})
    to_grif = grif_client.post(GRIF_URL, json={"source": "Волан", "message": "Ремонт готов"})
    to_kollektiv = kollektiv_client.post(KOLLEKTIV_URL, json=to_grif.json)

    assert to_rep.status_code == 200
    assert to_grif.status_code == 200
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json == {"status": "Ремонт готов"}
