from datetime import datetime

import pytest
from httpx import ASGITransport, AsyncClient

from server.main import app


@pytest.mark.asyncio
async def test_test_intersection():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:

        response = await ac.post("/patient", json={"name": "Ivan"})

        patient = response.json()

        assert patient["name"] == "Ivan"
        assert response.status_code == 200

        response = await ac.post("/doctor", json={"full_name": "Dmitry"})

        doctor = response.json()

        assert doctor["full_name"] == "Dmitry"
        assert response.status_code == 200
        response = await ac.post(
            "/appointment",
            json={
                "doctor_id": doctor["id"],
                "patient_id": patient["id"],
                "start_time": datetime(2025, 1, 1, 10, 0).isoformat(),
                "end_time": datetime(2025, 1, 1, 11, 0).isoformat(),
            },
        )

        assert response.status_code == 200

        response = await ac.post(
            "/appointment",
            json={
                "doctor_id": 1,
                "patient_id": 1,
                "start_time": datetime(2025, 1, 1, 10, 30).isoformat(),
                "end_time": datetime(2025, 1, 1, 11, 30).isoformat(),
            },
        )

        assert response.status_code == 409
