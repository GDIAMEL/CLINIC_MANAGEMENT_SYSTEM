CREATE DATABASE IF NOT EXISTS clinics_db;
USE clinics_db;

-- Patients Table
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    dob DATE
);

-- Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Services Table
CREATE TABLE IF NOT EXISTS services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

-- Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    service_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE
);

-- Payments Table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    amount_paid DECIMAL(10, 2),
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE
);

-- Sample Data
INSERT INTO patients (full_name, email, phone, gender, dob)
VALUES 
('Fredrick Kaviti', 'FredKaviti@gmail.com', '0700254254', 'Male', '2002-05-10'),
('Ashton Humphreys', 'Humphreys@gmail.com', '0701254254', 'Male', '2002-06-10'),
('Enock Tarei', 'Tarei@gmail.com', '0702254254', 'Male', '2002-07-10'),
('Sammy Kathuki', 'Kathuki@gmail.com', '0703254254', 'Male', '2002-08-10'),
('Erick Pyatich', 'Pyatich@gmail.com', '0704254254', 'Male', '2000-06-02'),
('Vanessa Mdee', 'Mdee@gmail.com', '0705254254', 'Female', '2001-10-10'),
('Maclaren Alexandria', 'Maclaren@gmail.com', '0706254254', 'Male', '2009-02-02');

INSERT INTO doctors (full_name, specialty, email)
VALUES 
('Dr. Alice Kimani', 'Dermatologist', 'aliceKimani@clinic.com'),
('Dr. Ernest Ngao', 'Anesthesiologist', 'Ngao21@clinic.com'),
('Dr. Caroline Wango', 'Psychiatrist', 'Wango01@clinic.com'),
('Dr. Deborah Manjuki', 'Cardiologist', 'DeborahManjuki@clinic.com'),
('Dr. Salome Manjuki', 'Critical Care Medicine Specialist', 'SalomeManjuki@clinic.com');

INSERT INTO services (service_name, description, price)
VALUES 
('General Consultation', 'Basic medical consultation and diagnosis', 1500.00),
('Dental Checkup', 'Routine dental examination including cleaning', 3000.00),
('Blood Test Panel', 'Comprehensive blood tests for health monitoring', 2500.00),
('Ultrasound Scan', 'Imaging service for internal body structures', 5000.00),
('Vaccination Service', 'Administration of preventive vaccines', 2000.00);

INSERT INTO appointments (patient_id, doctor_id, service_id, appointment_date)
VALUES 
(1, 1, 1, '2025-05-10 10:00:00'),
(2, 2, 2, '2025-05-11 11:00:00'),
(3, 3, 3, '2025-05-12 09:00:00'),
(4, 4, 4, '2025-05-13 14:30:00'),
(5, 5, 5, '2025-05-14 08:00:00'),
(6, 1, 3, '2025-05-15 12:00:00'),
(7, 2, 1, '2025-05-16 16:00:00');

INSERT INTO payments (appointment_id, amount_paid)
VALUES 
(1, 3000.00),
(2, 3500.00),
(3, 2500.00),
(4, 5000.00),
(5, 2000.00),
(6, 2500.00),
(7, 1500.00);

SHOW TABLES;
