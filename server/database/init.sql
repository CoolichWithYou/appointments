create table doctor (
    id          serial primary key,
    full_name   varchar(100) not null,
    created_at  timestamp default now()
);

create table patient (
    id     serial primary key,
    name   varchar(40) not null,
    email  varchar(100) unique
);

create table appointment (
    id          serial primary key,
    doctor_id   int not null,
    patient_id  int not null,
    start_time  timestamp not null,
    end_time    timestamp not null,

    CONSTRAINT unique_doctor_time UNIQUE (doctor_id, start_time),

    CONSTRAINT fk_doctor
        FOREIGN KEY (doctor_id)
        REFERENCES doctor(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_patient
        FOREIGN KEY (patient_id)
        REFERENCES patient(id)
        ON DELETE CASCADE
);