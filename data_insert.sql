-- 계절 데이터
INSERT INTO Season (name) VALUES ('Spring'), ('Summer'), ('Autumn'), ('Winter');

-- 성별 데이터
INSERT INTO Gender (name) VALUES ('Male'), ('Female'), ('Unisex');

-- 스타일 데이터
INSERT INTO Style (name) VALUES 
    ('Amekaji'), ('Street'), ('Casual'), ('Minimal');

-- Amekaji 데이터
INSERT INTO Color (color, style, type) VALUES
('Beige', 'Amekaji', 'Top'),
('Navy', 'Amekaji', 'Top'),
('Olive', 'Amekaji', 'Top'),
('Brown', 'Amekaji', 'Top'),
('White', 'Amekaji', 'Top'),
('Light Blue', 'Amekaji', 'Bottom'),
('Denim', 'Amekaji', 'Bottom'),
('Olive', 'Amekaji', 'Bottom'),
('Brown', 'Amekaji', 'Bottom'),
('Beige', 'Amekaji', 'Bottom'),
('Khaki', 'Amekaji', 'Outerwear'),
('Navy', 'Amekaji', 'Outerwear'),
('Black', 'Amekaji', 'Outerwear');

-- Street 데이터
INSERT INTO Color (color, style, type) VALUES
('Black', 'Street', 'Top'),
('White', 'Street', 'Top'),
('Gray', 'Street', 'Top'),
('Burgundy', 'Street', 'Top'),
('Blue', 'Street', 'Top'),
('Black', 'Street', 'Bottom'),
('Gray', 'Street', 'Bottom'),
('Khaki', 'Street', 'Bottom'),
('Light Blue', 'Street', 'Bottom'),
('Denim', 'Street', 'Bottom'),
('Black', 'Street', 'Outerwear'),
('Gray', 'Street', 'Outerwear'),
('Navy', 'Street', 'Outerwear');

-- Casual 데이터
INSERT INTO Color (color, style, type) VALUES
('White', 'Casual', 'Top'),
('Pastel', 'Casual', 'Top'),
('Gray', 'Casual', 'Top'),
('Navy', 'Casual', 'Top'),
('Beige', 'Casual', 'Top'),
('Light Blue', 'Casual', 'Bottom'),
('Denim', 'Casual', 'Bottom'),
('Beige', 'Casual', 'Bottom'),
('Black', 'Casual', 'Bottom'),
('Khaki', 'Casual', 'Bottom'),
('Beige', 'Casual', 'Outerwear'),
('White', 'Casual', 'Outerwear'),
('Black', 'Casual', 'Outerwear');

-- Minimal 데이터
INSERT INTO Color (color, style, type) VALUES
('White', 'Minimal', 'Top'),
('Black', 'Minimal', 'Top'),
('Gray', 'Minimal', 'Top'),
('Beige', 'Minimal', 'Top'),
('Navy', 'Minimal', 'Top'),
('Black', 'Minimal', 'Bottom'),
('Navy', 'Minimal', 'Bottom'),
('Gray', 'Minimal', 'Bottom'),
('Beige', 'Minimal', 'Bottom'),
('Light Blue', 'Minimal', 'Bottom'),
('Denim', 'Minimal', 'Bottom'),
('Black', 'Minimal', 'Outerwear'),
('Navy', 'Minimal', 'Outerwear'),
('Gray', 'Minimal', 'Outerwear');

-- 색상 매칭 데이터

-- 색상 매칭 데이터 삽입
INSERT INTO ColorMatching (style, season, outer_color, top_color, bottom_color) VALUES
-- Amekaji - Spring
('Amekaji', 'Spring', 'Khaki', 'Beige', 'Light Blue'),
('Amekaji', 'Spring', 'Navy', 'White', 'Beige'),
('Amekaji', 'Spring', 'Khaki', 'Olive', 'Brown'),
('Amekaji', 'Spring', 'Navy', 'Navy', 'Denim'),
('Amekaji', 'Spring', 'Black', 'Olive', 'Khaki'),
('Amekaji', 'Spring', 'Gray', 'Navy', 'Denim'),
('Amekaji', 'Spring', 'Beige', 'White', 'Gray'),
('Amekaji', 'Spring', 'Navy', 'Olive', 'Light Blue'),

