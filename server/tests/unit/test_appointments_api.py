from datetime import datetime

import pytest
from fastapi import HTTPException

from server.main import postapp
from server.schema import AppointmentModel


@pytest.mark.asyncio
async def test_appointment_time_conflict(mocker) -> None:
    mock_conn = mocker.AsyncMock()
    mock_conn.fetchval.side_effect = [1]

    appointment = AppointmentModel(
        doctor_id=1,
        patient_id=1,
        start_time=datetime(2023, 1, 1, 10, 0),
        end_time=datetime(2023, 1, 1, 11, 0),
    )

    with pytest.raises(HTTPException) as exc_info:
        await postapp(appointment, mock_conn)

    assert exc_info.value.status_code == 409
