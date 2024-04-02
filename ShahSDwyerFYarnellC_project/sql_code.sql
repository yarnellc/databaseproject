-- CREATE DATABASE:

-- DROP DATABASE `universityhealthservices`;
CREATE DATABASE  IF NOT EXISTS `universityhealthservices`;
USE `universityhealthservices`;


-- CREATE TABLES AND ADD INITIAL TUPLES: 
-- create university table
DROP TABLE IF EXISTS University;
CREATE TABLE University (
name VARCHAR(64) PRIMARY KEY,
stNum INT NOT NULL,
stName VARCHAR(64) NOT NULL,
zip CHAR(5) NOT NULL,
city VARCHAR(64) NOT NULL,
state CHAR(2) NOT NULL,
UNIQUE(stNum, stName, city, zip, state));

-- insert initial tuples into university table
INSERT INTO University (name, stNum, stName, city, state, zip) 
VALUES 
('Northeastern University', 360, 'Huntington Ave', 'Boston', 'MA', '02115'),
('Boston University', 233, 'Bay State Road', 'Boston', 'MA', '02115'),
('Boston College', 140, 'Commonwealth Ave', 'Chestnut Hill', 'MA', '02467');


-- create health center table
DROP TABLE IF EXISTS HealthCenter;
CREATE TABLE HealthCenter (
name VARCHAR(64) PRIMARY KEY,
stNum INT NOT NULL,
stName VARCHAR(64) NOT NULL,
zip CHAR(5) NOT NULL,
state CHAR(2) NOT NULL,
city VARCHAR(64) NOT NULL,
university VARCHAR(64) NOT NULL,
UNIQUE(stNum, stName, city,zip, state),
FOREIGN KEY (university) REFERENCES University(name) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into health center table
INSERT INTO HealthCenter (name, stNum, stName, city, state, zip, university) 
VALUES 
('Northeastern University Health And Counseling', 70, 'Forsyth St', 'Boston', 'MA', '02115', 'Northeastern University'),
('Boston University Student Health Services', 881, 'Commonwealth Ave', 'Boston', 'MA', '02115', 'Boston University'),
('Boston College University Health Services', 2150, 'Commonwealth Ave', 'Chestnut Hill', 'MA', '02467', 'Boston College');


-- create patient table
DROP TABLE IF EXISTS Patients;
CREATE TABLE Patients (
idNum INT AUTO_INCREMENT PRIMARY KEY,
firstName VARCHAR(64) NOT NULL,
lastName VARCHAR(64) NOT NULL,
college VARCHAR(64) NOT NULL,
phoneNum CHAR(10) NOT NULL,
Professor BOOLEAN NOT NULL,
Student BOOLEAN NOT NULL,
TA BOOLEAN NOT NULL,
last_treatment DATE,
UNIQUE( phoneNum),
FOREIGN KEY (college) REFERENCES University(name) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into patient table
INSERT INTO Patients ( firstName, lastName, college, phoneNum, Professor, Student, TA) 
VALUES 
	( 'Faith', 'Dwyer', 'Northeastern University', 1234567891, FALSE, TRUE, FALSE),
    ( 'Sanaya', 'Shah', 'Northeastern University', 2345678901, FALSE, TRUE, FALSE),
	( 'Chloe', 'Yarnell', 'Northeastern University', 3456789012, FALSE, TRUE, FALSE)
    ;
INSERT INTO Patients( firstName, lastName, college, phoneNum, Professor, Student, TA)  
VALUES ('Ethan', 'Kim', 'Northeastern University', 1234123412, FALSE, TRUE, FALSE);

-- create medical history table
DROP TABLE IF EXISTS MedicalHistory;
CREATE TABLE MedicalHistory (
patient INT PRIMARY KEY,
conditions VARCHAR(64) NOT NULL,
allergies VARCHAR(64) NOT NULL,
surgeries VARCHAR(64) NOT NULL,
immunizations VARCHAR(64) NOT NULL,
FOREIGN KEY (patient) REFERENCES Patients(idNum) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into medical history table
INSERT INTO MedicalHistory (patient, conditions, allergies, surgeries, immunizations)
VALUES
	(1, 'Diabetes', 'Penicillin', 'Knee replacement, Kidney transplant', 'Polio'),
    (2, 'Hypertension', 'Pollen, Aspirin', 'Appendectomy', 'Flu shot'),
    (3, 'Migraines', 'Aspirin, Sumatriptan', 'None', 'Tetanus, Hepatitis B');


-- create health insurance table
DROP TABLE IF EXISTS healthInsurance;
CREATE TABLE healthInsurance (
provider VARCHAR(64) NOT NULL,
policyNum INT NOT NULL,
patient INT NOT NULL,
copay INT NOT NULL,
PRIMARY KEY (patient, provider, policyNum),
FOREIGN KEY (patient) REFERENCES Patients(idNum) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into insurance table
INSERT INTO healthInsurance (provider, policyNum, copay, patient)
VALUES
	('Cigna', 15734378, 20, 3),
    ('Blue Cross Blue Shield', 23894, 0, 2),
    ('UnitedHealthcare', 1239862, 25, 1),
    ('None', 0, 0, 4);
    
    
-- create staff table
DROP TABLE IF EXISTS Staff;
CREATE TABLE Staff (
staffId INT AUTO_INCREMENT PRIMARY KEY,
firstName VARCHAR(64) NOT NULL,
lastName VARCHAR(64) NOT NULL,
healthCenter VARCHAR(64) NOT NULL,
role ENUM ('OfficeAssistant', 'Manager', 'Technician', 'Nurse', 'MD'),
FOREIGN KEY (HealthCenter) REFERENCES HealthCenter(name) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into staff table
INSERT INTO Staff ( firstName, lastName, healthCenter, role)
VALUES
	( 'John', 'Doe', 'Northeastern University Health And Counseling', 'OfficeAssistant'),
    ( 'Jane', 'Smith', 'Northeastern University Health And Counseling', 'Manager'),
    ( 'Aiden', 'Garcia', 'Northeastern University Health And Counseling', 'Technician'),
    ( 'Ethan', 'Nguyen', 'Northeastern University Health And Counseling', 'Nurse'),
    ( 'Sophia', 'Khan', 'Northeastern University Health And Counseling', 'MD');


-- create appointment table
DROP TABLE IF EXISTS Appointment;
CREATE TABLE Appointment (
aptNum INT AUTO_INCREMENT PRIMARY KEY,
patient INT ,
date DATE NOT NULL,
time TIME NOT NULL,
reason VARCHAR(64) NOT NULL,
FOREIGN KEY (patient) REFERENCES Patients(idNum) ON UPDATE CASCADE ON DELETE CASCADE
);

-- insert initial tuples into appointment table
INSERT INTO Appointment (patient, date, time, reason)
VALUES
	(1, '2023-06-07', '10:00:00', 'Routine check-up'),
    (2, '2023-06-07', '09:45:00', 'Flu-like symptoms'),
    (4, '2023-06-10', '15:15:00', 'Discussion of lab test results');

    
-- create exam table
DROP TABLE IF EXISTS Exam;
CREATE TABLE Exam (
examNum INT AUTO_INCREMENT PRIMARY KEY,
roomNum INT NOT NULL,
patient INT NOT NULL,
staff INT NOT NULL,
date DATE NOT NULL,
apt INT,
FOREIGN KEY (patient) REFERENCES Patients(idNum) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (staff) REFERENCES Staff(staffId) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (apt) REFERENCES Appointment(aptNum) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into exam table
INSERT INTO Exam ( roomNum, patient, staff, date, apt)
VALUES
	(1, 1, 4, '2023-05-09', 1),
    (2, 2, 4, '2023-06-09', 2),
    (3, 2, 5, '2023-05-16', NULL),
    (3, 4, 4, '2023-03-04', 3);
    

-- create diagnosis table
DROP TABLE IF EXISTS Diagnosis;
CREATE TABLE Diagnosis (
diagNum INT AUTO_INCREMENT PRIMARY KEY,
description TEXT NOT NULL,
illness BOOLEAN NOT NULL,
exam INT NOT NULL,
patient INT,
FOREIGN KEY (exam) REFERENCES Exam(examNum) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (patient) REFERENCES Patients(idNum) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into diagnosis table
INSERT INTO Diagnosis (description, illness, exam, patient)
VALUES
	('broken foot', FALSE, 1, 1),
	('cold', TRUE, 2, 2),
	('flu', TRUE, 3, 2),
	('cold', TRUE, 4, 4);
    
    
-- create treatment table
DROP TABLE IF EXISTS Treatment;
CREATE TABLE Treatment (
treatmentNum INT AUTO_INCREMENT PRIMARY KEY,
diagnosis INT NOT NULL,
date DATE NOT NULL,
patient INT,
type ENUM('Shot', 'PrescriptionMeds', 'OTCMeds', 'Referral', 'None'),
FOREIGN KEY (diagnosis) REFERENCES Diagnosis(diagNum) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into treatment table
INSERT INTO Treatment(diagnosis, date, type)
VALUES (1, '2023-06-07', 'Shot');
INSERT INTO Treatment(diagnosis, date, type)
VALUES (2, '2023-06-07', 'OTCMeds'), (3, '2023-06-10', 'PrescriptionMeds');
INSERT INTO Treatment(diagnosis, date, type)
VALUES(4, '2023-06-011', 'OTCMeds');

    
-- create bills table
DROP TABLE IF EXISTS Bills;
CREATE TABLE Bills (
patient INT NOT NULL,
billNum INT PRIMARY KEY,
amountDue INT NOT NULL,
paymentStatus BOOLEAN NOT NULL,
paymentDate DATE,
exam INT NOT NULL,
FOREIGN KEY (patient) REFERENCES Patients(idNum) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (exam) REFERENCES Exam(examNum) ON UPDATE CASCADE ON DELETE CASCADE);

-- insert initial tuples into bills table
INSERT INTO Bills (patient, billNum, amountDue, paymentStatus, paymentDate, exam)
VALUES
	(1, 049639, 120, TRUE, '2023-07-01', 1),
    (3, 049629, 65, TRUE, '2023-07-08', 3);
INSERT INTO Bills (patient, billNum, amountDue, paymentStatus, exam)
VALUES
    (2, 043632, 300, FALSE, 2); 


-- OBJECTS:

-- UNIVERSITY OBJECTS --
-- allow user to select university -- 
DELIMITER //
DROP PROCEDURE IF EXISTS selectU//
CREATE PROCEDURE selectU(name1 VARCHAR(64))
BEGIN
    SELECT *
    FROM University 
    WHERE University.name = name1;
END//
DELIMITER ;


-- allow user to insert university -- 
DELIMITER //
DROP PROCEDURE IF EXISTS insertU//
CREATE PROCEDURE insertU
(name VARCHAR(64),
stNum INT,
stName VARCHAR(64),
zip CHAR(5),
state CHAR(2),
city VARCHAR(64))
    BEGIN
    INSERT INTO University(name, stNum, stName, zip, state, city)
    VALUES(name, stNum, stName, zip, state, city);
    END //
DELIMITER ;

-- allow user to delete university --
DELIMITER //
DROP PROCEDURE IF EXISTS deleteU//
CREATE PROCEDURE deleteU(name VARCHAR(64)) 
BEGIN 
DELETE FROM University WHERE
name = University.name;
END//
DELIMITER ;


-- HEALTH CENTER OBJECTS
-- allow user to select health center -- 
DELIMITER //
DROP PROCEDURE IF EXISTS selectHC//
CREATE PROCEDURE selectHC(name VARCHAR(64))
BEGIN
    SELECT *
    FROM HealthCenter 
    WHERE HealthCenter.name = name;
END//
DELIMITER ;

-- allow user to insert health center -- 
DELIMITER //
DROP PROCEDURE IF EXISTS insertHC//
CREATE PROCEDURE insertHC
(name VARCHAR(64),
stNum INT,
stName VARCHAR(64),
zip CHAR(5),
state CHAR(2),
city VARCHAR(64),
university VARCHAR(64))
    BEGIN
    INSERT INTO healthCenter(name, stNum, stName, zip, state, city, university)
    VALUES(name, stNum, stName, zip, state, city, university);
    END //
DELIMITER ;

-- allow user to delete health center --
DELIMITER //
DROP PROCEDURE IF EXISTS deleteHC//
CREATE PROCEDURE deleteHC(name VARCHAR(64)) 
BEGIN 
DELETE FROM healthCenter WHERE
name = healthCenter.name;
END//
DELIMITER ;


-- PATIENT OBJECTS (not complete)
-- allow user to select a patient and their medical history from database -- 
DELIMITER //
DROP PROCEDURE IF EXISTS selectPat//
CREATE PROCEDURE selectPat( idNum INT)
BEGIN
    SELECT Patients.*, MedicalHistory.*
    FROM Patients
    JOIN MedicalHistory ON Patients.idNum = MedicalHistory.patient
    WHERE MedicalHistory.patient = idNum AND Patients.idNum = idNum;
END//
DELIMITER ;

-- allow user to insert a patient and their medical history --
DELIMITER //
DROP PROCEDURE IF EXISTS insertPatient//
CREATE PROCEDURE insertPatient(
    idNum INT,
    firstName VARCHAR(64),
    lastName VARCHAR(64),
    college VARCHAR(64),
    phoneNum CHAR(10),
    Professor BOOLEAN,
    Student BOOLEAN,
    TA BOOLEAN,
    last_treatment DATE,
    patient INT,
	conditions VARCHAR(64),
	allergies VARCHAR(64),
	surgeries VARCHAR(64),
	immunizations VARCHAR(64)
   
)
BEGIN
    INSERT INTO Patients(idNum, firstName, lastName, college, phoneNum, Professor, Student, TA, last_treatment)
    VALUES(idNum, firstName, lastName, college, phoneNum, Professor, Student, TA, last_treatment);

	INSERT INTO MedicalHistory(patient, conditions, allergies, surgeries, immunizations)
    VALUES(patient, conditions, allergies, surgeries, immunizations);
END//
DELIMITER ;

-- allow user to delete patient  --
DELIMITER //
DROP PROCEDURE IF EXISTS deletePatient//
CREATE PROCEDURE deletePatient( patientId INT, firstName VARCHAR(64), lastName VARCHAR(64)) 
BEGIN 
DELETE FROM Patients WHERE
firstName = firstName
AND lastName = lastName
AND patientId = idNum;
DELETE FROM MedicalHistory
WHERE patient = patientId;
DELETE FROM healthInsurance
WHERE patient = patientId;
END//
DELIMITER ;

-- allow the user to update patient info --
DELIMITER //
DROP PROCEDURE IF EXISTS updatePat//
CREATE PROCEDURE updatePat (up_idNum INT, up_val VARCHAR(64), new_val CHAR(64))
BEGIN
IF up_val = 'first name' THEN
UPDATE Patients SET firstName = new_val WHERE idNum = up_idNum;
ELSEIF up_val = 'last name' THEN 
UPDATE Patients SET lastName = new_val WHERE idNum = up_idNum;
ELSEIF up_val = 'college' THEN

	IF EXISTS (SELECT 1 FROM college WHERE name = new_val) THEN UPDATE Patients
	SET COLLEGE = new_val WHERE idNum = up_idNum;
    ELSE  
    SELECT 'This college is not in our database. Please enter: Northeastern University, 
    Boston College, or Boston University.' AS message;

    END IF;
ELSEIF up_val = 'phone number' THEN
UPDATE Patients SET phoneNum = new_val WHERE idNum = up_idNum;
ELSEIF up_val = 'professor' THEN
UPDATE Patients SET Professor = new_val WHERE idNum = up_idNum;
ELSEIF up_val = 'student' THEN
UPDATE Patients SET Student = new_val WHERE idNum = up_idNum;
ELSEIF up_val = 'TA' THEN
UPDATE Patients SET TA = new_val WHERE idNum = up_idNum;
ELSEIF up_val = 'last treatment' THEN
UPDATE Patients SET last_treatment = new_val WHERE idNum = up_idNum;
END IF;
END//
DELIMITER ;

-- easily update patient phone -- 
DELIMITER //
DROP PROCEDURE IF EXISTS updatePatientPhone//
CREATE PROCEDURE updatePatientPhone(patientId INT, newphone char(10))
BEGIN 
	UPDATE Patients
    SET phoneNum = newphone
    WHERE idNum = patientId;
  END//
  DELIMITER ;

-- easily update if patient's TA position --
DELIMITER //
DROP PROCEDURE IF EXISTS updatePatientTA //
CREATE PROCEDURE updatePatientTA(patientId INT, newTAposition tinyint(1))
BEGIN 
	UPDATE Patients
    SET TA = newTAposition
    WHERE idNum = patientId;
  END//
  DELIMITER ;

-- clean the patient database every five years --
DROP EVENT IF EXISTS dataclean;
CREATE EVENT dataclean
ON SCHEDULE EVERY 5 YEAR
DO
	DELETE FROM Patients
    WHERE last_treatment <= DATE_SUB(CURDATE(), INTERVAL 7 YEAR);
SET GLOBAL event_scheduler = ON;  -- citation = https://dev.mysql.com/doc/refman/8.0/en/events-configuration.html

--  update the last treatment date --
DELIMITER //
DROP TRIGGER IF EXISTS updateLast//
CREATE TRIGGER updateLast
AFTER INSERT ON Treatment
FOR EACH ROW
BEGIN 
UPDATE Patients
SET last_treatment = NEW.date
WHERE idNum = (SELECT patient FROM Exam WHERE examNum = NEW.diagnosis);
END//
DELIMITER ;


-- INSURANCE OBJECTS 
-- allow user to select insurance info --
DELIMITER //
DROP PROCEDURE IF EXISTS selectInsur//
CREATE PROCEDURE selectInsur(patient INT)
BEGIN
    SELECT healthInsurance.*
    FROM healthInsurance
    WHERE healthInsurance.patient = patient ;
END//
DELIMITER ;

-- allow user to insert an insurance policy --
DELIMITER //
DROP PROCEDURE IF EXISTS insertInsur//
CREATE PROCEDURE insertInsur(provider VARCHAR(64), patient INT, policyNum INT, copay INT) 
BEGIN 
INSERT INTO healthInsurance(provider, patient, policyNum, copay)
VALUES ( provider, patient, policyNum, copay);
END//
DELIMITER ;

-- allow user to update insurance info --
DELIMITER //
DROP PROCEDURE IF EXISTS updateInsur//
CREATE PROCEDURE updateInsur (up_idNum INT, up_val VARCHAR(64), new_val CHAR(64))
BEGIN
IF up_val = 'provider' THEN
UPDATE healthInsurance SET provider = new_val WHERE patient = up_idNum;
ELSEIF up_val = 'policyNum' THEN 
UPDATE healthInsurance SET policyNum = new_val WHERE patient = up_idNum;
ELSEIF up_val = 'copay' THEN
UPDATE healthInsurance SET copay = new_val WHERE patient = up_idNum;
END IF;
END//
DELIMITER ;


-- STAFF OBJECTS 
-- allow user to select staff -- 
DELIMITER //
DROP PROCEDURE IF EXISTS selectStaff//
CREATE PROCEDURE selectStaff( staffId INT)
BEGIN
    SELECT *
    FROM Staff
    WHERE Staff.staffId = staffId;
END//
DELIMITER ;

-- allow user to insert staff -- 
DELIMITER //
DROP PROCEDURE IF EXISTS insertStaff//
CREATE PROCEDURE insertStaff
(    staffId INT,
	firstName VARCHAR(64),
	lastName VARCHAR(64),
	healthCenter VARCHAR(64),
	role ENUM ('OfficeAssistant', 'Manager', 'Technician', 'Nurse', 'MD'))
    BEGIN
    INSERT INTO Staff(staffId, firstName, lastName, healthCenter, role)
    VALUES(staffId, firstName, lastName, healthCenter, role);
    END //
DELIMITER ;

-- allow user to delete staff --
DELIMITER //
DROP PROCEDURE IF EXISTS deleteStaff//
CREATE PROCEDURE deleteStaff( staffId INT) 
BEGIN 
DELETE FROM Staff WHERE
staffId = Staff.staffId;
END//
DELIMITER ;

-- allow user to update staff info --
DELIMITER //
DROP PROCEDURE IF EXISTS updateStaff//
CREATE PROCEDURE updateStaff (up_staffId INT, up_val VARCHAR(64), new_val CHAR(64))
BEGIN
IF up_val = 'first name' THEN
UPDATE Staff SET firstName = new_val WHERE staffId = up_staffId;
ELSEIF up_val = 'last name' THEN
UPDATE Staff SET lastName = new_val WHERE staffId = up_staffId;
ELSEIF up_val = 'role' THEN
UPDATE Staff SET role = new_val WHERE staffId = up_staffId;
END IF;
END//
DELIMITER ;


-- APPOINTMENT OBJECTS
-- allow user to select appointment --
DELIMITER //
DROP PROCEDURE IF EXISTS selectApt //
CREATE PROCEDURE selectApt(patient iNT)
BEGIN
SELECT *
FROM Appointment
WHERE Appointment.patient = patient;
END//
DELIMITER ;

-- allow user to insert appointment -- 
DELIMITER //
DROP PROCEDURE IF EXISTS insertApt1 //
CREATE PROCEDURE insertApt1 (patient INT, date DATE, time TIME, reason VARCHAR(64))
BEGIN
INSERT INTO Appointment(patient, date, time, reason)
    VALUES(patient, date, time , reason );
    END //
DELIMITER ;

-- allow user to delete appointment --
DELIMITER // 
DROP PROCEDURE IF EXISTS deleteApt//
CREATE PROCEDURE deleteApt(patient1 INT)
BEGIN 
DELETE FROM Appointment WHERE
patient1 = patient;
END//
DELIMITER ;

-- allow user to update appointment --
DELIMITER //
DROP PROCEDURE IF EXISTS updateApt//
CREATE PROCEDURE updateApt (up_idNum INT, up_val VARCHAR(64), new_val CHAR(64))
BEGIN
    IF up_val = 'date' THEN
        UPDATE Appointment SET `date` = new_val WHERE up_idNum = up_idNum;
    ELSEIF up_val = 'time' THEN 
        UPDATE Appointment SET `time` = new_val WHERE up_idNum = up_idNum;
    ELSEIF up_val = 'reason' THEN
        UPDATE Appointment SET reason = new_val WHERE up_idNum = up_idNum;
    ELSEIF up_val = 'exam' THEN
        UPDATE Appointment SET exam = new_val WHERE up_idNum = up_idNum;
    END IF;
END //
DELIMITER ;


-- EXAM OBJECTS 
-- allow user to select exam  --
DELIMITER //
DROP PROCEDURE IF EXISTS selectExam//
CREATE PROCEDURE selectExam( examNum INT)
BEGIN
    SELECT Exam.*
    FROM Exam
    WHERE Exam.examNum = examNum;
END//
DELIMITER ;

-- allow user to insert exam --
DELIMITER //
DROP PROCEDURE IF EXISTS insertExam//
CREATE PROCEDURE insertExam(roomNum INT, patient INT, staff INT, date DATE, apt INT) 
BEGIN 
INSERT INTO Exam(roomNum, patient, staff, date, apt)
VALUES ( roomNum, patient, staff, date, apt);
END//
DELIMITER ;

-- allow user to delete exam --
DELIMITER //
DROP PROCEDURE IF EXISTS deleteExam//
CREATE PROCEDURE deleteExam(examNum1 INT)
BEGIN
DELETE FROM Exam
WHERE examNum1 = examNum;
END //
DELIMITER ;


-- allow user to update exam info --
DELIMITER //
DROP PROCEDURE IF EXISTS updateExam//
CREATE PROCEDURE updateExam (up_examNum INT, up_val VARCHAR(64), new_val CHAR(64))
BEGIN
IF up_val = 'room number' THEN
UPDATE Exam SET roomNum = new_val WHERE examNum = up_examNum;
ELSEIF up_val = 'patient id' THEN 
UPDATE Exam SET patient = new_val WHERE examNum = up_examNum;
ELSEIF up_val = 'staff id' THEN
UPDATE Exam SET staff = new_val WHERE examNum = up_examNum;
END IF;
END//
DELIMITER ;


-- DIAGNOSIS OBJECTS
-- allow user to select diagnosis -- 
DELIMITER //
DROP PROCEDURE IF EXISTS selectDiag//
CREATE PROCEDURE selectDiag( diagNum INT)
BEGIN
    SELECT *
    FROM Diagnosis
    WHERE Diagnosis.diagNum = diagNum;
END//
DELIMITER ;

-- allow user to insert diagnosis --
DELIMITER //
DROP PROCEDURE IF EXISTS insertDiag//
CREATE PROCEDURE insertDiag(diagNum INT, description TEXT, illness BOOLEAN, exam INT, patient INT) 
BEGIN 
INSERT INTO Diagnosis(diagNum, description, illness, exam, patient)
VALUES ( diagNum, description, illness, exam, patient);
END//
DELIMITER ;

-- allow user to delete diagnosis -- 
DELIMITER //
DROP PROCEDURE IF EXISTS deleteDiag//
CREATE PROCEDURE deleteDiag( patientId INT) 
BEGIN 
DELETE FROM Diagnosis WHERE
patient = patientId;
END//
DELIMITER ;


-- TREATMENT OBJECTS
-- allow user to select treatment -- 
DELIMITER //
DROP PROCEDURE IF EXISTS selectTreat//
CREATE PROCEDURE selectTreat( treatmentNum INT)
BEGIN
    SELECT *
    FROM Treatment
    WHERE Treatment.treatmentNum = treatmentNum;
END//
DELIMITER ;

-- allow user to insert treatment -- 
DELIMITER //
DROP PROCEDURE IF EXISTS insertTreat//
CREATE PROCEDURE insertTreat
(    treatmentNum INT,
	diagnosis INT,
	date DATE,
	patient INT,
    type VARCHAR(64))
    BEGIN
    INSERT INTO Treatment(treatmentNum, diagnosis, date, patient, type)
    VALUES(treatmentNum, diagnosis, date, patient, type);
    END //
DELIMITER ;

-- allow user to delete treatment --
DELIMITER //
DROP PROCEDURE IF EXISTS deleteTreat//
CREATE PROCEDURE deleteTreat( treatmentNum1 INT) 
BEGIN 
DELETE FROM Treatment WHERE
treatmentNum1 = treatmentNum;
END//
DELIMITER ;


-- BILLS OBJECTS
-- allow user to select bill  --
DELIMITER //
DROP PROCEDURE IF EXISTS selectBill//
CREATE PROCEDURE selectBill( billNum INT)
BEGIN
    SELECT Bills.*
    FROM Bills
    WHERE Bills.billNum = billNum;
END//
DELIMITER ;    

-- allow user to insert a bill
DELIMITER //
DROP PROCEDURE IF EXISTS insertBill//
CREATE PROCEDURE insertBill( patient INT, billNum INT, amountDue INT, paymentStatus BOOLEAN, exam INT)
    BEGIN
    INSERT INTO Bills(patient, billNum, amountDue, paymentStatus, exam)
    VALUES(patient, billNum, amountDue, paymentStatus, exam);
    END //
DELIMITER ;


-- allow user to update billing info --
DELIMITER //
DROP PROCEDURE IF EXISTS updateBill//
CREATE PROCEDURE updateBill (up_billNum INT, up_val VARCHAR(64), new_val CHAR(64))
BEGIN
IF up_val = 'amount due' THEN
UPDATE Bills SET amountDue = new_val WHERE billNum = up_billNum;
ELSEIF up_val = 'payment status' THEN 
UPDATE Bills SET paymentStatus = new_val WHERE billNum = up_billNum;
ELSEIF up_val = 'payment date' THEN
UPDATE Bills SET paymentDate = new_val WHERE billNum = up_examNum;
END IF;
END//
DELIMITER ;


-- GUI OBJECTS
-- display limited fields for appointment
DELIMITER //
DROP PROCEDURE IF EXISTS selectAptforP//
CREATE PROCEDURE selectAptforP( patientIdGUI INT)
BEGIN
    SELECT a.time, a.date, a.reason
    FROM Appointment a
    WHERE a.patient = patientIdGUI;
END//
DELIMITER ; 

-- display limited fields for bill
DELIMITER //
DROP PROCEDURE IF EXISTS selectBillforP//
CREATE PROCEDURE selectBillforP( patientIdGUI INT)
BEGIN
    SELECT billNum, amountDue, paymentStatus, exam
    FROM Bills
    WHERE patient = patientIdGUI;
END//
DELIMITER ; 

-- display patient's health center
DELIMITER //
DROP PROCEDURE IF EXISTS selectHCforP//
CREATE PROCEDURE selectHCforP( patientIdGUI INT)
BEGIN
    SELECT HC.*
    FROM Patients P
    JOIN University U ON P.college = U.name
    JOIN HealthCenter HC ON HC.university = U.name
    WHERE P.idNum = patientIdGUI;
END//
DELIMITER ; 