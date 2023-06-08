/*
SET GLOBAL event_scheduler = ON;

DELIMITER //
CREATE EVENT update_student_state_event
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    UPDATE Student
    SET state = 0
    WHERE id IN (
        SELECT student_id
        FROM LeaveApplication
        WHERE approval_status = 'Accept' AND leave_time <= CURDATE()
    );
END; //
DELIMITER ;
*/
DELIMITER //
CREATE TRIGGER update_completion_time
AFTER UPDATE ON Maintenance
FOR EACH ROW
BEGIN
    IF NEW.approval_status = 'Accept' THEN
        UPDATE Maintenance
        SET completion_time = NOW()
        WHERE id = NEW.id;
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_maintenance_status_after_update
AFTER UPDATE ON Maintenance
FOR EACH ROW
BEGIN
    DECLARE room_count INT;
    DECLARE accepted_count INT;

    SELECT COUNT(*), SUM(IF(approval_status = 'Accept', 1, 0)) INTO room_count, accepted_count FROM Maintenance WHERE room_id = NEW.room_id AND apartment_id = NEW.apartment_id;

    IF room_count = accepted_count THEN
        UPDATE Room SET maintenance_status = 'Accept' WHERE id = NEW.room_id AND apartment_id = NEW.apartment_id;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_maintenance_status_after_insert
AFTER INSERT ON Maintenance
FOR EACH ROW
BEGIN
    UPDATE Room SET maintenance_status = 'Pending' WHERE id = NEW.room_id AND apartment_id = NEW.apartment_id;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER insert_room
AFTER INSERT ON Room
FOR EACH ROW
BEGIN
    IF NEW.occupied < NEW.max_occupancy AND NOT EXISTS (SELECT 1 FROM AvailableRooms WHERE apartment_id = NEW.apartment_id AND room_id = NEW.id) THEN
        INSERT INTO AvailableRooms (apartment_id, room_id) VALUES (NEW.apartment_id, NEW.id);
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_room_insert
AFTER UPDATE ON Room
FOR EACH ROW
BEGIN
    IF NEW.occupied < NEW.max_occupancy AND NOT EXISTS (SELECT 1 FROM AvailableRooms WHERE apartment_id = NEW.apartment_id AND room_id = NEW.id) THEN
        INSERT INTO AvailableRooms (apartment_id, room_id) VALUES (NEW.apartment_id, NEW.id);
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_room_delete
AFTER UPDATE ON Room
FOR EACH ROW
BEGIN
    IF NEW.occupied = NEW.max_occupancy THEN
        DELETE FROM AvailableRooms WHERE apartment_id = NEW.apartment_id AND room_id = NEW.id;
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER insert_student
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM AvailableRooms WHERE apartment_id = NEW.apartment_id AND room_id = NEW.room_id) THEN
        UPDATE Room SET occupied = occupied + 1 WHERE apartment_id = NEW.apartment_id AND id = NEW.room_id;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot insert student into a full room.';
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER delete_student
AFTER DELETE ON Student
FOR EACH ROW
BEGIN
    UPDATE Room 
    SET occupied = occupied - 1,
        president = CASE WHEN president = OLD.id THEN NULL ELSE president END
    WHERE apartment_id = OLD.apartment_id AND id = OLD.room_id;
END; //
DELIMITER ;