-- Amekaji - Summer
('Amekaji', 'Summer', 'Beige', 'White', 'Light Blue'),
('Amekaji', 'Summer', 'Beige', 'Beige', 'Olive'),
('Amekaji', 'Summer', 'Olive', 'Olive', 'Denim'),
('Amekaji', 'Summer', 'Navy', 'Navy', 'Light Blue'),
('Amekaji', 'Summer', 'Black', 'White', 'Gray'),
('Amekaji', 'Summer', 'Navy', 'Beige', 'Olive'),
('Amekaji', 'Summer', 'Gray', 'Light Blue', 'Khaki'),
('Amekaji', 'Summer', 'Beige', 'Olive', 'Denim'),

-- Amekaji - Autumn
('Amekaji', 'Autumn', 'Black', 'Brown', 'Light Blue'),
('Amekaji', 'Autumn', 'Khaki', 'Navy', 'Denim'),
('Amekaji', 'Autumn', 'Black', 'Olive', 'Brown'),
('Amekaji', 'Autumn', 'Black', 'Navy', 'Light Blue'),
('Amekaji', 'Autumn', 'Gray', 'Beige', 'Khaki'),
('Amekaji', 'Autumn', 'Navy', 'Olive', 'Brown'),
('Amekaji', 'Autumn', 'Beige', 'White', 'Gray'),
('Amekaji', 'Autumn', 'Navy', 'Light Blue', 'Olive'),

-- Amekaji - Winter
('Amekaji', 'Winter', 'Black', 'White', 'Olive'),
('Amekaji', 'Winter', 'Black', 'Navy', 'Light Blue'),
('Amekaji', 'Winter', 'Gray', 'Olive', 'Beige'),
('Amekaji', 'Winter', 'Navy', 'White', 'Khaki'),
('Amekaji', 'Winter', 'Beige', 'Gray', 'Light Blue'),
('Amekaji', 'Winter', 'Black', 'Olive', 'Navy'),
('Amekaji', 'Winter', 'Khaki', 'Brown', 'Light Blue'),
('Amekaji', 'Winter', 'Gray', 'White', 'Olive'),

-- Amekaji 모든 계절 올블랙 조합
('Amekaji', 'Spring', 'Black', 'Black', 'Black'),
('Amekaji', 'Summer', 'Black', 'Black', 'Black'),
('Amekaji', 'Autumn', 'Black', 'Black', 'Black'),
('Amekaji', 'Winter', 'Black', 'Black', 'Black'),

-- Street 모든 계절 올블랙 조합
('Street', 'Spring', 'Black', 'Black', 'Black'),
('Street', 'Summer', 'Black', 'Black', 'Black'),
('Street', 'Autumn', 'Black', 'Black', 'Black'),
('Street', 'Winter', 'Black', 'Black', 'Black'),

-- Casual 모든 계절 올블랙 조합
('Casual', 'Spring', 'Black', 'Black', 'Black'),
('Casual', 'Summer', 'Black', 'Black', 'Black'),
('Casual', 'Autumn', 'Black', 'Black', 'Black'),
('Casual', 'Winter', 'Black', 'Black', 'Black'),

-- Minimal 모든 계절 올블랙 조합
('Minimal', 'Spring', 'Black', 'Black', 'Black'),
('Minimal', 'Summer', 'Black', 'Black', 'Black'),
('Minimal', 'Autumn', 'Black', 'Black', 'Black'),
('Minimal', 'Winter', 'Black', 'Black', 'Black'),

-- Street 기본 색상 조합 (무채색 기반)
('Street', 'Spring', 'Black', 'Black', 'Black'),
('Street', 'Spring', 'Gray', 'White', 'Black'),
('Street', 'Summer', 'Black', 'Black', 'White'),
('Street', 'Autumn', 'Black', 'Black', 'Gray'),
('Street', 'Winter', 'White', 'Black', 'Gray'),

