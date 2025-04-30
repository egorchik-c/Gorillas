import pytest
import requests
from unittest.mock import patch
from volan.main import app as app_v
from grif.main import app as app_g
from kollektiv.main import app as app_k
from vetrolov.main import app as app_vetr
from diagnostic.main import app as app_d

VOLAN_URL = "http://localhost:8000/motion"
GRIF_URL = "http://localhost:8001/process"
KOLLEKTIV_URL = "http://localhost:8002/log"
VETROLOV_URL = "http://vetrolov:8005/energy"
DIAG_URL = "http://diagnostic:8006/confirm"

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
def vetrolov_client():
    return app_vetr.test_client()

@pytest.fixture
def diagnostic_client():
    return app_d.test_client()

@pytest.fixture
def mock_reboot():
    with patch("requests.post") as mock_post:
        def side_effect(url, json):
            if url == GRIF_URL:
                return MockResponse({"message": "reboot"}, 200)
            elif url == KOLLEKTIV_URL:
                return MockResponse({"status": "reboot"}, 200)
            return MockResponse({}, 404)

        mock_post.side_effect = side_effect
        yield mock_post

@pytest.fixture
def mock_power_off():
    with patch("requests.post") as mock_post:
        def side_effect(url, json):
            if url == VETROLOV_URL:
                return MockResponse({"status": "Diagnostic OK"}, 200)
            elif url == DIAG_URL:
                return MockResponse({"status": "Diagnostic OK"}, 200)
            elif url == GRIF_URL:
                return MockResponse({"source": "Диагностика", "message": "Отключение питания Ветролова"}, 200)
            elif url == KOLLEKTIV_URL:
                return MockResponse({"status": "Отключение питания Ветролова"}, 200)
            return MockResponse({}, 404)

        mock_post.side_effect = side_effect
        yield mock_post

def test_reboot(mock_reboot, grif_client, kollektiv_client):
    to_grif = grif_client.post(GRIF_URL, json={"message": "reboot"})
    to_kollektiv = kollektiv_client.post(KOLLEKTIV_URL, json={"message": "reboot"})

    assert to_grif.status_code == 200
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json == {"status": "reboot"}

def test_power_off(mock_power_off, vetrolov_client, diagnostic_client, grif_client, kollektiv_client):
    to_vetrolov = vetrolov_client.post(VETROLOV_URL, json={"message": "power_off"})
    to_diagnostic = diagnostic_client.post(DIAG_URL, json={"message": "power_off"})
    to_grif = grif_client.post(GRIF_URL, json={"source": "Диагностика", "message": "Отключение питания Ветролова"})
    to_kollektiv = kollektiv_client.post(KOLLEKTIV_URL, json={"source": "Диагностика", "message": "Отключение питания Ветролова"})
    
    assert to_vetrolov.status_code == 200
    assert to_diagnostic.status_code == 200
    assert to_grif.status_code == 200
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json == {"status": "Отключение питания Ветролова"}
