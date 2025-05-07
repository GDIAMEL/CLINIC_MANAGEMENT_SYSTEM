# SAMUEL EMMANUEL KIMARO 
# WEEK_8_DATABASE_PLP

# QUESTION ONE
## Build a Complete Database Management System
**Objective**

Design and implement a full-featured database using only MySQL.

**What to do**

1. Choose a real-world use case (e.g., Library Management, Student Records, Clinic Booking System, Inventory Tracking, etc.)
2. Create a well-structured relational database using SQL.

**Use SQL to create the following**

1. Tables with proper constraints (PK, FK, NOT NULL, UNIQUE)
2. Relationships (1-1, 1-M, M-M where needed)

**Deliverables**

A single .sql file containing your:

1. CREATE TABLE statements
2. Sample  data

# Clinic Management System

A comprehensive database system for managing clinic operations including patients, doctors, services, appointments, and payments.

## Database Overview

The Clinic Management System database (`clinics_db`) is designed to efficiently handle the core operations of a medical clinic, including:

- Patient records management
- Doctor information and specialties
- Medical services offered
- Appointment scheduling and tracking
- Payment processing and records

## Database Schema

The database consists of 5 tables with the following relationships:

### Entity Relationship Diagram (ERD)

```
+-------------+       +----------------+       +-------------+
|  PATIENTS   |       |  APPOINTMENTS  |       |   DOCTORS   |
+-------------+       +----------------+       +-------------+
| patient_id  |<----->| appointment_id |<----->| doctor_id   |
| full_name   |  1:N  | patient_id     |  N:1  | full_name   |
| email       |       | doctor_id      |       | specialty   |
| phone       |       | service_id     |       | email       |
| gender      |       | appointment_date       +-------------+
| dob         |       | status         |
+-------------+       +-------^--------+
                              |
                              |  1:N
                              |
                      +-------v--------+       +-------------+
                      |    SERVICES    |       |   PAYMENTS  |
                      +----------------+       +-------------+
                      | service_id     |<----->| payment_id  |
                      | service_name   |  1:N  | appointment_id |
                      | description    |       | amount_paid |
                      | price          |       | payment_date|
                      +----------------+       +-------------+
```

**Relationship Details:**

1. **Patients to Appointments** (One-to-Many)
   - A patient can schedule multiple appointments
   - Each appointment belongs to exactly one patient
   - Foreign key: `appointments.patient_id` references `patients.patient_id`

2. **Doctors to Appointments** (One-to-Many)
   - A doctor can conduct multiple appointments
   - Each appointment is conducted by exactly one doctor
   - Foreign key: `appointments.doctor_id` references `doctors.doctor_id`

3. **Services to Appointments** (One-to-Many)
   - A service can be included in multiple appointments
   - Each appointment involves exactly one service
   - Foreign key: `appointments.service_id` references `services.service_id`

4. **Appointments to Payments** (One-to-Many)
   - An appointment can generate multiple payments (e.g., installments)
   - Each payment is associated with exactly one appointment
   - Foreign key: `payments.appointment_id` references `appointments.appointment_id`

All relationships implement CASCADE DELETE to maintain referential integrity when parent records are removed.

## Tables Description

### Patients
Stores information about clinic patients.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| patient_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for patients |
| full_name | VARCHAR(100) | NOT NULL | Patient's full name |
| email | VARCHAR(100) | NOT NULL, UNIQUE | Patient's email address |
| phone | VARCHAR(15) | NOT NULL | Patient's contact number |
| gender | ENUM | NOT NULL | Patient's gender (Male, Female, Other) |
| dob | DATE | | Patient's date of birth |

### Doctors
Contains details about medical practitioners working at the clinic.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| doctor_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for doctors |
| full_name | VARCHAR(100) | NOT NULL | Doctor's full name |
| specialty | VARCHAR(100) | NOT NULL | Doctor's medical specialty |
| email | VARCHAR(100) | NOT NULL, UNIQUE | Doctor's email address |

### Services
Lists all medical services provided by the clinic.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| service_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for services |
| service_name | VARCHAR(100) | NOT NULL, UNIQUE | Name of the service |
| description | TEXT | | Detailed description of the service |
| price | DECIMAL(10,2) | NOT NULL | Cost of the service |

### Appointments
Tracks scheduled appointments between patients and doctors.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| appointment_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for appointments |
| patient_id | INT | FOREIGN KEY, NOT NULL | Reference to patient |
| doctor_id | INT | FOREIGN KEY, NOT NULL | Reference to doctor |
| service_id | INT | FOREIGN KEY, NOT NULL | Reference to service |
| appointment_date | DATETIME | NOT NULL | Date and time of appointment |
| status | ENUM | DEFAULT 'Scheduled' | Status of appointment (Scheduled, Completed, Cancelled) |

### Payments
Records payment transactions for appointments.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| payment_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for payments |
| appointment_id | INT | FOREIGN KEY, NOT NULL | Reference to appointment |
| amount_paid | DECIMAL(10,2) | | Amount paid for the service |
| payment_date | DATETIME | DEFAULT CURRENT_TIMESTAMP | Date and time of payment |

## Relationships

- A patient can have multiple appointments
- A doctor can conduct multiple appointments
- A service can be included in multiple appointments
- An appointment can have multiple payments (e.g., partial payments)
- Each appointment is associated with exactly one patient, one doctor, and one service

## Sample Data

The database includes sample data for testing and demonstration purposes, including:
- 7 patients with diverse demographics
- 5 doctors with different specialties
- 5 medical services with varying costs
- 7 appointments scheduled for May 2025
- 7 corresponding payment records

## Usage Examples

### Finding all appointments for a specific patient

```sql
SELECT a.appointment_id, d.full_name AS doctor_name, s.service_name, 
       a.appointment_date, a.status
FROM appointments a
JOIN doctors d ON a.doctor_id = d.doctor_id
JOIN services s ON a.service_id = s.service_id
WHERE a.patient_id = 1;
```

### Getting payment records for a specific time period

```sql
SELECT p.payment_id, pt.full_name AS patient_name, s.service_name, 
       p.amount_paid, p.payment_date
FROM payments p
JOIN appointments a ON p.appointment_id = a.appointment_id
JOIN patients pt ON a.patient_id = pt.patient_id
JOIN services s ON a.service_id = s.service_id
WHERE p.payment_date BETWEEN '2025-05-01' AND '2025-05-31';
```

### Finding available slots for a specific doctor

```sql
SELECT doctor_id, full_name
FROM doctors
WHERE doctor_id NOT IN (
    SELECT doctor_id
    FROM appointments
    WHERE appointment_date BETWEEN '2025-05-17' AND '2025-05-17 23:59:59'
);
```

## Installation

1. Ensure you have MySQL installed on your system
2. Run the SQL script to create the database structure:
   ```
   mysql -u username -p < clinic_management_system.sql
   ```
3. Verify the installation by connecting to the database:
   ```
   mysql -u username -p clinics_db
   ```

## Future Enhancements

- Add staff table for non-medical personnel
- Implement medical records tracking
- Add inventory management for medical supplies
- Create user permissions system for different staff roles
- Implement automated billing and insurance processing
