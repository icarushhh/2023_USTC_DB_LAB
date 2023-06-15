-- Insert into Apartment
INSERT INTO Apartment (id, total_rooms) VALUES ('W1', 5);
INSERT INTO Apartment (id, total_rooms) VALUES ('E1', 5);

-- Insert into Room
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('102', 'W1', 4, 'PB20111683');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('203', 'W1', 4, 'PB20111684');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('311', 'W1', 4, 'PB20111685');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('402', 'W1', 4, 'PB20111686');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('509', 'W1', 4, 'PB20111687');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('102', 'E1', 4, 'PB20111688');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('302', 'E1', 4, 'PB20111689');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('312', 'E1', 4, 'PB20001718');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('402', 'E1', 4, 'PB20121452');
INSERT INTO Room (id, apartment_id, max_occupancy, president) VALUES ('502', 'E1', 4, 'PB20011563');

-- Insert into Manager
INSERT INTO Manager (id, gender, name, id_card, phone, apartment_id, schedule, password) VALUES ('A01', 'Male', 'Eric Fan', '611103200211023611', '18329646187', 'E1', '8am-5pm', '123456');
INSERT INTO Manager (id, gender, name, id_card, phone, apartment_id, schedule, password) VALUES ('A02', 'Female', 'Cathy Lee', '601103234211023611', '18129996187', 'E1', '5pm-11pm', '321password');
INSERT INTO Manager (id, gender, name, id_card, phone, apartment_id, schedule, password) VALUES ('A03', 'Male', 'John Doe', '612103200211023611', '12229646187', 'W1', '8am-5pm', '563password123');
INSERT INTO Manager (id, gender, name, id_card, phone, apartment_id, schedule, password) VALUES ('A04', 'Female', 'Jane Swift', '613103200211021311', '19023646187', 'W1', '5pm-11pm', '896password123');

-- Insert into Student
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20111683', 'Jane Chen', 'Male', '2000-01-01', 'Class 1', 'W1', '102', 'CS', '611103200211023611', '123 Main St', '11029646087', 'jane.doe@example.com', 'Computer Science', 'password321', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20111684', 'Psdlls', 'Female', '2001-01-01', 'Class 1', 'W1', '203', 'CS', '611103200211023611', '123 Main St', '11129646187', 'jane.doe@example.com', 'Computer Science', 'password123', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20111685', 'Ssjydf', 'Female', '2002-01-01', 'Class 1', 'W1', '311', 'CS', '611103200211023611', '123 Main St', '11229646187', 'jane.doe@example.com', 'Computer Science', 'password456', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20111686', 'Lasd Asd', 'Male', '2003-01-01', 'Class 2', 'W1', '402', 'CS', '611103200211023611', '123 Main St', '11329646187', 'jane.doe@example.com', 'Computer Science', 'password654', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20111687', '李田所', 'Male', '2000-02-01', 'Class 2', 'W1', '509', 'CS', '611103200211023611', '123 Main St', '11429646187', 'jane.doe@example.com', 'Computer Science', 'password789', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20111688', '淳·简', 'Female', '2000-03-01', 'Class 2', 'E1', '102', 'CS', '611103200211023611', '123 Main St', '11529646187', 'jane.doe@example.com', 'Computer Science', 'password987', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20111689', 'Lsdasadxlasidasdxsadas', 'Male', '2000-04-01', 'Class 3', 'E1', '302', 'CS', '611103200211023611', '123 Main St', '11629646187', 'jane.doe@example.com', 'Computer Science', 'password012', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20001718', 'Hsjdna', 'Female', '2000-05-01', 'Class 3', 'E1', '312', 'CS', '611103200211023611', '123 Main St', '11729646187', 'jane.doe@example.com', 'Computer Science', '123456', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20121452', 'Lasia', 'Female', '2000-06-01', 'Class 3', 'E1', '402', 'CS', '611103200211023611', '123 Main St', '11829646187', 'jane.doe@example.com', 'Computer Science', 'ppppppppp', 1);
INSERT INTO Student (id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, state) VALUES ('PB20011563', 'Asndlpaso', 'Male', '2000-07-01', 'Class 3', 'E1', '502', 'CS', '611103200211023611', '123 Main St', '11929646187', 'jane.doe@example.com', 'Computer Science', '111111111', 1);

