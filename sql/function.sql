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
    UPDATE Room SET occupied = occupied + 1 WHERE id = ro_id AND apartment_id = apart_id;
    DELETE FROM AvailableRooms WHERE room_id = ro_id AND apartment_id = apart_id AND (SELECT occupied FROM Room WHERE id = ro_id AND apartment_id = apart_id) = (SELECT max_occupancy FROM Room WHERE id = ro_id AND apartment_id = apart_id);
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE check_out(IN student_id VARCHAR(20))
BEGIN
    DECLARE ro_id VARCHAR(20);
    DECLARE apart_id VARCHAR(20);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction in case of an error
        ROLLBACK;
    END;

    START TRANSACTION;
    SELECT room_id, apartment_id INTO ro_id, apart_id FROM Student WHERE id = student_id;
    UPDATE Room SET occupied = occupied - 1 WHERE id = ro_id AND apartment_id = apart_id;
    DELETE FROM Student WHERE id = student_id;
    IF NOT EXISTS (SELECT * FROM AvailableRooms WHERE room_id = ro_id AND apartment_id = apart_id) THEN
        INSERT INTO AvailableRooms (room_id, apartment_id) VALUES (ro_id, apart_id);
    END IF;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_student_info(IN student_id VARCHAR(20))
BEGIN
    SELECT id, name, gender, born, class, apartment_id, room_id, college, id_card, domicile, phone, email, major, state, photo FROM Student WHERE id = student_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_student_phone(IN student_id VARCHAR(20), IN new_phone VARCHAR(15))
BEGIN
    UPDATE Student SET phone = new_phone WHERE id = student_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_student_email(IN student_id VARCHAR(20), IN new_email VARCHAR(100))
BEGIN
    UPDATE Student SET email = new_email WHERE id = student_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_student_password(IN student_id VARCHAR(20), IN new_password VARCHAR(50))
BEGIN
    UPDATE Student SET password = new_password WHERE id = student_id;
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
        -- Update the old room
        UPDATE Room SET occupied = occupied - 1 WHERE id = (SELECT room_id FROM Student WHERE id = student_id) AND apartment_id = (SELECT apartment_id FROM Student WHERE id = student_id);
        -- If the student is the president of the old room, set the president to NULL
        UPDATE Room SET president = NULL WHERE president = student_id AND id = (SELECT room_id FROM Student WHERE id = student_id) AND apartment_id = (SELECT apartment_id FROM Student WHERE id = student_id);
        -- If the old room is not in the AvailableRooms table, add it
        IF NOT EXISTS (SELECT * FROM AvailableRooms WHERE room_id = (SELECT room_id FROM Student WHERE id = student_id) AND apartment_id = (SELECT apartment_id FROM Student WHERE id = student_id)) THEN
            INSERT INTO AvailableRooms (room_id, apartment_id) VALUES ((SELECT room_id FROM Student WHERE id = student_id), (SELECT apartment_id FROM Student WHERE id = student_id));
        END IF;
        -- Update the student
        UPDATE Student SET apartment_id = new_apart, room_id = new_room WHERE id = student_id;
        -- Update the new room
        UPDATE Room SET occupied = occupied + 1 WHERE id = new_room AND apartment_id = new_apart;
        -- If the new room is full and is in the AvailableRooms table, remove it
        IF (SELECT occupied FROM Room WHERE id = new_room AND apartment_id = new_apart) = (SELECT max_occupancy FROM Room WHERE id = new_room AND apartment_id = new_apart) AND EXISTS (SELECT * FROM AvailableRooms WHERE room_id = new_room AND apartment_id = new_apart) THEN
            DELETE FROM AvailableRooms WHERE room_id = new_room AND apartment_id = new_apart;
        END IF;
    END IF;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_student_photo(IN student_id VARCHAR(20), IN new_photo MEDIUMBLOB)
BEGIN
    UPDATE Student SET photo = new_photo WHERE id = student_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_manager_phone(IN manager_id VARCHAR(20), IN new_phone VARCHAR(15))
BEGIN
    UPDATE Manager SET phone = new_phone WHERE id = manager_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_manager_password(IN manager_id VARCHAR(20), IN new_password VARCHAR(50))
