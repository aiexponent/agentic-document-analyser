import pytest
from common.schemas import (
    BoundingBox,
    Dimension,
    TextAnchor,
    Entity,
    VisualElement,
    TableCell,
    TableRow,
    Table,
    Block,
    Page,
    DocumentContent,
    AnalysisResponse,
)
from common.utils import get_centroid_y, spatial_sort
from common.config import settings, Environment, LogLevel

def test_bounding_box_instantiation():
    bbox = BoundingBox(x1=10.0, y1=20.0, x2=100.0, y2=150.0)
    assert bbox.x1 == 10.0
    assert bbox.y1 == 20.0
    assert bbox.x2 == 100.0
    assert bbox.y2 == 150.0

def test_dimension_defaults():
    dim = Dimension(width=1920, height=1080)
    assert dim.width == 1920
    assert dim.height == 1080
    assert dim.unit == "pixel"

def test_block_and_page_schemas():
    bbox = BoundingBox(x1=0, y1=0, x2=100, y2=50)
    block = Block(block_type="title", text="Article 9 Overview", bounding_box=bbox)
    dim = Dimension(width=1000, height=1400)
    page = Page(page_number=1, dimension=dim, blocks=[block], base64_image="data:image/png;base64,abc123")
    
    assert page.page_number == 1
    assert len(page.blocks) == 1
    assert page.blocks[0].block_type == "title"
    assert page.base64_image.startswith("data:image/png;base64")

def test_analysis_response_schema():
    dim = Dimension(width=800, height=600)
    page = Page(page_number=1, dimension=dim, blocks=[])
    doc = DocumentContent(
        text="Full extracted document text.",
        pages=[page],
        entities=[],
        visual_elements=[],
        tables=[],
    )
    resp = AnalysisResponse(
        job_id="test-job-uuid-1234",
        status="completed",
        timestamp="1700000000.0",
        document=doc,
    )
    assert resp.job_id == "test-job-uuid-1234"
    assert resp.status == "completed"
    assert resp.document.text == "Full extracted document text."
    assert len(resp.document.pages) == 1

def test_get_centroid_y():
    bbox = {"x1": 50.0, "y1": 100.0, "x2": 250.0, "y2": 200.0}
    centroid = get_centroid_y(bbox)
    assert centroid == 150.0

def test_spatial_sort_reading_order():
    # 3 detections:
    # d1: row 1, col 2 (y1=10, x1=200)
    # d2: row 1, col 1 (y1=12, x1=50) -> should be first after sort
    # d3: row 2, col 1 (y1=100, x1=50) -> should be third
    d1 = {"bbox": {"x1": 200, "y1": 10, "x2": 400, "y2": 30}, "label": "header_right"}
    d2 = {"bbox": {"x1": 50, "y1": 12, "x2": 150, "y2": 30}, "label": "header_left"}
    d3 = {"bbox": {"x1": 50, "y1": 100, "x2": 300, "y2": 140}, "label": "body_text"}

    sorted_detections = spatial_sort([d1, d2, d3], y_tolerance=20)
    assert sorted_detections[0]["label"] == "header_left"
    assert sorted_detections[1]["label"] == "header_right"
    assert sorted_detections[2]["label"] == "body_text"

def test_spatial_sort_empty():
    assert spatial_sort([]) == []

def test_config_settings():
    assert settings.ENV in (Environment.DEV, Environment.PROD, "dev", "prod")
    assert settings.PREPROCESSING_PORT == 8001
    assert settings.VISUAL_PORT == 8002
