from datetime import datetime

import pytest
from async_asgi_testclient import TestClient

from server.main import app


@pytest.mark.asyncio
async def test_create_appointment() -> None:
    async with TestClient(app) as client:
        appointment_data = {
            "doctor_id": 1,
            "patient_id": 2,
            "start_time": datetime(2023, 1, 1, 10, 0).isoformat(),
            "end_time": datetime(2023, 1, 1, 11, 0).isoformat(),
        }

        response = await client.post("/appointments", json=appointment_data)

        assert response.status_code == 200
