import pytest
import requests
from unittest.mock import patch

VOLAN_URL = "http://localhost:8000/motion"
GRIF_URL = "http://localhost:8001/process"
KOLLEKTIV_URL = "http://localhost:8002/log"

@pytest.fixture
def mock_requests():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "access"}
        yield mock_post  

def test_access(mock_requests):
    to_volan = requests.post(VOLAN_URL, json={"motion_detected": True, "status": "access"})
    assert to_volan.status_code == 200

    log_volan = to_volan.json()
    to_grif = requests.post(GRIF_URL, json={"source": "Волан", "message": log_volan["status"]})
    assert to_grif.status_code == 200

    to_kollektiv = requests.post(KOLLEKTIV_URL, json=to_grif.json())
    assert to_kollektiv.status_code == 200
    assert to_kollektiv.json() == {"status": "access"}
