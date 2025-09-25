import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_run_scan():
    file_content = b"print('Hello World')\nprint('Test')"
    file = io.BytesIO(file_content)
    file.name = "test_file.py"

    response = client.post(
        "/scan/run",
        files={"file": (file.name, file, "text/plain")}
    )
    assert response.status_code == 200
    assert "results" in response.json()


def test_scan_history():
    response = client.get("/scan/history")
    assert response.status_code == 200
    assert "results" in response.json()
