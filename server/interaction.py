from sqlmodel import Field, Session, select

from server.schema import Appointment


async def doctor_appointments(session: Session, appointment: Appointment) -> bool:
    statement = (select(Appointment)
                 .where(Appointment.doctor_id == appointment.doctor_id)
                 .where(Appointment.start_time <= appointment.end_time)
                 .where(Appointment.end_time >= appointment.start_time)
                 )
    overlap = session.exec(statement).first()

    if overlap:
        return True
    return False
