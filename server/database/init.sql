create table appointment (
    id          serial primary key,
    doctor_id   int not null,
    patient_id  int not null,
    start_time  timestamp not null,
    end_time    timestamp not null,

    CONSTRAINT unique_doctor_time UNIQUE (doctor_id, start_time)
);