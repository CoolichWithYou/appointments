from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from server.main import app, get_session


def test_test_intersection():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)

        response = client.post("/patient", json={"name": "Ivan"})

        data = response.json()

        assert data["name"] == "Ivan"
        assert response.status_code == 200

        response = client.post("/doctor", json={"full_name": "Dmitry"})

        data = response.json()

        assert data["full_name"] == "Dmitry"
        assert response.status_code == 200

        response = client.post(
            "/appointment",
            json={
                "doctor_id": 1,
                "patient_id": 1,
                "start_time": datetime(2025, 1, 1, 10, 0).isoformat(),
                "end_time": datetime(2025, 1, 1, 11, 0).isoformat(),
            },
        )

        assert response.status_code == 200

        response = client.post(
            "/appointment",
            json={
                "doctor_id": 1,
                "patient_id": 1,
                "start_time": datetime(2025, 1, 1, 10, 30).isoformat(),
                "end_time": datetime(2025, 1, 1, 11, 30).isoformat(),
            },
        )

        assert response.status_code == 409

        app.dependency_overrides.clear()
