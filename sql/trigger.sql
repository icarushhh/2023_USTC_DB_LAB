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
