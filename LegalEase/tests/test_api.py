from fastapi.testclient import TestClient

from backend.dependencies import get_generator
from backend.main import app


class FakeGenerator:
    model = "test-model"
    demo_mode = False

    def generate_document(self, document_type, parties, terms, dates):
        return (
            f"{document_type}\n\n"
            f"Parties: {parties}\n\n"
            f"Terms: {terms}\n\n"
            f"Effective: {dates}"
        )


def test_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "LegalEase API is running"


def test_generate():
    app.dependency_overrides[get_generator] = lambda: FakeGenerator()
    client = TestClient(app)

    response = client.post(
        "/generate",
        json={
            "document_type": "NDA",
            "parties": "Alice, Bob",
            "terms": "Keep information confidential; Return documents",
            "dates": "2026-04-15",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "test-model"
    assert "NDA" in data["content"]

    app.dependency_overrides.clear()


def test_validation_rejects_empty_document_type():
    client = TestClient(app)
    response = client.post(
        "/generate",
        json={
            "document_type": "",
            "parties": "Alice, Bob",
            "terms": "Confidentiality",
            "dates": "2026-04-15",
        },
    )
    assert response.status_code == 422
