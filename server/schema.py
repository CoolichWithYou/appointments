from datetime import datetime

from pydantic import BaseModel

class AppointmentModel(BaseModel):
    doctor_id: int
    patient_id: int
    start_time: datetime
    end_time: datetime