-- Casual 기본 색상 조합 (무채색 기반)
('Casual', 'Spring', 'Black', 'White', 'Black'),
('Casual', 'Spring', 'Gray', 'Black', 'White'),
('Casual', 'Summer', 'Gray', 'White', 'Gray'),
('Casual', 'Autumn', 'Black', 'Black', 'Gray'),
('Casual', 'Winter', 'Gray', 'White', 'Black'),

-- Minimal 기본 색상 조합 (무채색 기반)
('Minimal', 'Spring', 'Black', 'Black', 'White'),
('Minimal', 'Summer', 'Gray', 'White', 'Black'),
('Minimal', 'Autumn', 'Black', 'Gray', 'White'),
('Minimal', 'Winter', 'Black', 'Black', 'Gray'),
('Minimal', 'Winter', 'White', 'Black', 'Charcoal');


-- 7. 코디 데이터 삽입
-- Amekaji
-- Spring
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Amekaji', 'Spring', 'Jacket', 'Shirt', 'Jeans'),
('Amekaji', 'Spring', 'Trucker Jacket', 'T-shirt', 'Chino Pants'),
('Amekaji', 'Spring', NULL, 'Flannel Shirt', 'Pants'),
('Amekaji', 'Spring', NULL, 'Sweatshirt', 'Loose Fit Jeans');

-- Summer
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Amekaji', 'Summer', NULL, 'Linen Shirt', 'Rolled Chino Pants'),
('Amekaji', 'Summer', NULL, 'Polo Shirt', 'Cargo Shorts'),
('Amekaji', 'Summer', NULL, 'Chambray Shirt', 'Denim Shorts'),
('Amekaji', 'Summer', NULL, 'Half-open Shirt', 'Slim Fit Chino Pants');

-- Autumn
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Amekaji', 'Autumn', 'Trench Coat', 'Knit Sweater', 'Corduroy Pants'),
('Amekaji', 'Autumn', 'Waxed Cotton Jacket', 'Thermal Henley', 'Wool Pants'),
('Amekaji', 'Autumn', 'Military Parka', 'Flannel Shirt', 'Dark Wash Jeans'),
('Amekaji', 'Autumn', 'Harrington Jacket', 'Chunky Cardigan', 'Straight Jeans');

-- Winter
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Amekaji', 'Winter', 'Heavy Parka', 'Turtleneck Sweater', 'Fleece-lined Pants'),
('Amekaji', 'Winter', 'Shearling Coat', 'Fisherman Sweater', 'Jeans'),
('Amekaji', 'Winter', 'Duffel Coat', 'Flannel Shirt', 'Corduroy Pants'),
('Amekaji', 'Winter', 'Long Parka', 'Wool Sweater', 'Cargo Pants');

-- Street
-- Spring
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Street', 'Spring', 'Hoodie', 'Graphic T-shirt', 'Cargo Pants'),
('Street', 'Spring', NULL, 'Long Sleeve T-shirt', 'Jogger Pants'),
('Street', 'Spring', 'Windbreaker', 'Sweatshirt', 'Track Pants'),
('Street', 'Spring', 'Bomber Jacket', 'Oversized Hoodie', 'Slim Fit Jogger Pants');

-- Summer
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Street', 'Summer', NULL, 'Tank Top', 'Basketball Shorts'),
('Street', 'Summer', NULL, 'Oversized T-shirt', 'Cuffed Shorts'),
('Street', 'Summer', NULL, 'V-neck T-shirt', 'Utility Shorts'),
('Street', 'Summer', NULL, 'Longline T-shirt', 'Loose Fit Pants');

-- Autumn
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Street', 'Autumn', 'Denim Jacket', 'Layered Hoodie', 'Distressed Jeans'),
('Street', 'Autumn', 'Padded Jacket', 'Crewneck Sweatshirt', 'Cargo Pants'),
('Street', 'Autumn', 'Varsity Jacket', 'Graphic Hoodie', 'Loose Fit Pants'),
('Street', 'Autumn', 'Anorak Jacket', 'Long Sleeve Shirt', 'Fitted Jogger Pants');

