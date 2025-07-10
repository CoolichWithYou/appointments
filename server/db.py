from server.schema import AppointmentModel


async def doctor_appointments(conn, appointment: AppointmentModel) -> bool:
    overlap = await conn.fetchval(
        """
        SELECT s.id,
               s.doctor_id,
               s.patient_id,
               s.start_time,
               s.end_time
        FROM appointment s
        WHERE (s.doctor_id = $1)
          and (s.start_time <= $2)
          and (s.end_time >= $3)
        """,
        appointment.doctor_id,
        appointment.start_time,
        appointment.end_time,
    )

    if overlap:
        return True
    return False
