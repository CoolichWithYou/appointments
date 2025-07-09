import pytest
from datetime import datetime
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
        end_time=datetime(2023, 1, 1, 11, 0)
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_appointments(appointment, mock_conn)

    assert exc_info.value.status_code == 409
    assert "У доктора уже есть встреча в это время" in str(exc_info.value.detail)

    mock_conn.fetchval.assert_called_once_with(
        "\n        SELECT 1\n        FROM appointment\n        WHERE doctor_id = $1\n          AND start_time < $3\n          AND end_time > $2\n        LIMIT 1;\n        ",
        1,
        appointment.start_time,
        appointment.end_time
    )