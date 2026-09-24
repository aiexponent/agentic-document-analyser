import io
import json
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from visual_service.main import app, client as fireworks_client

client = TestClient(app)

# ---------------------------------------------------------------------------
# API Tests: Visual Intelligence Service Endpoints
# ---------------------------------------------------------------------------

def test_visual_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "visual_service"
    assert "model" in data

def test_detect_layout_valid(monkeypatch, sample_image_bytes, mock_vlm_json_response):
    async def mock_analyze_image(prompt="", base64_image=None):
        return mock_vlm_json_response

    monkeypatch.setattr(fireworks_client, "analyze_image", mock_analyze_image)

    files = {"file": ("architecture_diagram.png", sample_image_bytes, "image/png")}
    response = client.post("/detect/layout", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "detections" in data
    detections = data["detections"]
    assert len(detections) == 4

    # Verify first detection (title)
    d0 = detections[0]
    assert d0["label"] == "title"
    assert d0["confidence"] == 1.0
    assert "EU AI Act" in d0["attributes"]["text"]
    assert "bbox" in d0
    assert d0["bbox"]["x1"] >= 0
    assert d0["bbox"]["y1"] >= 0

def test_detect_layout_markdown_wrapped_json(monkeypatch, sample_image_bytes, mock_vlm_markdown_response):
    async def mock_analyze_image(prompt="", base64_image=None):
        return mock_vlm_markdown_response

    monkeypatch.setattr(fireworks_client, "analyze_image", mock_analyze_image)

    files = {"file": ("annex_iv.png", sample_image_bytes, "image/png")}
    response = client.post("/detect/layout", files=files)
    assert response.status_code == 200
    data = response.json()
    detections = data.get("detections", [])
    assert len(detections) == 2
    assert detections[0]["label"] == "header"
    assert "Annex IV" in detections[0]["attributes"]["text"]

def test_detect_layout_invalid_image():
    files = {"file": ("corrupt.png", b"not-a-valid-image-bytes", "image/png")}
    response = client.post("/detect/layout", files=files)
    assert response.status_code == 400
    assert "Invalid image file" in response.json()["detail"]

def test_detect_layout_vlm_failure(monkeypatch, sample_image_bytes):
    async def mock_analyze_image(prompt="", base64_image=None):
        raise RuntimeError("Fireworks AI connection timeout")

    monkeypatch.setattr(fireworks_client, "analyze_image", mock_analyze_image)

    files = {"file": ("diagram.png", sample_image_bytes, "image/png")}
    response = client.post("/detect/layout", files=files)
    assert response.status_code == 503
    assert "Visual Intelligence Service Failed" in response.json()["detail"]

def test_coordinate_denormalization(monkeypatch):
    # Test specific coordinate scaling: image 1000 x 500
    img = Image.new("RGB", (1000, 500), color=(100, 100, 100))
    b = io.BytesIO()
    img.save(b, format="PNG")
    img_bytes = b.getvalue()

    custom_vlm_response = json.dumps([
        {"type": "title", "bbox": [100, 200, 500, 400], "text": "Normalized Title"}
    ])

    async def mock_analyze_image(prompt="", base64_image=None):
        return custom_vlm_response

    monkeypatch.setattr(fireworks_client, "analyze_image", mock_analyze_image)

    files = {"file": ("custom.png", img_bytes, "image/png")}
    response = client.post("/detect/layout", files=files)
    assert response.status_code == 200
    det = response.json()["detections"][0]

    # [100, 200, 500, 400] on (1000 width, 500 height)
    # x1 = (100/1000) * 1000 = 100
    # y1 = (200/1000) * 500  = 100
    # x2 = (500/1000) * 1000 = 500
    # y2 = (400/1000) * 500  = 200
    assert det["bbox"]["x1"] == pytest.approx(100.0)
    assert det["bbox"]["y1"] == pytest.approx(100.0)
    assert det["bbox"]["x2"] == pytest.approx(500.0)
    assert det["bbox"]["y2"] == pytest.approx(200.0)
