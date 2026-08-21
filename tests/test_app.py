import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app

init_db()
client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_investor():
    payload = {"name": "Techstars", "category": "Accelerator", "stage": "due_diligence"}
    create_response = client.post("/investors", json=payload)
    assert create_response.status_code == 201

    list_response = client.get("/investors")
    assert list_response.status_code == 200
    names = [item["name"] for item in list_response.json()]
    assert "Techstars" in names


def test_create_inventory_item():
    payload = {"sku": "SKU-001", "name": "Test Urun", "classification": "SIA", "quantity": 10}
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    assert response.json()["sku"] == "SKU-001"


def test_daily_report_run():
    response = client.post("/reports/daily/run")
    assert response.status_code == 200
    assert "investors" in response.json()
