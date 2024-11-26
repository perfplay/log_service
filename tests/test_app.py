import pytest
from log_service.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_process_request(client):
    response = client.post(
        '/process_request',
        json={"device_id": "123", "user_id": "456", "error": "Some error"}
    )
    assert response.status_code == 200
    assert response.json["status"] == "success"