-- Winter
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Street', 'Winter', 'Long Puffer', 'Oversized Sweater', 'Tech Fleece Pants'),
('Street', 'Winter', 'Parka', 'Fleece Hoodie', 'Track Pants'),
('Street', 'Winter', 'Fur Coat', 'Turtleneck Sweater', 'Wide Fit Jeans'),
('Street', 'Winter', 'Quilted Jacket', 'Knit Hoodie', 'Cargo Pants');

-- Casual
-- Spring
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Casual', 'Spring', 'Lightweight Blazer', 'V-neck T-shirt', 'Chino Pants'),
('Casual', 'Spring', NULL, 'Cotton Shirt', 'Ankle Pants'),
('Casual', 'Spring', 'Trench Coat', 'Henley Shirt', 'Jeans'),
('Casual', 'Spring', 'Quilted Jacket', 'Knit Sweater', 'Pants');

-- Summer
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Casual', 'Summer', NULL, 'Polo Shirt', 'Shorts'),
('Casual', 'Summer', NULL, 'Linen Shirt', 'Crop Pants'),
('Casual', 'Summer', NULL, 'Crewneck T-shirt', 'Chino Pants'),
('Casual', 'Summer', NULL, 'Half-open Shirt', 'Slim Fit Jeans');

-- Autumn
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Casual', 'Autumn', 'Wool Cardigan', 'Long Sleeve Shirt', 'Dark Wash Jeans'),
('Casual', 'Autumn', 'Pea Coat', 'Knit Sweater', 'Slim Fit Pants'),
('Casual', 'Autumn', 'Trench Coat', 'Oxford Shirt', 'Corduroy Pants'),
('Casual', 'Autumn', 'Shawl Collar Jacket', 'Turtleneck Sweater', 'Straight Chino Pants');

-- Winter
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Casual', 'Winter', 'Wool Coat', 'Chunky Sweater', 'Jeans'),
('Casual', 'Winter', 'Long Puffer', 'Fleece Hoodie', 'Cargo Pants'),
('Casual', 'Winter', 'Down Jacket', 'Thermal T-shirt', 'Wool Pants'),
('Casual', 'Winter', 'Shearling Jacket', 'Knit Sweater', 'Corduroy Pants');

-- Minimal
-- Spring
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Minimal', 'Spring', 'Blazer', 'Shirt', 'Slim Fit Pants'),
('Minimal', 'Spring', NULL, 'Turtleneck', 'Crop Pants'),
('Minimal', 'Spring', 'Coat', 'Knit', 'Wide Fit Pants'),
('Minimal', 'Spring', 'Jacket', 'Long Sleeve Shirt', 'Ankle Pants');

-- Summer
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Minimal', 'Summer', NULL, 'Linen Shirt', 'Tapered Pants'),
('Minimal', 'Summer', NULL, 'Slim Fit T-shirt', 'Chino Pants'),
('Minimal', 'Summer', NULL, 'Polo Shirt', 'Crop Pants'),
('Minimal', 'Summer', NULL, 'Long Sleeve T-shirt', 'Wide Fit Pants');

-- Autumn
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Minimal', 'Autumn', 'Overcoat', 'Turtleneck Knit', 'Slim Fit Pants'),
('Minimal', 'Autumn', 'Wool Blazer', 'Shirt', 'Corduroy Pants'),
('Minimal', 'Autumn', 'Trench Coat', 'Knit Sweater', 'Slacks'),
('Minimal', 'Autumn', 'Long Jacket', 'Long Sleeve Shirt', 'Straight Pants');

-- Winter
INSERT INTO OutfitRecommendation (style, season, outerwear, top, bottom) VALUES
('Minimal', 'Winter', 'Wool Coat', 'Turtleneck Knit', 'Slim Fit Pants'),
('Minimal', 'Winter', 'Long Puffer', 'Hoodie', 'Jogger Pants'),
('Minimal', 'Winter', 'Double Coat', 'Layered Knit', 'Wide Fit Pants'),
('Minimal', 'Winter', 'Wool Jacket', 'Knit Turtleneck', 'Fleece-lined Pants');
