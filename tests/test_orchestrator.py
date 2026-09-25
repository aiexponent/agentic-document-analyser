import base64
import pytest
from fastapi.testclient import TestClient

from orchestrator.main import app

client = TestClient(app)

# ---------------------------------------------------------------------------
# API Tests: Orchestrator Service Endpoints
# ---------------------------------------------------------------------------

def test_orchestrator_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "orchestrator"

@pytest.mark.asyncio
async def test_analyze_single_image(monkeypatch, sample_image_bytes):
    # Mock call_service and httpx calls in orchestrator
    mock_pp_data = {
        "status": "success",
        "original_dims": {"width": 200, "height": 200},
        "processed_dims": {"width": 200, "height": 200},
    }

    mock_vis_data = {
        "detections": [
            {
                "label": "title",
                "confidence": 1.0,
                "bbox": {"x1": 10.0, "y1": 10.0, "x2": 190.0, "y2": 50.0},
                "attributes": {"text": "Architecture Overview"},
            },
            {
                "label": "text",
                "confidence": 0.95,
                "bbox": {"x1": 10.0, "y1": 60.0, "x2": 190.0, "y2": 180.0},
                "attributes": {"text": "Risk controls mapped to Article 9."},
            },
        ]
    }

    async def mock_call_service(client, url, file_path, filename, content_type):
        if "normalize" in url:
            return mock_pp_data
        return None

    class MockResponse:
        def __init__(self, data, status_code=200):
            self._data = data
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP error {self.status_code}")

        def json(self):
            return self._data

    async def mock_post(self, url, *args, **kwargs):
        if "detect/layout" in url:
            return MockResponse(mock_vis_data)
        return MockResponse({}, status_code=404)

    import orchestrator.main
    monkeypatch.setattr(orchestrator.main, "call_service", mock_call_service)
    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)

    files = {"file": ("architecture.png", sample_image_bytes, "image/png")}
    response = client.post("/analyze", files=files)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "completed"
    assert "job_id" in data
    doc = data["document"]
    assert len(doc["pages"]) == 1
    assert doc["pages"][0]["page_number"] == 1
    assert len(doc["pages"][0]["blocks"]) == 2
    assert "Architecture Overview" in doc["text"]
    assert "Article 9" in doc["text"]
    assert len(doc["visual_elements"]) == 2

@pytest.mark.asyncio
async def test_analyze_multipage_pdf(monkeypatch, sample_image_bytes):
    b64_img = base64.b64encode(sample_image_bytes).decode("utf-8")
    mock_pdf_pages = {
        "total_pages": 2,
        "pages": [
            {"page_number": 1, "base64_image": b64_img, "width": 800, "height": 1000},
            {"page_number": 2, "base64_image": b64_img, "width": 800, "height": 1000},
        ],
    }

    mock_vis_page1 = {
        "detections": [
            {
                "label": "title",
                "confidence": 1.0,
                "bbox": {"x1": 50.0, "y1": 50.0, "x2": 750.0, "y2": 150.0},
                "attributes": {"text": "Page 1: Executive Summary"},
            }
        ]
    }

    mock_vis_page2 = {
        "detections": [
            {
                "label": "table",
                "confidence": 0.99,
                "bbox": {"x1": 50.0, "y1": 200.0, "x2": 750.0, "y2": 800.0},
                "attributes": {"text": "Page 2: Risk Ledger"},
            }
        ]
    }

    async def mock_call_service(client, url, file_path, filename, content_type):
        if "pdf_to_images" in url:
            return mock_pdf_pages
        return None

    class MockResponse:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    call_count = 0

    async def mock_post(self, url, *args, **kwargs):
        nonlocal call_count
        call_count += 1
        # Alternate response for pages
        if call_count % 2 == 1:
            return MockResponse(mock_vis_page1)
        return MockResponse(mock_vis_page2)

    import orchestrator.main
    monkeypatch.setattr(orchestrator.main, "call_service", mock_call_service)
    monkeypatch.setattr("httpx.AsyncClient.post", mock_post)

    files = {"file": ("compliance_dossier.pdf", b"%PDF-1.4 dummy content", "application/pdf")}
    response = client.post("/analyze", files=files)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "completed"
    doc = data["document"]
    assert len(doc["pages"]) == 2
    assert doc["pages"][0]["page_number"] == 1
    assert doc["pages"][1]["page_number"] == 2
    # Check page break separator
    assert "--- PAGE BREAK ---" in doc["text"]

def test_analyze_preprocessing_failure(monkeypatch, sample_image_bytes):
    async def mock_failed_call(*args, **kwargs):
        return None

    import orchestrator.main
    monkeypatch.setattr(orchestrator.main, "call_service", mock_failed_call)

    files = {"file": ("error.png", sample_image_bytes, "image/png")}
    response = client.post("/analyze", files=files)
    assert response.status_code == 500
