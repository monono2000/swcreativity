SELECT 
    o.name AS outfit_name,
    s.name AS style_name,
    se.name AS season_name,
    g.name AS gender_name,
    c.name AS color_name,
    o.description
FROM Outfit o
JOIN Style s ON o.style_id = s.style_id
JOIN Season se ON o.season_id = se.season_id
JOIN Gender g ON o.gender_id = g.gender_id
JOIN Color c ON o.color_id = c.color_id
WHERE o.season_id = 2  -- 여름
  AND o.style_id = 2   -- 스트릿
  AND o.gender_id = 3; -- 중성
