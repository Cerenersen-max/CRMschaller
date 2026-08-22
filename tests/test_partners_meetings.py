import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient

from app.database import init_db
from app.main import app
from app.services.email_templates import build_aston_martin_partnership_email

init_db()
client = TestClient(app)


def test_create_investor_with_contact_fields():
    # Not: isim, scripts/seed_partners.py'nin ekledigi gercek 'Aston Martin'
    # kaydiyla (paylasilan test DB'sinde) carpismasin diye kasitli farkli.
    payload = {
        "name": "Aston Martin (test contact)",
        "category": "Lifestyle collaboration",
        "contact_name": "Partner Contact",
        "contact_email": "partnerships@astonmartin.example",
    }
    response = client.post("/investors", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["contact_email"] == "partnerships@astonmartin.example"


def test_outreach_email_preview():
    create_response = client.post(
        "/investors",
        json={
            "name": "Preview Partner",
            "contact_name": "Jane Doe",
            "contact_email": "jane@example.com",
        },
    )
    investor_id = create_response.json()["id"]

    response = client.get(f"/investors/{investor_id}/outreach-email-preview")
    assert response.status_code == 200
    assert "jane@example.com" in response.json()["raw_email"]


def test_outreach_email_preview_requires_contact_email():
    create_response = client.post("/investors", json={"name": "No Contact Partner"})
    investor_id = create_response.json()["id"]

    response = client.get(f"/investors/{investor_id}/outreach-email-preview")
    assert response.status_code == 422


def test_build_aston_martin_partnership_email():
    message = build_aston_martin_partnership_email(
        to_name="Partner Contact", to_email="partnerships@astonmartin.example"
    )
    assert "partnerships@astonmartin.example" in message["To"]
    assert "MIME-Version" in message


def test_create_and_list_meeting():
    payload = {
        "title": "GUCA",
        "cadence": "weekly",
        "day_of_week": "Pazartesi",
        "time_of_day": "10:00",
        "agenda": "Veri tabani mimarisi + website design + AI website generator",
    }
    create_response = client.post("/meetings", json=payload)
    assert create_response.status_code == 201

    list_response = client.get("/meetings")
    assert list_response.status_code == 200
    titles = [m["title"] for m in list_response.json()]
    assert "GUCA" in titles
