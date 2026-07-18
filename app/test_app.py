import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Application Mauve" in response.data
    assert b"Aicha" in response.data

def test_api(client):
    response = client.get('/api')
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Welcome to the API"}

def test_healthz(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_readyz(client):
    response = client.get('/readyz')
    assert response.status_code == 200
    assert response.json == {"status": "ready"}