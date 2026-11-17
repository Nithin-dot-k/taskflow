from fastapi.testclient import TestClient
from main import app

# 1. Create a simulated client using our FastAPI app instance
client = TestClient(app)

def test_read_root():
    """Test that the root endpoint '/' returns status 200 and the welcome message."""
    # 2. Simulate an HTTP GET request to '/'
    response = client.get("/")

    # 3. Assert (verify) expectations:
    assert response.status_code == 200
    assert "message" in response.json()
    assert "TaskFlow" in response.json()["message"]