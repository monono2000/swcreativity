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
    bottom_size FLOAT,
    outer_size VARCHAR(10),
    waist_cm INT NOT NULL
);

CREATE TABLE SizeInfo (
    size_id INT PRIMARY KEY AUTO_INCREMENT,
    body_id INT,
    top_size VARCHAR(10),
    bottom_size FLOAT,
    outer_size VARCHAR(10),
    FOREIGN KEY (body_id) REFERENCES BodyInfo(body_id)
);

-- 3. 스타일 테이블
CREATE TABLE Style (
    style_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL
);

-- 4. 성별 테이블
CREATE TABLE Gender (
    gender_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL --skasudklefjk
);

-- 5. 색상 테이블
CREATE TABLE Color (
    color_id INT PRIMARY KEY AUTO_INCREMENT,
    color VARCHAR(50) NOT NULL, -- 색상
    style VARCHAR(50) NOT NULL, -- 스타일 (예: Amekaji, Street, etc.)
    type VARCHAR(10) NOT NULL  -- 상의 또는 하의
);


-- 6. 색상 매칭
CREATE TABLE ColorMatching (
    matching_id INT PRIMARY KEY AUTO_INCREMENT, -- 고유 매칭 ID
    style VARCHAR(50) NOT NULL,                 -- 스타일 이름
    season VARCHAR(10) NOT NULL,                -- 계절 (봄, 여름, 가을, 겨울)
    outer_color VARCHAR(50) NULL,
    top_color VARCHAR(50) NULL,
    bottom_color VARCHAR(50) NULL
);

-- 7. 옷 종류 추천
CREATE TABLE OutfitRecommendation (
    outfit_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique outfit ID
    style VARCHAR(50),                        -- Style name
    season VARCHAR(10),                       -- Season (Spring, Summer, Fall, Winter)
    outerwear VARCHAR(255),                   -- Recommended outerwear
    top VARCHAR(255),                         -- Recommended top
    bottom VARCHAR(255)                       -- Recommended bottom
);



CREATE TABLE TempInput (
    temp_id INT PRIMARY KEY AUTO_INCREMENT,
    season VARCHAR(20) NOT NULL,
    height_cm INT NOT NULL,
    weight_kg INT NOT NULL,
    waist_cm INT NOT NULL,
    style VARCHAR(50) NOT NULL,
    preferred_color VARCHAR(50)
);

