DELIMITER //

CREATE TRIGGER after_bodyinfo_insert
AFTER INSERT ON BodyInfo
FOR EACH ROW
BEGIN
    IF NEW.height_cm <= 160 AND NEW.weight_kg <= 55 THEN
        UPDATE BodyInfo SET top_size = 'S', bottom_size = 'S', outer_size = 'S' WHERE body_id = NEW.body_id;
    ELSEIF NEW.height_cm <= 170 AND NEW.weight_kg <= 70 THEN
        UPDATE BodyInfo SET top_size = 'M', bottom_size = 'M', outer_size = 'M' WHERE body_id = NEW.body_id;
    ELSE
        UPDATE BodyInfo SET top_size = 'L', bottom_size = 'L', outer_size = 'L' WHERE body_id = NEW.body_id;
    END IF;
END;
//

DELIMITER ;
