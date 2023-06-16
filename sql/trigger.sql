DELIMITER //
CREATE TRIGGER update_completion_time
BEFORE UPDATE ON Maintenance
FOR EACH ROW
BEGIN
    IF NEW.approval_status = '已完成' THEN
        SET NEW.completion_time = NOW();
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

    SELECT COUNT(*), SUM(IF(approval_status = '已完成', 1, 0)) INTO room_count, accepted_count FROM Maintenance WHERE room_id = NEW.room_id AND apartment_id = NEW.apartment_id;

    IF room_count = accepted_count THEN
        UPDATE Room SET maintenance_status = '已完成' WHERE id = NEW.room_id AND apartment_id = NEW.apartment_id;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_maintenance_status_after_insert
AFTER INSERT ON Maintenance
FOR EACH ROW
BEGIN
    UPDATE Room SET maintenance_status = '待维修' WHERE id = NEW.room_id AND apartment_id = NEW.apartment_id;
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

DELIMITER //
CREATE TRIGGER update_occupancy 
AFTER UPDATE ON Student
FOR EACH ROW
BEGIN
    -- 如果宿舍ID改变
    IF NEW.room_id != OLD.room_id OR NEW.apartment_id != OLD.apartment_id THEN
        -- 在旧宿舍将occupied人数减1
        UPDATE Room 
        SET occupied = occupied - 1
        WHERE id = OLD.room_id AND apartment_id = OLD.apartment_id AND occupied > 0;

        -- 在新宿舍将occupied人数加1
        UPDATE Room 
        SET occupied = occupied + 1
        WHERE id = NEW.room_id AND apartment_id = NEW.apartment_id AND occupied < max_occupancy;
    END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_student_state_after_return_approval
AFTER UPDATE ON ReturnApplication
FOR EACH ROW
BEGIN
    IF NEW.approval_status = '已通过' AND NEW.student_id IN (SELECT id FROM Student WHERE state = 0) THEN
        UPDATE Student SET state = 1 WHERE id = NEW.student_id;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_student_state_after_leave_approval
AFTER UPDATE ON LeaveApplication
FOR EACH ROW
BEGIN
    IF NEW.approval_status = '已通过' AND NEW.student_id IN (SELECT id FROM Student WHERE state = 1) THEN
        UPDATE Student SET state = 0 WHERE id = NEW.student_id;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER delete_existing_leave_application
BEFORE INSERT ON LeaveApplication
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM LeaveApplication
        WHERE student_id = NEW.student_id AND approval_status = '审核中'
    ) THEN
        DELETE FROM LeaveApplication
        WHERE student_id = NEW.student_id AND approval_status = '审核中';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER delete_existing_return_application
BEFORE INSERT ON ReturnApplication
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM ReturnApplication
        WHERE student_id = NEW.student_id AND approval_status = '审核中'
    ) THEN
        DELETE FROM ReturnApplication
        WHERE student_id = NEW.student_id AND approval_status = '审核中';
    END IF;
END //
DELIMITER ;
