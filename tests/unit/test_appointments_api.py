from datetime import datetime

import pytest
from fastapi import HTTPException

from server.main import get_appointments
from server.schema import AppointmentModel


@pytest.mark.asyncio
async def test_appointment_time_conflict(mocker):
    """Тестирование обработки конфликта времени при создании записи"""
    mock_conn = mocker.AsyncMock()

    mock_conn.fetchval.return_value = 1

    appointment = AppointmentModel(
        doctor_id=1,
        patient_id=1,
        start_time=datetime(2023, 1, 1, 10, 0),
        end_time=datetime(2023, 1, 1, 11, 0),
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_appointments(appointment, mock_conn)

    assert exc_info.value.status_code == 409

    query = (
        "SELECT FROM appointment "
        "WHERE doctor_id = $1 AND start_time < $3 AND end_time > $2 "
        "LIMIT 1;"
    )

    mock_conn.fetchval.assert_called_once_with(
        query,
        1,
        appointment.start_time,
        appointment.end_time,
    )
