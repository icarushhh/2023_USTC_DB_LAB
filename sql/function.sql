DELIMITER //
CREATE PROCEDURE check_in(IN student_id VARCHAR(20), IN student_name VARCHAR(50), IN student_gender VARCHAR(10), IN student_born VARCHAR(50), IN student_class VARCHAR(50), IN student_college VARCHAR(100), IN student_id_card VARCHAR(50), IN student_domicile VARCHAR(100), IN student_phone VARCHAR(15), IN student_email VARCHAR(100), IN student_major VARCHAR(100), IN ro_id VARCHAR(20), IN apart_id VARCHAR(20))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction in case of an error
        ROLLBACK;
    END;

    START TRANSACTION;
    INSERT INTO Student (id, name, gender, born, class, college, id_card, domicile, phone, email, major, room_id, apartment_id, password, state) VALUES (student_id, student_name, student_gender, student_born, student_class, student_college, student_id_card, student_domicile, student_phone, student_email, student_major, ro_id, apart_id, RIGHT(student_id_card, 6), 1);
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE check_out(IN student_id VARCHAR(20))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction in case of an error
        ROLLBACK;
    END;

    START TRANSACTION;
    DELETE FROM Student WHERE id = student_id;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_student_info(IN student_id VARCHAR(20))
BEGIN
    SELECT id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, password, 
    state, photo FROM Student WHERE id = student_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_student_info(
    IN student_id VARCHAR(20),
    IN new_photo MEDIUMBLOB,
    IN new_phone VARCHAR(15),
    IN new_email VARCHAR(100),
    IN new_password VARCHAR(50)
)
BEGIN
    UPDATE Student 
    SET 
        photo = new_photo,
        phone = new_phone,
        email = new_email,
        password = new_password
    WHERE id = student_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_student_state(IN student_id VARCHAR(20), IN new_state BOOLEAN)
BEGIN
    UPDATE Student SET state = new_state WHERE id = student_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_student_room(IN student_id VARCHAR(20), IN new_apart VARCHAR(20), IN new_room VARCHAR(20))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction in case of an error
        ROLLBACK;
    END;

    START TRANSACTION;
    -- Check if the target room is full
    IF (SELECT occupied FROM Room WHERE id = new_room AND apartment_id = new_apart) < (SELECT max_occupancy FROM Room WHERE id = new_room AND apartment_id = new_apart) THEN
        -- Update the student
        UPDATE Student SET apartment_id = new_apart, room_id = new_room WHERE id = student_id;
    END IF;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_manager_info(IN manager_id VARCHAR(20))
BEGIN
    SELECT id, name, gender, apartment_id, id_card, phone, schedule, photo FROM Manager WHERE id = manager_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_manager_info(
    IN manager_id VARCHAR(20),
    IN new_phone VARCHAR(15),
    IN new_password VARCHAR(50),
    IN new_photo MEDIUMBLOB
)
BEGIN
    UPDATE Manager 
    SET 
        phone = new_phone,
        password = new_password,
        photo = new_photo
    WHERE id = manager_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE CountPhotosForGivenMaintenance(IN given_maintenance_id VARCHAR(20))
BEGIN
    SELECT COUNT(photo_id) AS photo_count
    FROM MaintenancePhotos
    WHERE maintenance_id = given_maintenance_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_room_info(IN ro_id VARCHAR(20), IN apart_id VARCHAR(20))
BEGIN
    SELECT max_occupancy, occupied, president, maintenance_status FROM Room WHERE id = ro_id AND apartment_id = apart_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_room_president(IN ro_id VARCHAR(20), IN apart_id VARCHAR(20), IN new_president VARCHAR(20))
