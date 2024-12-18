DELIMITER //

CREATE TRIGGER after_bodyinfo_insert
AFTER INSERT ON BodyInfo
FOR EACH ROW
BEGIN
    -- 기본값 설정
    UPDATE BodyInfo SET top_size = 'S', outer_size = 'S' WHERE body_id = NEW.body_id;

    -- 상의 사이즈 설정 (범위 기반)
    IF NEW.height_cm >= 180 AND NEW.weight_kg >= 80 THEN
        UPDATE BodyInfo SET top_size = 'XXL', outer_size = 'XXL' WHERE body_id = NEW.body_id;
    ELSEIF NEW.height_cm >= 175 AND NEW.weight_kg >= 73 THEN
        UPDATE BodyInfo SET top_size = 'XL', outer_size = 'XL' WHERE body_id = NEW.body_id;
    ELSEIF NEW.height_cm >= 170 AND NEW.weight_kg >= 67 THEN
        UPDATE BodyInfo SET top_size = 'L', outer_size = 'L' WHERE body_id = NEW.body_id;
    ELSEIF NEW.height_cm >= 165 AND NEW.weight_kg >= 62 THEN
        UPDATE BodyInfo SET top_size = 'M', outer_size = 'M' WHERE body_id = NEW.body_id;
    END IF;
END;
//

DELIMITER ;
