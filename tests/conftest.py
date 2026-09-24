import os
import sys
import cv2
import numpy as np
import pytest

# Ensure repository root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Set test environment variables
os.environ["ENV"] = "dev"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["FIREWORKS_API_KEY"] = "fake_test_key_for_unit_tests"
os.environ["FIREWORKS_MODEL"] = "accounts/fireworks/models/qwen2p5-vl-72b-instruct"
os.environ["PREPROCESSING_HOST"] = "127.0.0.1"
os.environ["PREPROCESSING_PORT"] = "8001"
os.environ["VISUAL_HOST"] = "127.0.0.1"
os.environ["VISUAL_PORT"] = "8002"

@pytest.fixture
def sample_rgb_image() -> np.ndarray:
    """Generate a clean synthetic 200x200 RGB image with white text on dark background."""
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.rectangle(img, (20, 20), (180, 180), (40, 40, 40), -1)
    cv2.putText(img, "DOC INTEL", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return img

@pytest.fixture
def sample_image_bytes(sample_rgb_image) -> bytes:
    """Encode the synthetic image to PNG bytes."""
    _, encoded = cv2.imencode(".png", sample_rgb_image)
    return encoded.tobytes()

@pytest.fixture
def sample_noisy_image(sample_rgb_image) -> np.ndarray:
    """Add Gaussian/uniform noise to the synthetic image."""
    noise = np.random.randint(0, 40, sample_rgb_image.shape, dtype=np.uint8)
    return cv2.add(sample_rgb_image, noise)

@pytest.fixture
def sample_skewed_image() -> np.ndarray:
    """Create an image with a rotated high-contrast contour for deskew testing."""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    rect = ((150, 150), (120, 60), 25.0)  # center, size, angle
    box = cv2.boxPoints(rect)
    box = np.int64(box)
    cv2.drawContours(img, [box], 0, (255, 255, 255), -1)
    return img

@pytest.fixture
def mock_vlm_json_response() -> str:
    """Sample raw string mimicking a valid Fireworks AI JSON response."""
    return """[
      {"type": "title", "bbox": [50, 20, 950, 80], "text": "EU AI Act Article 9 Risk Assessment"},
      {"type": "diagram", "bbox": [100, 120, 900, 500], "text": "Model Training -> Safety Gate -> Production Pipeline"},
      {"type": "table", "bbox": [100, 550, 900, 800], "text": "Metric | Threshold | Observed"},
      {"type": "text", "bbox": [100, 820, 900, 900], "text": "Compliance evidence successfully verified."}
    ]"""

@pytest.fixture
def mock_vlm_markdown_response() -> str:
    """Sample raw string mimicking a Fireworks response wrapped in markdown code fences."""
    return """```json
    [
      {"type": "header", "bbox": [50, 10, 500, 60], "text": "Annex IV Technical Specification"},
      {"type": "text", "bbox": [50, 100, 800, 300], "text": "System architecture conforms to standards."}
    ]
    ```"""
