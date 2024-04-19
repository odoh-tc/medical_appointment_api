# Medical Appointment API

## Introduction

The Medical Appointment API provides endpoints for managing patients, doctors, and appointments in a medical setting. It allows users to create, update, retrieve, and delete patient and doctor records, as well as schedule and manage appointments.

---

### Endpoints

#### Patients

- GET /patients/{patient_id}: Retrieve a patient by ID.
- POST /patients/: Create a new patient.
- PUT /patients/{patient_id}: Update an existing patient.
- DELETE /patients/{patient_id}: Delete a patient by ID.

---

#### Doctors

- GET /doctors/{doctor_id}: Retrieve a doctor by ID.
- POST /doctors/: Create a new doctor.
- PUT /doctors/{doctor_id}: Update an existing doctor.
- DELETE /doctors/{doctor_id}: Delete a doctor by ID.
- PUT /doctors/{doctor_id}/availability: Set a doctor's availability status.

---

#### Appointments

- POST /appointments/: Create a new appointment. Assigns the first available doctor to the appointment.
- PUT /appointments/{appointment_id}/complete: Complete an appointment. Marks the doctor as available again.
- DELETE /appointments/{appointment_id}: Cancel an appointment before it is completed, making the doctor available again.

---

### Data Models

#### Patient

- **username**: Username of the patient.
- **first_name**: First name of the patient.
- **last_name**: Last name of the patient.
- **age**: Age of the patient.
- **sex**: Gender of the patient.
- **weight**: Weight of the patient.
- **height**: Height of the patient.
- **phone_number**: Phone number of the patient.

---

#### Doctor

- **username**: Username of the doctor.
- **specialization**: Medical specialization of the doctor.
- **phone**: Phone number of the doctor.
- **is_available**: Availability status of the doctor.

---

#### Appointment

- **patient**: Patient associated with the appointment.
- **doctor**: Doctor assigned to the appointment.
- **date**: Date and time of the appointment.
- **is_completed**: Completion status of the appointment.
