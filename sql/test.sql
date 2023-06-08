-- Insert into student_apartment
INSERT INTO Apartment (id, total_rooms) VALUES ('E1', 10);
INSERT INTO Apartment (id, total_rooms) VALUES ('W1', 20);

-- Insert into Room
INSERT INTO Room (id, apartment_id, max_occupancy, occupied, president, maintenance_status) 
VALUES ('402', 'W1', 4, 0, 'PB20111683', 'Accept');

-- Insert into Manager
INSERT INTO Manager (id, gender, name, id_card, phone, apartment_id, schedule, password) 
VALUES ('M100203', 'Male', 'John Doe', '123456789', '1234567890', 'W1', '9am-5pm', '123456');

-- Insert into Student
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) 
VALUES ('PB20111683', 'Jane Chen', 'Male', '2000-01-01', 'Class 1', 'W1', '402', 'CS', '987654321', 
		'123 Main St', '0987654321', 'jane.doe@example.com', 'Computer Science', '123456', 1);