BEGIN
    UPDATE Room SET president = new_president WHERE id = ro_id AND apartment_id = apart_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE report_maintenance(IN student_id VARCHAR(20), IN ro_id VARCHAR(20), IN apart_id VARCHAR(20), IN fault_in VARCHAR(1000), IN fault_photo MEDIUMBLOB)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction in case of an error
        ROLLBACK;
    END;

    START TRANSACTION;
    INSERT INTO Maintenance (room_id, apartment_id, reporter_id, fault_info, approval_status, application_time) VALUES (ro_id, apart_id, student_id, fault_in, 'Pending', NOW());
    INSERT INTO MaintenancePhotos (maintenance_id, photo) VALUES (LAST_INSERT_ID(), fault_photo);
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_maintenance_status(IN order_id INT, IN new_status VARCHAR(20))
BEGIN
    UPDATE Maintenance SET approval_status = new_status WHERE id = order_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_maintenance_person(IN order_id INT, IN new_person VARCHAR(20))
BEGIN
    UPDATE Maintenance SET person_in_charge = new_person WHERE id = order_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE register_visitor(IN id_card VARCHAR(50), IN name VARCHAR(50), IN category VARCHAR(20), IN phone VARCHAR(15), IN purpose VARCHAR(1000), IN target_room VARCHAR(20), IN target_apartment VARCHAR(20), IN departure_time DATETIME)
BEGIN
    INSERT INTO Visitor (id_card, name, category, phone, purpose, target_room, target_apartment, arrival_time, departure_time) VALUES (id_card, name, category, phone, purpose, target_room, target_apartment, NOW(), departure_time);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetStudentsInRoom(IN given_room_id VARCHAR(20), IN given_apartment_id VARCHAR(20))
BEGIN
    SELECT id AS student_id, name AS student_name
    FROM Student
    WHERE room_id = given_room_id AND apartment_id = given_apartment_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE apply_for_leave(IN student_id VARCHAR(20), IN leave_time DATETIME, IN expected_return_time DATETIME, IN purpose VARCHAR(1000), IN destination VARCHAR(1000))
BEGIN
    DECLARE room_id VARCHAR(20);
    DECLARE apartment_id VARCHAR(20);
    SELECT room_id, apartment_id INTO room_id, apartment_id FROM Student WHERE id = student_id;
    INSERT INTO LeaveApplication (student_id, room_id, apartment_id, leave_time, expected_return_time, approval_status, purpose, destination) VALUES (student_id, room_id, apartment_id, leave_time, expected_return_time, 'Pending', purpose, destination);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE apply_for_return(IN student_id VARCHAR(20), IN return_time DATETIME)
BEGIN
    DECLARE room_id VARCHAR(20);
    DECLARE apartment_id VARCHAR(20);
    SELECT room_id, apartment_id INTO room_id, apartment_id FROM Student WHERE id = student_id;
    INSERT INTO ReturnApplication (student_id, room_id, apartment_id, return_time, approval_status) VALUES (student_id, room_id, apartment_id, return_time, 'Pending');
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE delete_leave(IN leave_id INT)
BEGIN
    DELETE FROM LeaveApplication WHERE id = leave_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE delete_return(IN return_id INT)
BEGIN
    DELETE FROM ReturnApplication WHERE id = return_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_leave_status(IN order_id INT, IN new_status VARCHAR(20))
BEGIN
    UPDATE LeaveApplication SET approval_status = new_status WHERE id = order_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_return_status(IN order_id INT, IN new_status VARCHAR(20))
BEGIN
    UPDATE ReturnApplication SET approval_status = new_status WHERE id = order_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE StudentLogin(IN input_id VARCHAR(20), IN input_password VARCHAR(50), OUT result VARCHAR(50))
