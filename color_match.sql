SELECT 
    c1.name AS base_color,
    c2.name AS matching_color
FROM ColorMatching cm
JOIN Color c1 ON cm.base_color_id = c1.color_id
JOIN Color c2 ON cm.matching_color_id = c2.color_id
WHERE c1.name = '화이트';