BEGIN
    UPDATE Manager SET password = new_password WHERE id = manager_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_manager_photo(IN manager_id VARCHAR(20), IN new_photo MEDIUMBLOB)
BEGIN
    UPDATE Manager SET photo = new_photo WHERE id = manager_id;
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
CREATE PROCEDURE update_room_max(IN ro_id VARCHAR(20), IN apart_id VARCHAR(20), IN new_max INT)
BEGIN
    UPDATE Room SET max_occupancy = new_max WHERE id = ro_id AND apartment_id = apart_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_room_occupied(IN ro_id VARCHAR(20), IN apart_id VARCHAR(20), IN new_occupied INT)
BEGIN
    UPDATE Room SET occupied = new_occupied WHERE id = ro_id AND apartment_id = apart_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_room_president(IN ro_id VARCHAR(20), IN apart_id VARCHAR(20), IN new_president VARCHAR(20))
BEGIN
    UPDATE Room SET president = new_president WHERE id = ro_id AND apartment_id = apart_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE report_maintenance(IN student_id VARCHAR(20), IN student_name VARCHAR(50), IN ro_id VARCHAR(20), IN apart_id VARCHAR(20), IN fault_in VARCHAR(1000), IN fault_photo MEDIUMBLOB)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Rollback the transaction in case of an error
        ROLLBACK;
    END;

    START TRANSACTION;
    INSERT INTO Maintenance (room_id, apartment_id, reporter_id, reporter_name, fault_info, approval_status, application_time) VALUES (ro_id, apart_id, student_id, student_name, fault_in, 'Pending', NOW());
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
CREATE PROCEDURE update_visitor_name(IN iden_card VARCHAR(50), IN new_name VARCHAR(50))
BEGIN
    UPDATE Visitor SET name = new_name WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_visitor_category(IN iden_card VARCHAR(50), IN new_category VARCHAR(20))
BEGIN
    UPDATE Visitor SET category = new_category WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_visitor_phone(IN iden_card VARCHAR(50), IN new_phone VARCHAR(15))
BEGIN
    UPDATE Visitor SET phone = new_phone WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_visitor_purpose(IN iden_card VARCHAR(50), IN new_purpose VARCHAR(1000))
BEGIN
    UPDATE Visitor SET purpose = new_purpose WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_visitor_target_room(IN iden_card VARCHAR(50), IN new_target_room VARCHAR(20))
BEGIN
    UPDATE Visitor SET target_room = new_target_room WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_visitor_target_apartment(IN iden_card VARCHAR(50), IN new_target_apartment VARCHAR(20))
BEGIN
    UPDATE Visitor SET target_apartment = new_target_apartment WHERE id_card = iden_card;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_visitor_departure_time(IN iden_card VARCHAR(50), IN new_departure_time DATETIME)
BEGIN
    UPDATE Visitor SET departure_time = new_departure_time WHERE id_card = iden_card;
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
    DECLARE student_name VARCHAR(50);
    DECLARE room_id VARCHAR(20);
    DECLARE apartment_id VARCHAR(20);
    DECLARE student_phone VARCHAR(15);
    SELECT name, room_id, apartment_id, phone INTO student_name, room_id, apartment_id, student_phone FROM Student WHERE id = student_id;
    INSERT INTO LeaveApplication (student_id, student_name, room_id, apartment_id, leave_time, expected_return_time, approval_status, purpose, destination, phone) VALUES (student_id, student_name, room_id, apartment_id, leave_time, expected_return_time, 'Pending', purpose, destination, student_phone);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE apply_for_return(IN student_id VARCHAR(20), IN return_time DATETIME)
BEGIN
    DECLARE student_name VARCHAR(50);
    DECLARE room_id VARCHAR(20);
    DECLARE apartment_id VARCHAR(20);
    DECLARE student_phone VARCHAR(15);
    SELECT name, room_id, apartment_id, phone INTO student_name, room_id, apartment_id, student_phone FROM Student WHERE id = student_id;
    INSERT INTO ReturnApplication (student_id, student_name, room_id, apartment_id, return_time, approval_status, phone) VALUES (student_id, student_name, room_id, apartment_id, return_time, 'Pending', student_phone);
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
