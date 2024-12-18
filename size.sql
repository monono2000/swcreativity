DELIMITER //

CREATE TRIGGER after_tempinput_insert
AFTER INSERT ON TempInput
FOR EACH ROW
BEGIN
    -- SizeInfo 테이블에 사이즈 삽입: CASE 문을 사용해 범위별 사이즈 설정
    INSERT INTO SizeInfo (top_size, outer_size)
    VALUES (
        CASE
            WHEN NEW.height_cm >= 180 AND NEW.weight_kg >= 80 THEN 'XXL'
            WHEN NEW.height_cm >= 175 AND NEW.weight_kg >= 73 THEN 'XL'
            WHEN NEW.height_cm >= 170 AND NEW.weight_kg >= 67 THEN 'L'
            WHEN NEW.height_cm >= 165 AND NEW.weight_kg >= 62 THEN 'M'
            ELSE 'S'
        END,
        CASE
            WHEN NEW.height_cm >= 180 AND NEW.weight_kg >= 80 THEN 'XXL'
            WHEN NEW.height_cm >= 175 AND NEW.weight_kg >= 73 THEN 'XL'
            WHEN NEW.height_cm >= 170 AND NEW.weight_kg >= 67 THEN 'L'
            WHEN NEW.height_cm >= 165 AND NEW.weight_kg >= 62 THEN 'M'
            ELSE 'S'
        END
    );
END;
//

DELIMITER ;
