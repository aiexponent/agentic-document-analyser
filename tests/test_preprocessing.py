import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from preprocessing_service.processors import ImageProcessor
from preprocessing_service.main import app

client = TestClient(app)

# ---------------------------------------------------------------------------
# Unit Tests: ImageProcessor
# ---------------------------------------------------------------------------

def test_denoise_color_image(sample_noisy_image):
    processed = ImageProcessor.denoise_image(sample_noisy_image)
    assert processed is not None
    assert processed.shape == sample_noisy_image.shape
    assert processed.dtype == np.uint8

def test_denoise_grayscale_image():
    gray = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    processed = ImageProcessor.denoise_image(gray)
    assert processed is not None
    assert processed.shape == (100, 100)

def test_denoise_exception_handling():
    # Pass an invalid object to test graceful fallback
    invalid_input = "not_an_image"
    result = ImageProcessor.denoise_image(invalid_input)
    assert result == invalid_input

def test_deskew_image(sample_skewed_image):
    deskewed = ImageProcessor.deskew_image(sample_skewed_image)
    assert deskewed is not None
    assert deskewed.shape == sample_skewed_image.shape

def test_deskew_blank_image():
    blank = np.zeros((100, 100, 3), dtype=np.uint8)
    result = ImageProcessor.deskew_image(blank)
    assert result is not None
    assert result.shape == (100, 100, 3)

def test_correct_orientation(sample_rgb_image):
    result = ImageProcessor.correct_orientation(sample_rgb_image)
    assert np.array_equal(result, sample_rgb_image)

# ---------------------------------------------------------------------------
# API Tests: Preprocessing Service Endpoints
# ---------------------------------------------------------------------------

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "preprocessing"

def test_normalize_valid_image(sample_image_bytes):
    files = {"file": ("test.png", sample_image_bytes, "image/png")}
    response = client.post("/preprocess/normalize", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "original_dims" in data
    assert "processed_dims" in data
    assert "denoise" in data["steps_completed"]

def test_normalize_non_image_rejected():
    files = {"file": ("test.txt", b"plain text content", "text/plain")}
    response = client.post("/preprocess/normalize", files=files)
    assert response.status_code == 400
    assert "File must be an image" in response.json()["detail"]

def test_pdf_to_images_non_pdf_rejected(sample_image_bytes):
    files = {"file": ("test.png", sample_image_bytes, "image/png")}
    response = client.post("/preprocess/pdf_to_images", files=files)
    assert response.status_code == 400
    assert "File must be a PDF" in response.json()["detail"]

def test_pdf_to_images_mocked(monkeypatch):
    # Mock pdf2image.convert_from_bytes to avoid needing actual Poppler binary in test env
    dummy_pil_img = Image.new("RGB", (200, 300), color=(255, 255, 255))
    
    def mock_convert_from_bytes(contents):
        return [dummy_pil_img, dummy_pil_img]

    import pdf2image
    monkeypatch.setattr(pdf2image, "convert_from_bytes", mock_convert_from_bytes)

    files = {"file": ("report.pdf", b"%PDF-1.4 dummy pdf bytes", "application/pdf")}
    response = client.post("/preprocess/pdf_to_images", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total_pages"] == 2
    assert len(data["pages"]) == 2
    assert data["pages"][0]["page_number"] == 1
    assert data["pages"][0]["width"] == 200
    assert data["pages"][0]["height"] == 300
    assert "base64_image" in data["pages"][0]
