-- 계절 데이터
INSERT INTO Season (name) VALUES ('Spring'), ('Summer'), ('Autumn'), ('Winter');

-- 성별 데이터
INSERT INTO Gender (name) VALUES ('Male'), ('Female'), ('Unisex');

-- 스타일 데이터
INSERT INTO Style (name) VALUES 
    ('밀리터리'), ('스트릿'), ('캐주얼'), ('아메카지'), 
    ('남친룩'), ('클래식'), ('포멀'), ('댄디룩'), ('미니멀');

-- 색상 데이터
INSERT INTO Color (name) VALUES
    ('화이트'), ('블랙'), ('네이비'), ('레드'), ('그린'), ('베이지');

-- 색상 매칭 데이터
INSERT INTO ColorMatching (base_color_id, matching_color_id) VALUES
    (1, 2), (1, 3), (2, 1), (2, 4), 
    (3, 1), (3, 5), (4, 2), (4, 6),
    (5, 3), (5, 6), (6, 1), (6, 4);

-- 코디 데이터
INSERT INTO Outfit (name, style_id, season_id, gender_id, color_id, description) VALUES
    ('밀리터리 자켓', 1, 1, 1, 6, '봄 시즌에 적합한 밀리터리 자켓'),
    ('스트릿 후드티', 2, 2, 3, 2, '여름용 스트릿 스타일 후드티'),
    ('캐주얼 셔츠', 3, 3, 2, 1, '가을에 입기 좋은 캐주얼 셔츠'),
    ('아메카지 코트', 4, 4, 1, 3, '겨울에 어울리는 아메카지 코트');
