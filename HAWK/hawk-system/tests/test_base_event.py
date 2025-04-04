import pytest
import requests
from unittest.mock import patch

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
                return MockResponse({"message": "denied"}, 200)
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


def test_access(mock_access):
    to_volan = requests.post(VOLAN_URL, json={"motion_detected": True, "status": "access"})
    assert to_volan.status_code == 200

    log_volan = to_volan.json()
    to_grif = requests.post(GRIF_URL, json={"source": "Волан", "message": log_volan["message"]})
    assert to_grif.status_code == 200

    to_kollektiv = requests.post(KOLLEKTIV_URL, json=to_grif.json())
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json() == {"status": "access"}

def test_denied(mock_denied):
    to_volan = requests.post(VOLAN_URL, json={"motion_detected": True, "status": "denied"})
    log_volan = to_volan.json()
    assert to_volan.status_code == 200

    to_sec = requests.post(SECURITY_URL, json=log_volan["message"])
    sec_log = to_sec.json()
    assert to_sec.status_code == 200

    to_grif = requests.post(GRIF_URL, json={"source": "Волан", "message": sec_log["status"]})
    assert to_grif.status_code == 200

    to_kollektiv = requests.post(KOLLEKTIV_URL, json=to_grif.json())
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json() == {"status": "Охрана решила проблему"}

def test_repair(mock_repair):
    to_volan = requests.post(VOLAN_URL, json={"motion_detected": True, "status": "repair"})
    log_volan = to_volan.json()
    assert to_volan.status_code == 200

    to_repair = requests.post(REPAIR_URL, json=log_volan["message"])
    repair_log = to_repair.json()
    assert to_repair.status_code == 200

    to_grif = requests.post(GRIF_URL, json={"source": "Волан", "message": repair_log["status"]})
    assert to_grif.status_code == 200

    to_kollektiv = requests.post(KOLLEKTIV_URL, json=to_grif.json())
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json() == {"status": "Ремонт готов"}