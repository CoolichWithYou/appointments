from datetime import datetime

import pytest
from async_asgi_testclient import TestClient
from server.main import app


@pytest.mark.asyncio
async def test_appointment_creation_flow() -> None:
    """Тестирование полного цикла создания записи через API"""

    async with TestClient(app) as client:
        pool = app.state.pool
        async with pool.acquire() as conn:
            await conn.execute("DELETE FROM appointment")

        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

        start_time = datetime(2023, 1, 1, 10, 0).isoformat()
        end_time = datetime(2023, 1, 1, 11, 0).isoformat()

        appointment_data = {
            "doctor_id": 1,
            "patient_id": 2,
            "start_time": start_time,
            "end_time": end_time,
        }

        response = await client.post("/appointments", json=appointment_data)
        assert response.status_code == 200, response.text
        response_data = response.json()

        created_id = response_data["id"]

        assert response_data["doctor_id"] == appointment_data["doctor_id"]
        assert response_data["patient_id"] == appointment_data["patient_id"]
        assert response_data["start_time"] == start_time
        assert response_data["end_time"] == end_time

        response = await client.get(f"/appointments/{created_id}")
        assert response.status_code == 200
        appointment = response.json()

        assert appointment["id"] == created_id
        assert appointment["doctor_id"] == appointment_data["doctor_id"]
        assert appointment["patient_id"] == appointment_data["patient_id"]
        assert appointment["start_time"] == start_time
        assert appointment["end_time"] == end_time

        invalid_data = appointment_data.copy()
        invalid_data["end_time"] = datetime(2023, 1, 1, 9, 0).isoformat()
        response = await client.post("/appointments", json=invalid_data)
        assert response.status_code == 400
        assert "должно быть после" in response.json()["detail"]

        conflict_data = appointment_data.copy()
        conflict_data["start_time"] = datetime(2023, 1, 1, 10, 30).isoformat()
        conflict_data["end_time"] = datetime(2023, 1, 1, 11, 30).isoformat()
        response = await client.post("/appointments", json=conflict_data)
        assert response.status_code == 409

        response = await client.get("/appointments/999")
        assert response.status_code == 404
        assert "не найдено" in response.json()["detail"]
