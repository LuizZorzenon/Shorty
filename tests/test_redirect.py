from fastapi.testclient import TestClient
from app.core.settings import settings


from app.main import app

client = TestClient(app)


def test_redirect_erro():
    response = client.get("/abc123")
    assert response.status_code == 404

    assert response.json() == {"detail": "URL not found"}
