CREATE TABLE Apartment (
    id VARCHAR(20) PRIMARY KEY,
    total_rooms INT DEFAULT NULL
);

CREATE TABLE Room (
    id VARCHAR(20) NOT NULL,
    apartment_id VARCHAR(20) NOT NULL,
    max_occupancy INT DEFAULT NULL,
    occupied INT DEFAULT NULL,
    president VARCHAR(20) DEFAULT NULL,
    maintenance_status VARCHAR(20) DEFAULT NULL,
    PRIMARY KEY (apartment_id, id),
    FOREIGN KEY (apartment_id) REFERENCES Apartment(id)
);

CREATE TABLE Manager (
    id VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10) DEFAULT NULL,
    name VARCHAR(50) DEFAULT NULL,
    id_card VARCHAR(50) DEFAULT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    apartment_id VARCHAR(20) DEFAULT NULL,
    schedule VARCHAR(50) DEFAULT NULL,
    password VARCHAR(50) DEFAULT NULL,
    photo MEDIUMBLOB DEFAULT NULL,
    FOREIGN KEY (apartment_id) REFERENCES Apartment(id)
);

CREATE TABLE Student (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) DEFAULT NULL,
    gender VARCHAR(10) DEFAULT NULL,
    born VARCHAR(50) DEFAULT NULL,
    class VARCHAR(50) DEFAULT NULL,
    apartment_id VARCHAR(20) DEFAULT NULL,
    room_id VARCHAR(20) DEFAULT NULL,
    college VARCHAR(100) DEFAULT NULL,
    id_card VARCHAR(50) DEFAULT NULL,
    domicile VARCHAR(100) DEFAULT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    email VARCHAR(100) DEFAULT NULL,
    major VARCHAR(100) DEFAULT NULL,
    password VARCHAR(50) DEFAULT NULL,
    state BOOLEAN DEFAULT 1,
    photo MEDIUMBLOB DEFAULT NULL,
    FOREIGN KEY (apartment_id, room_id) REFERENCES Room(apartment_id, id)
);

CREATE TABLE Maintenance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id VARCHAR(20) DEFAULT NULL,
    apartment_id VARCHAR(20) DEFAULT NULL,
    reporter_id VARCHAR(20) DEFAULT NULL,
    reporter_name VARCHAR(50) DEFAULT NULL,
    fault_info VARCHAR(1000) DEFAULT NULL,
    approval_status VARCHAR(20) DEFAULT NULL,
    person_in_charge VARCHAR(50) DEFAULT NULL,
    application_time DATETIME DEFAULT NULL,
    completion_time DATETIME DEFAULT NULL,
    FOREIGN KEY (apartment_id, room_id) REFERENCES Room(apartment_id, id),
    FOREIGN KEY (reporter_id) REFERENCES Student(id),
    FOREIGN KEY (person_in_charge) REFERENCES Manager(id)
);

CREATE TABLE Visitor (
    id_card VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) DEFAULT NULL,
    category VARCHAR(20) DEFAULT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    purpose VARCHAR(1000) DEFAULT NULL, 
    target_room VARCHAR(20) DEFAULT NULL,
    target_apartment VARCHAR(20) DEFAULT NULL,
    arrival_time DATETIME DEFAULT NULL,
    departure_time DATETIME DEFAULT NULL,
    FOREIGN KEY (target_apartment, target_room) REFERENCES Room(apartment_id, id)
);

CREATE TABLE AvailableRooms (
    apartment_id VARCHAR(20) NOT NULL,
    room_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (apartment_id, room_id),
    FOREIGN KEY (apartment_id, room_id) REFERENCES Room(apartment_id, id)
);

CREATE TABLE MaintenancePhotos (
    maintenance_id INT DEFAULT NULL,
    photo_id INT AUTO_INCREMENT PRIMARY KEY,
    photo MEDIUMBLOB DEFAULT NULL,
    FOREIGN KEY (maintenance_id) REFERENCES Maintenance(id) ON DELETE CASCADE
);

CREATE TABLE LeaveApplication (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) DEFAULT NULL,
    student_name VARCHAR(50) DEFAULT NULL,
    room_id VARCHAR(20) DEFAULT NULL,
    apartment_id VARCHAR(20) DEFAULT NULL,
    leave_time DATETIME DEFAULT NULL,
    expected_return_time DATETIME DEFAULT NULL,
    purpose VARCHAR(1000) DEFAULT NULL,
    destination VARCHAR(1000) DEFAULT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    approval_status VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(id),
    FOREIGN KEY (apartment_id, room_id) REFERENCES Room(apartment_id, id)
);

CREATE TABLE ReturnApplication (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) DEFAULT NULL,
    student_name VARCHAR(50) DEFAULT NULL,
    room_id VARCHAR(20) DEFAULT NULL,
    apartment_id VARCHAR(20) DEFAULT NULL,
    return_time DATETIME DEFAULT NULL,
    phone VARCHAR(15) DEFAULT NULL,
    approval_status VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(id),
    FOREIGN KEY (apartment_id, room_id) REFERENCES Room(apartment_id, id)
);
/*
CREATE VIEW StudentView AS
SELECT s.*, m.id AS maintenance_id, m.fault_info, m.approval_status, m.person_in_charge, m.application_time, m.completion_time, r.max_occupancy, r.occupied, r.president, r.maintenance_status, a.id AS apart_id, m2.name AS manager_name, m2.phone AS manager_phone, m2.photo AS manager_photo, m2.schedule AS manager_schedule, m2.id AS manager_id
FROM Student s
JOIN Room r ON s.room_id = r.id AND s.apartment_id = r.apartment_id
JOIN Apartment a ON s.apartment_id = a.id
JOIN Maintenance m ON s.id = m.reporter_id
JOIN Manager m2 ON a.id = m2.apartment_id;

CREATE VIEW ManagerView AS
SELECT m.*, mi.id AS maintenance_id, mi.fault_info, mi.approval_status, mi.reporter_id, mi.reporter_name, mi.application_time, mi.completion_time, a.id AS apart_id, a.total_rooms, r.id AS room_id, r.max_occupancy, r.occupied, r.president, r.maintenance_status, v.id_card AS visitor_id_card, v.name AS visitor_name, v.category AS visitor_category, v.phone AS visitor_phone, v.purpose AS visitor_purpose, v.arrival_time AS visitor_arrival_time, v.departure_time AS visitor_departure_time
FROM Manager m
JOIN Apartment a ON m.apartment_id = a.id
JOIN Room r ON a.id = r.apartment_id AND m.apartment_id = r.apartment_id
JOIN Maintenance mi ON m.id = mi.person_in_charge
JOIN Visitor v ON a.id = v.target_apartment;
*/