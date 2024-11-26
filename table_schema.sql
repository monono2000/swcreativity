CREATE DATABASE clothing_recommendation;
USE clothing_recommendation;

-- 1. 계절 테이블
CREATE TABLE Season (
    season_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL
);

-- 2. 신체 정보 테이블
CREATE TABLE BodyInfo (
    body_id INT PRIMARY KEY AUTO_INCREMENT,
    gender VARCHAR(10) NOT NULL,
    height_cm INT NOT NULL,
    weight_kg INT NOT NULL,
    top_size VARCHAR(10),
    bottom_size VARCHAR(10),
    outer_size VARCHAR(10)
);

-- 3. 스타일 테이블
CREATE TABLE Style (
    style_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

-- 4. 성별 테이블
CREATE TABLE Gender (
    gender_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL
);

-- 5. 색상 테이블
CREATE TABLE Color (
    color_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

-- 6. 코디 세트 테이블
CREATE TABLE Outfit (
    outfit_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    style_id INT,
    season_id INT,
    gender_id INT,
    color_id INT,
    description TEXT,
    FOREIGN KEY (style_id) REFERENCES Style(style_id),
    FOREIGN KEY (season_id) REFERENCES Season(season_id),
    FOREIGN KEY (gender_id) REFERENCES Gender(gender_id),
    FOREIGN KEY (color_id) REFERENCES Color(color_id)
);

-- 7. 색상 매칭 테이블
CREATE TABLE ColorMatching (
    base_color_id INT,
    matching_color_id INT,
    FOREIGN KEY (base_color_id) REFERENCES Color(color_id),
    FOREIGN KEY (matching_color_id) REFERENCES Color(color_id)
);