BEGIN
    DECLARE temp_password VARCHAR(50);
    SELECT password INTO temp_password FROM Student WHERE id = input_id;
    IF temp_password IS NULL THEN
        SET result = 'Student ID not found.';
    ELSEIF temp_password != input_password THEN
        SET result = 'Incorrect password.';
    ELSE
        SET result = 'Login successful.';
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ManagerLogin(IN input_id VARCHAR(20), IN input_password VARCHAR(50), OUT result VARCHAR(50))
BEGIN
    DECLARE temp_password VARCHAR(50);
    SELECT password INTO temp_password FROM Manager WHERE id = input_id;
    IF temp_password IS NULL THEN
        SET result = 'Manager ID not found.';
    ELSEIF temp_password != input_password THEN
        SET result = 'Incorrect password.';
    ELSE
        SET result = 'Login successful.';
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_visitor(
    IN iden_card VARCHAR(50), 
    IN new_name VARCHAR(50), 
    IN new_category VARCHAR(20), 
    IN new_phone VARCHAR(15), 
    IN new_purpose VARCHAR(1000), 
    IN new_target_room VARCHAR(20), 
    IN new_target_apartment VARCHAR(20), 
    IN new_departure_time DATETIME)
BEGIN
    UPDATE Visitor 
    SET 
        name = new_name, 
        category = new_category, 
        phone = new_phone, 
        purpose = new_purpose, 
        target_room = new_target_room, 
        target_apartment = new_target_apartment, 
        departure_time = new_departure_time 
    WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE delete_visitor(IN iden_card VARCHAR(50))
BEGIN
    DELETE FROM Visitor WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_leave_applications(IN student_id_in VARCHAR(20))
BEGIN
    SELECT 
        LeaveApplication.id, 
        LeaveApplication.student_id, 
        Student.name, 
        Student.phone, 
        LeaveApplication.room_id, 
        LeaveApplication.apartment_id, 
        LeaveApplication.leave_time, 
        LeaveApplication.expected_return_time, 
        LeaveApplication.purpose, 
        LeaveApplication.destination, 
        LeaveApplication.approval_status
    FROM 
        LeaveApplication
    JOIN 
        Student ON LeaveApplication.student_id = Student.id
    WHERE 
        LeaveApplication.student_id = student_id_in;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_return_applications(IN student_id_in VARCHAR(20))
BEGIN
    SELECT 
        ReturnApplication.id, 
        ReturnApplication.student_id, 
        Student.name, 
        Student.phone, 
        ReturnApplication.room_id, 
        ReturnApplication.apartment_id, 
        ReturnApplication.return_time, 
        ReturnApplication.approval_status
    FROM 
        ReturnApplication
    JOIN 
        Student ON ReturnApplication.student_id = Student.id
    WHERE 
        ReturnApplication.student_id = student_id_in;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_apartment_maintenance_student(IN stud_id VARCHAR(20))
BEGIN
    SELECT 
        Maintenance.id, 
        Maintenance.room_id, 
        Maintenance.apartment_id, 
        Maintenance.reporter_id, 
        Maintenance.fault_info, 
        Maintenance.approval_status, 
        Maintenance.person_in_charge, 
        Maintenance.application_time, 
        Maintenance.completion_time,
        MaintenancePhotos.photo,
        Student.name AS reporter_name
    FROM 
        Maintenance
    JOIN 
         Student ON Maintenance.reporter_id = Student.id
    LEFT JOIN
        MaintenancePhotos ON Maintenance.id = MaintenancePhotos.maintenance_id
    WHERE 
        Maintenance.apartment_id = (SELECT apartment_id FROM Student WHERE id = stud_id) AND Maintenance.room_id = (SELECT room_id FROM Student WHERE id = stud_id);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_apartment_maintenance_administrator()
BEGIN
    SELECT 
        Maintenance.id, 
        Maintenance.room_id, 
        Maintenance.apartment_id, 
        Maintenance.reporter_id, 
        Maintenance.fault_info, 
        Maintenance.approval_status, 
        Maintenance.person_in_charge, 
        Maintenance.application_time, 
        Maintenance.completion_time,
        MaintenancePhotos.photo,
        Student.name AS reporter_name
    FROM 
        Maintenance
    JOIN 
         Student ON Maintenance.reporter_id = Student.id
    LEFT JOIN
        MaintenancePhotos ON Maintenance.id = MaintenancePhotos.maintenance_id;
END //
DELIMITER ;
